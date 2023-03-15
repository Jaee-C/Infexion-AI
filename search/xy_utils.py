from .types import Action, BoardState

def update_board_state(state: BoardState, action: Action) -> BoardState:
    """
    Updates the board state by applying the given action.
    """
    print("update board state")

def is_goal_reached(state: BoardState) -> bool:
    """
    Checks if the goal state (all pieces on board are Red) has been reached. Returns `True` if goal has been reached, `False` otherwise.
    """
    dim = 7
    for r in range(0, dim):
        for q in range(0, dim):
            if (r, q) in state and state[(r, q)][0] == "b":
                return False
    return True