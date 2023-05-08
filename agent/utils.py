from referee.game.actions import Action, SpawnAction, SpreadAction
from referee.game.board import Board
from referee.game.constants import BOARD_N, MAX_TOTAL_POWER
from referee.game.hex import HexDir, HexPos
from referee.game.player import PlayerColor


def find_possible_actions(b: Board, c: PlayerColor, spawn_limit: int=3) -> list[Action]:
        possible_actions: list[Action] = find_spread_actions(b, 
            c) + find_spawn_actions(b, spawn_limit)
        return possible_actions

def find_spread_actions(b: Board, color: PlayerColor) -> list[Action]:
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

    for i in range(BOARD_N):
        for j in range(BOARD_N):
            if b[HexPos(i, j)].player == color:
                new_actions = [SpreadAction(
                    HexPos(i, j), direction) for direction in HexDir]
                action_list += new_actions

    return action_list

def find_spawn_actions(b, limit=3) -> list[Action]:
    action_list: list[Action] = []
    
    # Check if max power reached
    if (b._total_power >= MAX_TOTAL_POWER):
        return action_list

    # Find unoccupied cells
    for i in range(BOARD_N):
        for j in range(BOARD_N):
            if b[HexPos(i, j)].player == None:
                new_action = SpawnAction(HexPos(i, j))
                action_list.append(new_action)

    # only return the first action for now -- add a new more spawn options otherwise insta win
    if limit == None:
        return action_list
    return action_list[0:limit]