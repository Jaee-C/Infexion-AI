from .utils import render_board, get_num_spreads
from .types import BoardState, Action

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
        print(f"- Actions: {self.actions}\n- Cost: {self.cost}\n- Estimated Cost: {self.estimated_cost}")
        print(render_board(self.state, ansi=False))

    def evaluation_function(self) -> int:
        return self.cost + get_num_spreads(self.state)

    def __lt__(self, other: object) -> bool:
        return self.estimated_cost < other.estimated_cost
    
    def __str__(self):
        return f"({self.estimated_cost},{len(self.actions)})"

    def __repr__(self):
        return f"({self.estimated_cost},{len(self.actions)})"