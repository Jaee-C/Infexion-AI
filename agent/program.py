# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from .constants import COLOUR, POWER
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from referee.game.constants import BOARD_N, MAX_CELL_POWER
from referee.game.hex import HexDir
from referee.game.board import Board
from utils import find_possible_actions

# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        self._state: Board = Board()
        self.first = True
        # self._prev_state: Board = Board()
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        match self._color:
            case PlayerColor.RED:
                # return self.find_possible_actions(self._state)[0]
                best_action, cost = self.minimax(
                    self._state, 3, True, float('-inf'), float('inf'))
                # print(f"Testing: {self._color}, {best_action}, {cost}")
                return best_action
            case PlayerColor.BLUE:
                # return self.find_possible_actions(self._state)[0]
                best_action, cost = self.minimax(
                    self._state, 3, True, float('-inf'), float('inf'))
                # print(best_action, cost)
                return best_action

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent's state with the last player's action.
        """
        match action:
            case SpawnAction(cell):
                self._state.apply_action(action)
            case SpreadAction(cell, direction):
                self._state.apply_action(action)

    def evaluate_value(self, b: Board) -> int:
        # Count agent's power
        power = 0
        for cell in b._state:
            if b[cell].power > 0:
                if b[cell].player == self._color:
                    power += b[cell].power
                else:
                    power -= b[cell].power
        return power

    

    def minimax(self, b: Board, depth: int, is_max: bool, alpha: int, beta: int) -> tuple[Action, int]:
        if depth == 0:
            # print(b.render())
            # print(f"TESING: {self.evaluate_value(b)}")
            return None, self.evaluate_value(b)
        if b.game_over:
            winner = b.winner_color
            # pos or neg depending on ismax or not
            return None, float('inf') if winner == self._color else float('-inf')
        

        colour = self._color if is_max else self._color.opponent
        curr_max = float('-inf')
        curr_min = float('inf')
        all_actions = find_possible_actions(b, colour)
        best_action = all_actions[0]
        for action in find_possible_actions(b, colour):
            b.apply_action(action)
            _, val = self.minimax(b, depth-1, not is_max, alpha, beta)
            if is_max and val > curr_max:
                curr_max = val
                best_action = action
                alpha = max(alpha, curr_max)
                if beta <= alpha:
                    b.undo_action()
                    break
            elif not is_max and val < curr_min:
                curr_min = val
                best_action = action
                beta = min(beta, curr_min)
                if beta <= alpha:
                    b.undo_action()
                    break
            b.undo_action()

        if is_max:
            cost = curr_max
        else:
            cost = curr_min
        return best_action, cost
