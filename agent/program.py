# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from .minimax import MinimaxAgent
from referee.game import \
    PlayerColor, Action
from .board import Board

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
        match color:
            case PlayerColor.RED:
                self.opponent = PlayerColor.BLUE
            case PlayerColor.BLUE:
                self.opponent = PlayerColor.RED
        self._agent = MinimaxAgent(self._color, "eval_func1")

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        action, _ = self._agent.minimax(self._state, MAX_DEPTH, True, float('-inf'), float('inf'))
        return action
    
    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent's state with the last player's action.
        """
        self._state.apply_action(action)