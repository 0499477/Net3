# Routing Algorithm Assignment: Distance Vector and Split Horizon

## Overview
This project simulates routing in a network of routers using two algorithms:
- **Distance Vector (DV)**
- **Split Horizon (SH)**

It reads network topologies and updates from standard input and prints:
- Step-by-step **distance tables**
- Final **routing tables**

## Files

- `distance_vector.py` – Standard DV implementation
- `split_horizon.py` – DV with Split Horizon improvement
- `test_input.txt` – Example test input

## Input Format
The input must be provided via standard input and must follow this structure:

```text
X
Y
Z
DISTANCEVECTOR
X Z 8
X Y 2
Y Z 3
UPDATE
Y Z -1
X Z 3
END
```

### Explanation:
- First lines: list of router names (one per line)
- `DISTANCEVECTOR`: signals start of topology definition
- Lines after: direct links between routers with their cost
- `UPDATE`: defines changes in the network (cost update or removal with -1)
- `END`: signals end of input and triggers final convergence + output

## Output Format

1. **Distance Table:** printed for every router at each time step
2. **Routing Table:** printed once after convergence

### Example Routing Table Output:
```text
X Routing Table:
Y,Y,2
Z,Y,5
```

## How to Run

### Prerequisites
- Python 3.6+ (pre-installed in most Unix environments)

### Run Distance Vector
```bash
python3 distance_vector.py < test_input.txt
```

### Run Split Horizon
```bash
python3 split_horizon.py < test_input.txt
```

## Notes
- `INF` indicates unreachable destinations.
- All routers update synchronously at each step.
- Updates in the input can remove links or add new routers.

## Logbook Requirement
You must maintain a development logbook (e.g., `logbook.txt`) with:
- Dates and tasks
- Design decisions
- Testing and debugging observations

## License
This assignment is part of academic coursework and not licensed for distribution.
