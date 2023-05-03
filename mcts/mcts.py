from referee.game import Action, Board
from agent.program import Agent
from agent.utils import find_possible_actions
from referee.game.constants import BOARD_N
from referee.game.hex import HexDir, HexPos
import random
from referee.game import PlayerColor
from referee.game.board import CellState
import math

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
    
    def print_tree(self):
        # pretty print a dictionary as a table
        print("{:10s} | {:10s} | {:10s} | {:10s} | {:10s} | {:10s}".format("hash", "wins", "visits", "ucb", "children", "parents"))
        for hash, node in self.tree.items():
            print("{:10s} | {:10d} | {:10d} | {:10d} | {:10d} | {:10d}".format(hash, node["wins"], node["visits"], node["ucb"], len(node["children"]), len(node["parents"])))


    def hash(self, b: Board) -> str:
        hash = ""
        for i in range(BOARD_N):
            for j in range(BOARD_N):
                cell = HexPos(i, j)
                if b[cell].player != None:
                    player_short = "R" if b[cell].player == PlayerColor.RED else "B"
                    cell_short = str(cell).replace("-", "")
                    hash += f"{cell_short}:{player_short}{str(b[cell.power])},"   # r-q:COLOR<POWER> | eg. "00R1,10B2,..." : {...}
        print("Hashed Board")
        # print(b.render())
        print(f"hash: {hash}")
        return hash
    
    def unhash(self, s: str) -> Board:
        state: Board = Board()
        for entry in s.split(","):
            if len(entry) == 0:
                continue
            r, q, player_short, power = entry.split("")
            player: PlayerColor = PlayerColor.RED if player_short == "R" else PlayerColor.BLUE
            state[HexPos(r, q)] = CellState(player, power)
        return state

    def selection(self, parent_hash: str):
        if self.tree == {}:
            return (None, parent_hash)
        # Select the child with the highest UCB value
        parent = self.tree[parent_hash]
        for (action, child_hash) in parent["children"]:
            print(f"Selecting child {child_hash} with action {str(action)}")
            if child_hash not in self.tree:
                return (parent_hash, action)
            
                self.tree[child_hash]["parents"].append(parent_hash)
            child = self.tree[child_hash]
            max_ucb = -1
            max_ucb_hash = ""
            if child["ucb"] > max_ucb:
                max_ucb = child["ucb"]
                max_ucb_hash = child_hash
        return self.selection(self, max_ucb_hash)
    
    def expansion(self, parent_hash: str, child_hash: str):
        # Create the new child node and add to the tree
        print(f"Expanding child {child_hash}")
        actions: list[Action] = find_possible_actions(self.unhash(child_hash), PlayerColor.RED)
        hashed_children = [(a, None) for a in actions]
        self.tree[child_hash] = {
            "wins": 0,
            "visits": 0,
            "ucb": 0,
            "children": hashed_children,
            "parents": [parent_hash]
        }
        self.print_tree()
        for child_hash in hashed_children:
            if child_hash in self.tree and self.tree[child_hash]["parents"]:
                # child has already been visited by another parent - add this parent and backpropagate child's stats
                self.tree[child_hash]["parents"].append(parent_hash)

    def simulation(self, b: Board, player: PlayerColor) -> int:
        # possible optimisation: evaluation function for every move
        temp_board = Board(b._state)
        temp_board._turn_color = player
        while not temp_board.game_over:
            minimax_player = Agent(temp_board._turn_color)
            minimax_player._state = temp_board
            action = minimax_player.action()
            # action = random.choice(find_possible_actions(temp_board, temp_board._turn_color))
            print(str(action))
            temp_board.apply_action(action)
            print(temp_board.render())

        return 1 if temp_board.winner_color == player else 0

    def backpropagation(self, isWin: int, child_hash: str):
        # Update the wins, visits and UCB of the child node and all its parents
        # Use UCB1 formula for selection
        # UCB = (num_wins / num_visits) + C * sqrt(log(parent.num_visits) / num_visits)
        self.tree[child_hash]["wins"] += isWin
        self.tree[child_hash]["visits"] += 1

        # use the parent with maximum visits to calculate UCB of child
        parent_visits = max([self.tree[parent_hash]["visits"] for parent_hash in self.tree[child_hash]["parents"]])
        self.tree[child_hash]["ucb"] = (self.tree[child_hash]["wins"] / self.tree[child_hash]["visits"]) + 1.41 * math.sqrt(math.log(parent_visits) / self.tree[child_hash]["visits"])

        # update parent's wins, visits and backpropagate
        for parent_hash in self.tree[child_hash]["parents"]:
            self.tree[parent_hash]["wins"] += isWin
            self.tree[parent_hash]["visits"] += 1
            return self.backpropagation(self, isWin, parent_hash)
    
    def mcts(self, num_iterations: int):
        b = Board()
        for i in range(num_iterations):
            print("MCTS Iteration {i}")
            print(b.render())
            parent_hash, child_hash = self.selection(self.hash(b))
            new_child = self.expansion(parent_hash, child_hash)
            isWin = self.simulation(b, PlayerColor.RED)
            self.backpropagation(isWin, new_child)
            print(self.tree)

def main():
    mcts = MonteCarloTreeSearch()
    board = Board()
    mcts.mcts(100)