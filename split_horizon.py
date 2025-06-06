#!/usr/bin/env python3

import sys
import copy
from collections import defaultdict

INF = 9999

class Router:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}  # Direct neighbors with link cost
        self.distance_table = defaultdict(lambda: defaultdict(lambda: INF))  # destination -> via -> cost
        self.routing_table = {}  # destination -> (next_hop, cost)

    def initialize(self, nodes):
        for dest in nodes:
            for via in nodes:
                self.distance_table[dest][via] = INF
            if dest == self.name:
                self.distance_table[dest][self.name] = 0

    def update_neighbor(self, neighbor, cost):
        self.neighbors[neighbor] = cost
        self.distance_table[neighbor][neighbor] = cost

    def send_distance_vector(self):
        # Send vector excluding paths learned via each neighbor (Split Horizon)
        vectors = {}
        for neighbor in self.neighbors:
            vec = {}
            for dest in self.distance_table:
                if dest == neighbor:
                    continue
                best_via = min(self.distance_table[dest], key=lambda v: self.distance_table[dest][v])
                if best_via == neighbor:
                    continue  # Split Horizon: do not send back route learned from neighbor
                vec[dest] = self.distance_table[dest][best_via]
            vectors[neighbor] = vec
        return vectors

    def receive_update(self, from_router, vector):
        changed = False
        for dest, cost in vector.items():
            new_cost = self.neighbors[from_router] + cost
            if new_cost < self.distance_table[dest][from_router]:
                self.distance_table[dest][from_router] = new_cost
                changed = True
        return changed

    def compute_routing_table(self):
        self.routing_table = {}
        for dest in sorted(self.distance_table):
            if dest == self.name:
                continue
            best_hop, best_cost = None, INF
            for via in sorted(self.distance_table[dest]):
                cost = self.distance_table[dest][via]
                if cost < best_cost:
                    best_hop = via
                    best_cost = cost
            if best_cost == INF:
                self.routing_table[dest] = ("INF", INF)
            else:
                self.routing_table[dest] = (best_hop, best_cost)

    def print_distance_table(self, timestep):
        print(f"{self.name} Distance Table at t={timestep}")
        dests = sorted(self.distance_table.keys())
        vias = sorted(self.distance_table.keys())
        header = "    " + "  ".join(vias)
        print(header)
        for dest in dests:
            row = [dest]
            for via in vias:
                val = self.distance_table[dest][via]
                row.append(str(val) if val != INF else "INF")
            print("  ".join(row))
        print()

    def print_routing_table(self):
        print(f"{self.name} Routing Table:")
        for dest in sorted(self.routing_table):
            hop, cost = self.routing_table[dest]
            cost_str = str(cost) if cost != INF else "INF"
            print(f"{dest},{hop},{cost_str}")
        print()

def parse_input():
    routers = {}
    nodes = []
    topology = []
    updates = []
    mode = None

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        if line == 'DISTANCEVECTOR':
            mode = 'topology'
            continue
        elif line == 'UPDATE':
            mode = 'update'
            continue
        elif line == 'END':
            break

        if mode is None:
            nodes.append(line)
        elif mode == 'topology':
            topology.append(line.split())
        elif mode == 'update':
            updates.append(line.split())

    return nodes, topology, updates

def build_network(nodes, topology):
    routers = {name: Router(name) for name in nodes}
    for router in routers.values():
        router.initialize(nodes)
    for src, dst, cost in topology:
        cost = int(cost)
        if cost != -1:
            routers[src].update_neighbor(dst, cost)
            routers[dst].update_neighbor(src, cost)
    return routers

def split_horizon_algorithm(routers):
    timestep = 0
    converged = False
    while not converged:
        print(f"=== Step {timestep} ===")
        for router in sorted(routers):
            routers[router].print_distance_table(timestep)

        updates = {}
        for name, router in routers.items():
            updates[name] = router.send_distance_vector()

        any_change = False
        for receiver_name, router in routers.items():
            for sender_name in router.neighbors:
                if sender_name in routers and receiver_name in updates[sender_name]:
                    changed = router.receive_update(sender_name, updates[sender_name])
                    any_change = any_change or changed

        if not any_change:
            converged = True
        timestep += 1

    for router in routers.values():
        router.compute_routing_table()
    for name in sorted(routers):
        routers[name].print_routing_table()

def apply_updates(routers, updates):
    for update in updates:
        src, dst, cost = update
        cost = int(cost)
        if src not in routers:
            routers[src] = Router(src)
        if dst not in routers:
            routers[dst] = Router(dst)
        for r in routers.values():
            r.initialize(routers.keys())
        if cost == -1:
            routers[src].neighbors.pop(dst, None)
            routers[dst].neighbors.pop(src, None)
        else:
            routers[src].update_neighbor(dst, cost)
            routers[dst].update_neighbor(src, cost)

def main():
    nodes, topology, updates = parse_input()
    routers = build_network(nodes, topology)
    split_horizon_algorithm(routers)
    if updates:
        apply_updates(routers, updates)
        split_horizon_algorithm(routers)

if __name__ == '__main__':
    main()
