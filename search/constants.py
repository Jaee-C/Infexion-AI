# Index of keys in BoardState
COLOR = 0
POWER = 1

# Board coordinates
R = 0
Q = 1

# Color of occupied cell
RED = "r"
BLUE = "b"

# Action directions
DIRECTIONS: dict[str, tuple[int, int]] = {
    "TOP": (1, -1),
    "BOTTOM": (-1, 1),
    "TOP_LEFT": (0, -1),
    "TOP_RIGHT": (1, 0),
    "BOTTOM_LEFT": (-1, 0),
    "BOTTOM_RIGHT": (0, 1)
}
