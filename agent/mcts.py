from referee.game import Action, Board
from agent.program import Agent
from utils import find_possible_actions
from referee.game.constants import BOARD_N
from referee.game.hex import HexDir, HexPos
import random
from referee.game.actions import PlayerColor
from referee.game.board import CellState

class MonteCarloTreeSearch():

    """
    Tree representation

    hashed_state(str): {
        wins: int,
        visits: int,
        ucb: int,
        children: [(move(Action), hashed_state(str)), (... , ...), ...],
        parents: [hashed_state(str)]
    }
    """
    Child = (Action, str)

    def __init__(self) -> None:
        self.tree = {}

    def hash(b: Board) -> str:
        hash = ""
        for cell in b._state:
            if b[cell].player != None:
                player_short = "R" if b[cell].player == PlayerColor.RED else "B"
                cell_short = str(cell).replace("-", "")
                hash += f"{cell_short}:{player_short}{str(b[cell.power])},"   # r-q:COLOR<POWER> | eg. "00R1,10B2,..." : {...}
        return hash
    
    def unhash(s: str) -> Board:
        state: Board = {}
        for entry in s.split(","):
            if len(entry) == 0:
                continue
            r, q, player_short, power = entry.split("")
            player: PlayerColor = PlayerColor.RED if player_short == "R" else PlayerColor.BLUE
            state[HexPos(r, q)] = CellState(player, power)
        return Board()

    def selection(self, parent_hash):
        # Select the child with the highest UCB value
        parent = self.tree[parent_hash]
        for (_, child_hash) in parent["children"]:
            if child_hash not in self.tree:
                return child_hash
            child = self.tree[child_hash]
            max_ucb = -1
            max_ucb_hash = ""
            if child["ucb"] > max_ucb:
                max_ucb = child["ucb"]
                max_ucb_hash = child_hash
        return self.selection(self, max_ucb_hash)
    
    def expansion():

        pass

    def simulation(self, b: Board, player: PlayerColor):
        # possible optimisation: evaluation function for every move
        tempboard = Board(b._state)
        tempboard._turn_color = player
        while not b.game_over:
            action = random.choice(find_possible_actions(b, player))
            tempboard.apply_action(action)

        return 1 if tempboard.winner_color == player else 0

    def backpropagation():
        # Use UCB1 formula for selection
        # UCB = (num_wins / num_visits) + C * sqrt(log(parent.num_visits) / num_visits)
        

        pass
    
    def mcts(b: Board):
        pass

    