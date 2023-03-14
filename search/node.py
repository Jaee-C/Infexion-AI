from .types import BoardState, Action

# NOTE: I think this class is better placed in `types` sincce we use it as a type anyways
class Node():
    def __init__(self, state: BoardState, actions: list[Action], cost: int):
        self.state = state
        self.actions = actions
        self.cost = cost