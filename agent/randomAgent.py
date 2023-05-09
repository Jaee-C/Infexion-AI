from argparse import Action
import random
from .board import Board
from .utils import find_possible_actions
from referee.game.player import PlayerColor

class RandomAgent():
    """
    Agent that takes random actions.
    """
    def __init__(self, color: PlayerColor):
        self._color = color
    def action(self, b: Board) -> Action:
        actions = find_possible_actions(b, self._color)
        return actions[random.randint(0, len(actions) - 1)]