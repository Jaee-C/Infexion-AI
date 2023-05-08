# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction
from .board import Board
from .transposition import Transposition
from .utils import find_possible_actions

MAX_DEPTH = 3

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
        self.transposition_table = Transposition()
        self.total_time_spent = 0
        self.turns = 0
        self.opponent = None
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
                self.opponent = PlayerColor.BLUE
            case PlayerColor.BLUE:
                self.opponent = PlayerColor.RED
                print("Testing: I am playing as blue")

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        res = self.minimax(self._state, 3, True, float('-inf'), float('inf'))

        if referee["space_remaining"] and referee["space_remaining"] <= 5:
            self.transposition_table.clear()

        return res[0]

        # match self._color:
        #     case PlayerColor.RED:
        #         res = self.random_actions(self._state)
        #         return res
        #     case PlayerColor.BLUE:
        #         res = self.minimax(self._state, 3, True, float('-inf'), float('inf'))
        #         self.total_time_spent += 180 - referee['time_remaining']
        #         return res[0]

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent's state with the last player's action.
        """
        match action:
            case SpawnAction(cell):
                self._state.apply_action(action)
            case SpreadAction(cell, direction):
                self._state.apply_action(action)
        self.turns += 1
        # print(f"Average time spent: {self.total_time_spent / self.turns}")

    def evaluate_value(self, b: Board) -> int:
        # Count agent's power
        power = 0
        for cell in b._state:
            if b[cell].power > 0:
                if b[cell].player == self._color:
                    power += b[cell].power
                else:
                    power -= b[cell].power

        power += (len(b._player_cells(self._color)) - len(b._player_cells(self.opponent)))
        
        return power
    
    

    def minimax(self, b: Board, depth: int, is_max: bool, alpha: int, beta: int) -> tuple[Action, int]:
        
        if depth == 0:
            return None, self.evaluate_value(b)
        if b.game_over:
            winner = b.winner_color
            # pos or neg depending on ismax or not
            if winner == self._color:
                return None, float('inf')
            else:
                return None, float('-inf')
        
        alpha_org = alpha
        beta_org = beta
        b_hash = b.get_hash()

        # Probe the transposition table to see if we have a useable matching
        # entry from the current position. If we get a hit, return the score
        # and stop searching.
        tt_score, should_use, best_move = self.transposition_table.find(b_hash, depth, alpha, beta)

        if should_use:
            return best_move, tt_score

        colour = self._color if is_max else self._color.opponent
        curr_max = float('-inf')
        curr_min = float('inf')
        all_actions = find_possible_actions(b, colour)
        best_action = all_actions[0]
        for action in all_actions:
            b.apply_action(action)
            _, val = self.minimax(b, depth-1, not is_max, alpha, beta)
            if is_max and val > curr_max:
                curr_max = val
                best_action = action
                alpha = max(alpha, curr_max)
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

        b_hash = self._state.get_hash()
        self.transposition_table.store(b_hash, cost, best_action, depth, alpha_org, beta_org)
        
        return best_action, cost
