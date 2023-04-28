# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from agent.constants import POWER
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from referee.game.constants import BOARD_N, MAX_CELL_POWER
from referee.game.hex import HexDir
from .types import BoardState


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
        self._state: BoardState = {}
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
                print(self._state)
                if len(self._state) > 0:
                    return SpreadAction(HexPos(3, 3), HexDir.Up)
                return SpawnAction(HexPos(3, 3))
            case PlayerColor.BLUE:
                # This is going to be invalid... BLUE never spawned!
                return SpawnAction(HexPos(2, 3))
                # return SpreadAction(HexPos(3, 3), HexDir.Up)

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        match action:
            case SpawnAction(cell):
                # print(f"Testing: {color} SPAWN at {cell}")
                self._state[cell] = (color, 1)
            case SpreadAction(cell, direction):
                # print(f"Testing: {color} SPREAD from {cell}, {direction}")
                (r, q, dr, dq) = (cell.r, cell.q, direction.r, direction.q)
                new_state = self._state.copy()
                (spread_colour, spread_power) = new_state[cell]
                
                # Empty the current cell
                del new_state[cell]

                # Update the power of the cell that is being spread to
                for i in range(1, spread_power + 1):
                    current_cell = ((r + dr * i) % BOARD_N, (q + dq * i) % BOARD_N)
                    new_power = new_state[current_cell][POWER] + 1 if current_cell in new_state else 1

                    # Empty the cell if it has reached max power
                    if new_power == MAX_CELL_POWER:
                        new_state.pop(current_cell)
                    else:
                        new_state[current_cell] = (spread_colour, new_power)
                self._state = new_state

    def evaluate_value(self, b: BoardState) -> int:

        return
    
    def terminal_test(self, b: BoardState) -> PlayerColor:
        return
    
    def find_possible_actions(self, b: BoardState) -> list[Action]:
        possible_actions: list[Action] = self.find_spread_actions(self._color) 
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

        for coords, cell in self._state.items():
            if cell[0] == color:
                for direction in HexDir:
                    new_action = Action(coords, direction)
                    action_list.append(new_action)
        
        return action_list
    
    def find_spawn_actions(self) -> list[Action]:
        action_list: list[Action] = []

        # for 

        return action_list

    def minimax(self, b:BoardState, depth:int, is_max:bool) -> tuple[Action, int]:
        if depth == 0:
                return None, self.evaluate_value(b)
        winner=self.terminal_test(b)
        if winner != None:
            return None, float('inf') if winner == self.color else float('-inf') # pos or neg depending on ismax or not

        curr_max = float('-inf')
        curr_min = float('inf')
        best_action = None
        for action in self.find_possible_actions(b):
            b.apply_action(action)
            _, val = self.minimax(b, depth-1, not is_max)
            if is_max:
                curr_max = max(val, curr_max)
                best_action = action
            else:
                curr_min = min(val, curr_min)
                best_action = action
            b.undo_action()
        
        if is_max:
            cost = curr_max
        else:
            const = curr_min
        return best_action, cost
