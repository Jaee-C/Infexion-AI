from .types import BoardState, Action

class Node():
    def __init__(self, state: BoardState, actions: list[Action], cost: int):
        self.state = state
        self.actions = actions
        self.cost = cost