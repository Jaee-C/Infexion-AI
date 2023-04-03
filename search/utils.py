# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from numpy import sign
from .types import Action, BoardState
from .constants import BOARD_BOUNDARY, COLOR, MAX_INT, MAX_POWER, POWER, BLUE, DIRECTIONS

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


def find_colour_coordinates(state: BoardState, colour: str) -> list[tuple[int, int]]:
    """
    Given a board, find all the coordinates in the board.
    Returns a lists of (r, q) coordinates that corresponds to red cells 
    in the given board.

    Arguments:
    state -- current state of the game board
    colour -- either "r" or "b"

    Returns:
    List of coordinates on the board which contains red pieces
    """
    red_coordinates = []
    for coord in state:
        if state[coord][COLOR] == colour:
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


def is_goal_reached(state: BoardState) -> bool:
    """
    Determine if the agent has reached the goal state. There are no blue cells
    on the board.

    Arguments:
    state -- current state of the game board

    Returns:
    `True` if the goal state is reached (ie. all pieces on board are Red), `False` otherwise.
    """
    for color, _ in state.values():
        if color == BLUE:
            return False
    return True


def update_board_states(state: BoardState, action: Action) -> BoardState:
    """
    Update the board state given an action.

    Arguments:
    state -- current state of the game board
    action -- the action to be taken

    Returns:
    The updated board state.
    """
    (r, q, dr, dq) = action
    new_state = state.copy()
    (spread_colour, spread_power) = new_state[(r, q)]
    
    # Empty the current cell
    del new_state[(r, q)]

    # Update the power of the cell that is being spread to
    for i in range(1, spread_power + 1):
        current_cell = ((r + dr * i) % BOARD_BOUNDARY, (q + dq * i) % BOARD_BOUNDARY)
        new_power = new_state[current_cell][POWER] + 1 if current_cell in new_state else 1

        # Empty the cell if it has reached max power
        if new_power == MAX_POWER:
            new_state.pop(current_cell)
        else:
            new_state[current_cell] = (spread_colour, new_power)
    return new_state

def circular_min_diff(a: int, b: int) -> int:
    """
    Get the minimum difference between two numbers on a circular array. 
    Used to calculate manhattan distance of two coordinates on a board.
    
    Example:
    distance between 0 and 6 on a circular array of size 7 is 1, not 6.

    first diff = 6
    ┍-----┷-----┑
    0 1 2 3 4 5 6 0 1 2 3 4 5 6
                ┕┯┙
            second diff = 1
    """
    first_diff = abs(a - b)
    second_diff = abs(min(a, b) + BOARD_BOUNDARY - max(a, b))
    return min(first_diff, second_diff)

def get_num_spreads(state: BoardState) -> int:
    """
    Sums the minimum number of SPREAD actions from each blue cell to any other cell.

    Arguments:
    state -- current state of the game board

    Returns:
    The sum of the minimum number of SPREAD actions from each blue cell to any other cell.
    """
    total_spreads = 0
    for blue in find_colour_coordinates(state, BLUE):
        min_spreads = MAX_INT
        for other in state:
            if blue == other:
                continue
            diff_r = blue[0] - other[0]
            diff_q = blue[1] - other[1]

            # SPREAD cannot perform turns, so an extra move is needed when a turn is required
            curr_bend = 0
            if not in_straight_line(other, blue):
                curr_bend = 1

            # If the difference in r and q are the same sign, then the distance is the absolute value of the difference
            # Otherwise, the distance is the minimum difference between the two coordinates
            curr_distance = abs(diff_q + diff_r) if sign(diff_r) == sign(diff_q) else max(circular_min_diff(blue[0], other[0]), circular_min_diff(blue[1], other[1]))

            # Update the minimum distance, assuming each move can have a SPREAD power of 6 (relaxed problem)
            if curr_distance // 6 + curr_bend + 1 < min_spreads:
                min_spreads = curr_distance // 6 + curr_bend + 1

        total_spreads += min_spreads
    
    return total_spreads

def in_straight_line(cell1: tuple[int, int], cell2: tuple[int, int]) -> bool:
    """
    Check if cell1 and cell2 are in a straight line.

    Arguments:
    cell1 -- coordinate of the first cell
    cell2 -- coordinate of the second cell

    Returns:
    `True` if both cell1 and cell2 are in a straight line, `False` otherwise.
    """
    diff_r = cell2[0] - cell1[0]
    diff_q = cell2[1] - cell1[1]
    return diff_r == 0 or diff_q == 0 or diff_r == diff_q or diff_r == -diff_q

def get_colour_power(state: BoardState, colour: str) -> int:
    """
    Sums the power of all `colour` cells on the board.

    Arguments:
    state -- current state of the game board
    colour -- either "r" or "b"

    Returns:
    The sum of the power of all `colour` cells on the board.
    """
    total_power = 0
    for cell in find_colour_coordinates(state, colour):
        total_power += state[cell][POWER]
    return total_power