BoardState = dict[tuple, tuple] # coordinate (r, q): cell state (colour, power)
Action = (int, int, int, int) # (r, q, dr, dq)