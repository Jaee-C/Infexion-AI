# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from mcts.mcts import MonteCarloTreeSearch
from .constants import COLOUR, POWER
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from referee.game.constants import BOARD_N, MAX_TOTAL_POWER
from referee.game.hex import HexDir
from .board import Board

import random

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
        self.transposition_table = {}
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
        res = self.minimax(self._state, 3, True, float('-inf'), float('inf'), 0)
        return res[0]

        match self._color:
            case PlayerColor.RED:
                # return self.find_possible_actions(self._state)[0]
                res = self.random_actions(self._state)
                # print(f"RED nodes {res[-1]}")
                return res
                # print(f"Testing: {self._color}, {best_action}, {cost}")
            case PlayerColor.BLUE:
                # return self.find_possible_actions(self._state)[0]
                res = self.minimax(self._state, 3, True, float('-inf'), float('inf'), 0)
                # print(f"BLUE nodes {res[-1]}")
                # print(best_action, cost)
                # print(f"TIME SPENT: {180 - referee['time_remaining']}")
                self.total_time_spent += 180 - referee['time_remaining']
                return res[0]

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

    def find_possible_actions(self, b: Board, c: PlayerColor) -> list[Action]:
        possible_actions: list[Action] = self.find_spread_actions(
            c) + self.find_spawn_actions()
        return possible_actions

    def find_spread_actions(self, color: PlayerColor) -> list[Action]:
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
                if self._state[HexPos(i, j)].player == color:
                    new_actions = [SpreadAction(
                        HexPos(i, j), direction) for direction in HexDir]
                    action_list += new_actions

        return action_list

    def find_spawn_actions(self) -> list[Action]:
        action_list: list[Action] = []

        # Find unoccupied cells
        for i in range(BOARD_N):
            for j in range(BOARD_N):
                if self._state[HexPos(i, j)].player == None:
                    new_action = SpawnAction(HexPos(i, j))
                    action_list.append(new_action)

        # only return the first action for now -- add a new more spawn options otherwise insta win
        return action_list[0:3]

    def minimax(self, b: Board, depth: int, is_max: bool, alpha: int, beta: int) -> tuple[Action, int]:
        if depth == 0:
            return None, self.evaluate_value(b), n
            # return self.quiescence_search(b, 3, not is_max, alpha, beta, n)
        if b.game_over:
            winner = b.winner_color
            # pos or neg depending on ismax or not
            if winner == self._color:
                return None, float('inf'), 0
            else:
                return None, float('-inf'), 0
        
        alpha_org = alpha
        b_hash = b.get_hash()
        if b_hash in self.transposition_table:
            tt_entry = self.transposition_table[b_hash]
            if tt_entry[1] == 'EXACT':
                return tt_entry[0][0], tt_entry[0][1], 1 
            elif tt_entry[1] == 'MAX':
                alpha = max(alpha, tt_entry[0][1])
            elif tt_entry[1] == 'MIN':
                beta = min(beta, tt_entry[0][1])
        n += 1
        colour = self._color if is_max else self._color.opponent
        curr_max = float('-inf')
        curr_min = float('inf')
        all_actions = find_possible_actions(b, colour)
        best_action = all_actions[0]
        for action in self.find_possible_actions(b, colour):
            b.apply_action(action)
            _, val, n1 = self.minimax(b, depth-1, not is_max, alpha, beta, n)
            n += n1
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

        self._store(self.transposition_table, b, alpha_org, beta, best_action, cost)
        
        return best_action, cost, n
    
    def quiescence_search(self, b: Board, depth: int, is_max: bool, alpha: int, beta: int, n: int) -> tuple[Action, int, int]:
        if b.game_over:
            winner = b.winner_color
            # pos or neg depending on ismax or not
            if winner == self._color:
                return [], float('inf'), 0
            else:
                return [], float('-inf'), 0
        
        n += 1
        colour = self._color if is_max else self._color.opponent
        capture_actions = list(filter(lambda x : self.is_a_capture(colour, x), self.find_possible_actions(b, colour)))

        if len(capture_actions) == 0 or depth == 0:
            return None, self.evaluate_value(b), 1

        alpha_org = alpha
        beta_org = beta
        b_hash = b.get_hash()
        if b_hash in self.transposition_table:
            tt_entry = self.transposition_table[b_hash]
            if tt_entry[1] == 'EXACT':
                return tt_entry[0][0], tt_entry[0][1], 1 
            elif tt_entry[1] == 'MAX':
                alpha = max(alpha, tt_entry[0][1])
            elif tt_entry[1] == 'MIN':
                beta = min(beta, tt_entry[0][1])
        curr_max = float('-inf')
        curr_min = float('inf')
        best_action = capture_actions[0]
        for action in capture_actions:
            if not b.validate_action(action):
                continue

            b.apply_action(action)
            _, val, n1 = self.minimax(b, depth-1, not is_max, alpha, beta, n)
            n += n1
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

        self._store(self.transposition_table, b, alpha_org, beta_org, best_action, cost)

        return best_action, cost, n
    
    def is_a_capture(self, p: PlayerColor, a: Action):
        opponent_color = PlayerColor.RED if p == PlayerColor.BLUE else PlayerColor.BLUE
        old_num_opponent = len(self._state._player_cells(opponent_color))
        self._state.apply_action(a);
        new_num_opponent = len(self._state._player_cells(opponent_color))
        self._state.undo_action()
        if new_num_opponent < old_num_opponent:
            print("old", old_num_opponent, self._state.render())
            self._state.apply_action(a);
            print("new", new_num_opponent, self._state.render())
            self._state.undo_action()
            return True
        return False

    def _store(self, table: dict, board: Board, alpha: int, beta: int, best, cost):
        if cost <= alpha:
            flag = 'MIN'
        elif cost >= beta:
            flag = 'MAX'
        else:
            flag = 'EXACT'

        table[board.get_hash()] = [(best, cost), flag]
