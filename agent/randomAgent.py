from argparse import Action
import random
from agent.board import Board

class RandomAgent():
    def random_actions(self, b: Board) -> Action:
        actions = self.find_possible_actions(b, self._color)
        return actions[random.randint(0, len(actions) - 1)]