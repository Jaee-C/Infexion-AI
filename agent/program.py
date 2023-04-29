# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from agent.constants import COLOUR, POWER
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from referee.game.constants import BOARD_N, MAX_CELL_POWER
from referee.game.hex import HexDir
from referee.game.board import Board


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
                best_action, cost = self.minimax(self._state, 3, True)
                print(f"Testing: {self._color}, {best_action}, {cost}")
                return best_action
            case PlayerColor.BLUE:
                # return self.find_possible_actions(self._state)[0]
                best_action, cost = self.minimax(self._state, 3, True)
                print(best_action, cost)
                return best_action

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent's state with the last player's action.
        """
        match action:
            case SpawnAction(cell):
                # print(f"Testing: {color} SPAWN at {cell}")
                # self._prev_state = self._state.copy()
                # self._state[cell] = (color, 1)
                # print(self._state[cell])
                self._state.apply_action(action)
            case SpreadAction(cell, direction):
                # print(f"Testing: {color} SPREAD from {cell}, {direction}")
                # self._prev_state = self._state.copy()
                print("SPREADS")
                (r, q, dr, dq) = (cell.r, cell.q, direction.r, direction.q)
                self._state.apply_action(action)
                # new_state = self._state.copy()
                # (spread_colour, spread_power) = new_state[cell]
                # self._state.apply_action(action)

                # Empty the current cell
                # del new_state[cell]

                # Update the power of the cell that is being spread to
                # for i in range(1, spread_power + 1):
                #     current_cell = ((r + dr * i) %
                #                     BOARD_N, (q + dq * i) % BOARD_N)
                #     new_power = new_state[current_cell][POWER] + \
                #         1 if current_cell in new_state else 1

                #     # Empty the cell if it has reached max power
                #     if new_power == MAX_CELL_POWER:
                #         new_state.pop(current_cell)
                #     else:
                #         new_state[current_cell] = (spread_colour, new_power)
                # self._state = new_state
        # print(f"prev_state: {self._prev_state}")
        # print(f"state: {self._state}")

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

    def terminal_test(self, b: Board) -> PlayerColor|None:
        return None

    def find_possible_actions(self, b: Board, c: PlayerColor) -> list[Action]:
        possible_actions: list[Action] = self.find_spread_actions(c)  + self.find_spawn_actions()
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
                    new_actions = [SpreadAction(HexPos(i, j), direction) for direction in HexDir]
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

    def minimax(self, b: Board, depth: int, is_max: bool) -> tuple[Action, int]:
        if depth == 0:
            # print(b.render())
            # print(f"TESING: {self.evaluate_value(b)}")
            return None, self.evaluate_value(b)
        winner = self.terminal_test(b)
        if winner != None:
            # pos or neg depending on ismax or not
            return None, float('inf') if winner == self._color else float('-inf')

        curr_max = float('-inf')
        curr_min = float('inf')
        best_action = None
        colour = self._color if is_max else self._color.opponent
        for action in self.find_possible_actions(b, colour):
            b.apply_action(action)
            _, val = self.minimax(b, depth-1, not is_max)
            if is_max and val > curr_max:
                curr_max = val
                best_action = action
            elif not is_max and val < curr_min:
                curr_min = val
                best_action = action
            b.undo_action()
            # self._state = self._prev_state

        if is_max:
            cost = curr_max
        else:
            cost = curr_min
        return best_action, cost
