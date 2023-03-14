# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from .types import Action, BoardState
from .constants import COLOR, RED, DIRECTIONS

def apply_ansi(str, bold=True, color=None):
    """
    Wraps a string with ANSI control codes to enable basic terminal-based
    formatting on that string. Note: Not all terminals will be compatible!

    Arguments:

    str -- String to apply ANSI control codes to
    bold -- True if you want the text to be rendered bold
    color -- Colour of the text. Currently only red/"r" and blue/"b" are
        supported, but this can easily be extended if desired...

    """
    bold_code = "\033[1m" if bold else ""
    color_code = ""
    if color == "r":
        color_code = "\033[31m"
    if color == "b":
        color_code = "\033[34m"
    return f"{bold_code}{color_code}{str}\033[0m"

def render_board(board: dict[tuple, tuple], ansi=False) -> str:
    """
    Visualise the Infexion hex board via a multiline ASCII string.
    The layout corresponds to the axial coordinate system as described in the
    game specification document.
    
    Example:

        >>> board = {
        ...     (5, 6): ("r", 2),
        ...     (1, 0): ("b", 2),
        ...     (1, 1): ("b", 1),
        ...     (3, 2): ("b", 1),
        ...     (1, 3): ("b", 3),
        ... }
        >>> print_board(board, ansi=False)

                                ..     
                            ..      ..     
                        ..      ..      ..     
                    ..      ..      ..      ..     
                ..      ..      ..      ..      ..     
            b2      ..      b1      ..      ..      ..     
        ..      b1      ..      ..      ..      ..      ..     
            ..      ..      ..      ..      ..      r2     
                ..      b3      ..      ..      ..     
                    ..      ..      ..      ..     
                        ..      ..      ..     
                            ..      ..     
                                ..     
    """
    dim = 7
    output = ""
    for row in range(dim * 2 - 1):
        output += "    " * abs((dim - 1) - row)
        for col in range(dim - abs(row - (dim - 1))):
            # Map row, col to r, q
            r = max((dim - 1) - row, 0) + col
            q = max(row - (dim - 1), 0) + col
            if (r, q) in board:
                color, power = board[(r, q)]
                text = f"{color}{power}".center(4)
                if ansi:
                    output += apply_ansi(text, color=color, bold=False)
                else:
                    output += text
            else:
                output += " .. "
            output += "    "
        output += "\n"
    return output


def find_red_coordinates(state: BoardState) -> list[tuple[int, int]]:
    """
    Given a board, find all the coordinates in the board.
    Returns a lists of (r, q) coordinates that corresponds to red cells 
    in the given board.

    Arguments:
    state -- current state of the game board

    Returns:
    List of coordinates on the board which contains red pieces
    """
    red_coordinates = []
    for coord in state:
        if state[coord][COLOR] == RED:
            red_coordinates.append(coord)

    return red_coordinates


def find_possible_actions(state: BoardState, coordinate: tuple[int, int]) -> list[Action]:
    """
    Find all the possible SPREAD actions that Red can make given a coordinate
    of a red cell. Returns a list of `Actions` that can be made.

    For each red cell, the red player can make 6 different SPREAD moves, in the
    6 directions of the cell.

    Arguments:
    state -- current state of the game board
    coordinate -- the coordinate of the piece to find actions of

    Returns:
    A list of possible actions to take from `coordinate`
    """
    action_list: list[Action] = []

    for direction in DIRECTIONS:
        action_list.append(coordinate + DIRECTIONS[direction])
    
    return action_list

