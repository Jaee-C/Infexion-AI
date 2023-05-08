# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from agent.minimax import MinimaxAgent
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction
from .board import Board
from .transposition import Transposition

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
                print("Testing: I am playing as red")
                self.opponent = PlayerColor.BLUE
            case PlayerColor.BLUE:
                self.opponent = PlayerColor.RED
                print("Testing: I am playing as blue")

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        match self._color:
            case PlayerColor.RED:
                minimax_agent_1 = MinimaxAgent(self._color, "eval_func1")
                action, cost = minimax_agent_1.minimax(self._state, 3, True, float('-inf'), float('inf'))
                return action
            case PlayerColor.BLUE:
                minimax_agent_2 = MinimaxAgent(self._color, "eval_func2")
                action, cost = minimax_agent_2.minimax(self._state, 3, True, float('-inf'), float('inf'))
                return action

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent's state with the last player's action.
        """
        match action:
            case SpawnAction(cell):
                self._state.apply_action(action)
            case SpreadAction(cell, direction):
                self._state.apply_action(action)

    