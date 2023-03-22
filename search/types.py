# BoardState:
# - key: coordinate - (r, q)
# - value: cell state - (color, power)
BoardState = dict[tuple, tuple]

# Action:
# (r, q, dr, dq), where dr is the r direction in which the action is to be taken
# and dq is the q direction in which the action is to be taken
Action = (int, int, int, int)
