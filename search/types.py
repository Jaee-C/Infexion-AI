# BoardState:
# - key: coordinate - (r, q)
# - value: cell state - (color, power)
BoardState = dict[tuple, tuple]

# Action:
# (r, q, dr, dq), where dr is the r direction in which the action is to be taken
# and dq is the q direction in which the action is to be taken
Action = (int, int, int, int)

class Node():
    def __init__(self, state: BoardState, actions: list[Action], cost: int):
        self.state = state
        self.actions = actions
        self.cost = cost
        self.estimated_cost = self.evaluation_function()
    def print_node(self):
        """
        Print the node's state, actions and cost
        """
        print(f"- Actions: {self.actions}\n- Cost: {self.cost}")
        from .utils import render_board
        print(render_board(self.state, ansi=False))
    def evaluation_function(self) -> int:
        return self.cost + distance_to_blues(self.state) + red_power(self.state)