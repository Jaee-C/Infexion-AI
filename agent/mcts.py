import random
import math
import csv
from agent.minimax import MinimaxAgent
from referee.game.actions import Action, SpawnAction, SpreadAction
from referee.game.board import Board, CellState
from referee.game.constants import BOARD_N
from referee.game.hex import HexDir, HexPos, HexVec
from referee.game.player import PlayerColor
from .utils import find_possible_actions

from .constants import UCB_CONSTANT

class MCTSAgent():
    """
    Monte Carlo Tree Search Agent
    """
    def __init__(self, tree={}) -> None:
        """
        Tree representation of the MCTS tree. The tree is represented as a dictionary of hashed states, where each hashed state is a dictionary of the form:
            hashed_state(str): {
                wins: int,
                visits: int,
                ucb: int,
                children: [(move(Action), hashed_state(str)), (... , ...), ...],
                parents: [hashed_state(str)]
            }
        """
        self.tree = tree
    
    def print_tree(self):
        """
        Pretty print the MCTS tree as a table.
        """
        print()
        print("{:100s} | {:10s} | {:10s} | {:10s} | {:10s} | {:10s} | {:5s}".format("hash", "wins", "visits", "ucb", "children", "parents", "is_red"))
        for hash, node in self.tree.items():
            print("{:100s} | {:10.1f} | {:10.1f} | {:10f} | {:10d} | {:10d} | {:5s}".format(hash, node["wins"], node["visits"], node["ucb"], len(node["children"]), len(node["parents"]), str(node["is_red_turn"])))


    def hash(self, b: Board) -> str:
        """
        Hashes the board state into a string, where each cell is represented as a string of the form: "r-q:COLOR<POWER>"
        where r and q are the row and column of the cell, COLOR is either "R" or "B" for red or blue, and POWER is the power of the cell. 
        Each cell is separated by commas (`,`).

        Arguments:
        b -- the board to hash

        Returns:
        A string representing the board state
        """
        hash = ""
        for i in range(BOARD_N):
            for j in range(BOARD_N):
                cell = HexPos(i, j)
                if b[cell].player != None:
                    player_short = "R" if b[cell].player == PlayerColor.RED else "B"
                    cell_short = str(cell).replace("-", "")
                    hash += f"{cell_short}{player_short}{str(b[cell].power)},"   # r-q:COLOR<POWER>
        hash = hash.strip(",")
        return hash
    
    def unhash(self, s: str) -> Board:
        """
        Unhashes the board state from a string, where each cell is represented as a string of the form: "r-q:COLOR<POWER>" to a Board object.

        Arguments:
        s -- the string to unhash

        Returns:
        A Board object representing the board state.
        """
        new_board: Board = Board()
        if s == "":
            return new_board
        for entry in s.split(","):
            if len(entry) == 0:
                continue
            r, q, player_short, power = int(entry[0]), int(entry[1]), entry[2], int(entry[3])
            player: PlayerColor = PlayerColor.RED if player_short == "R" else PlayerColor.BLUE
            new_board._state[HexPos(r, q)] = CellState(player, power)
        return new_board
    
    def unhash_action(self, s: str) -> Action:
        """
        Unhashes the action from a string of the form: "SPAWN(r, q)" or "SPREAD(r, q, dr, dq)" to an Action object.

        Arguments:
            s -- the string to unhash

        Returns:
            An Action object representing the action.
        """
        if s.startswith("SPAWN"):
            return SpawnAction(HexPos(int(s[6]), int(s[9])))
        if s.startswith("SPREAD"):
            pos = HexPos(int(s[7]), int(s[10]))
            dir_r, dir_q = s[13:-1].split(", ")
            dir = HexDir(HexVec(int(dir_r), int(dir_q)))
            return SpreadAction(pos, dir)

    def selection(self, parent_hash: str):
        """
        Start at the root node of the tree and recursively select the child node with the highest Upper Confidence Bound (UCB) until a leaf node is reached. The UCB value balances exploration (visiting less-visited nodes) and exploitation (favoring nodes with high estimated values).

        Arguments:
        parent_hash -- the hash of the parent node

        Returns:
        A tuple of (parent_hash, child_hash)
        """
        # print(f"SELECTION parent_hash: {parent_hash}")
        # Create parent node if not present in tree
        if parent_hash not in self.tree:
            self.expansion(None, parent_hash)
        
        # Select the child with the highest UCB value
        parent = self.tree[parent_hash]
        max_ucb = -1
        max_ucb_hash = ""
        for (action, child_hash) in parent["children"]:
            if child_hash == None:
                # Apply action to parent board
                temp_board = self.unhash(parent_hash)
                temp_board._turn_color = PlayerColor.RED if parent["is_red_turn"] else PlayerColor.BLUE
                temp_board.apply_action(self.unhash_action(action))

                # Update Child Node
                child_hash = self.hash(temp_board)
                self.tree[parent_hash]["children"].remove((action, None))
                self.tree[parent_hash]["children"].append((action, child_hash))
                # print(f"  Selecting child {child_hash} with action {str(action)}")
                return (parent_hash, child_hash)

            child = self.tree[child_hash]

            # UCB Comparison
            if child["ucb"] >= max_ucb and child_hash not in self.tree[parent_hash]["parents"]:
                max_ucb = child["ucb"]
                max_ucb_hash = child_hash
        return self.selection(max_ucb_hash)
    
    def expansion(self, parent_hash: str, child_hash: str):
        """
        Expand the tree by creating and adding a new child node to the parent node. The child node is created with its possible actions.

        Arguments:
        parent_hash -- the hash of the parent node
        child_hash -- the hash of the child node

        Returns:
        None
        """
        # Only create the child node if it does not already exist
        if child_hash not in self.tree:
            # Create the new child node with its possible actions and add to the tree
            is_red_turn = True if parent_hash in ["None", None] else not self.tree[parent_hash]["is_red_turn"]
            actions: list[Action] = find_possible_actions(self.unhash(child_hash), PlayerColor.RED if is_red_turn else PlayerColor.BLUE, 2)
            hashed_children = [(str(a), None) for a in actions]
            self.tree[child_hash] = {
                "wins": 0,
                "visits": 0,
                "ucb": 0,
                "children": hashed_children,
                "parents": [parent_hash],
                "is_red_turn": is_red_turn
            }
        else:
            # Add the parent to the existing child's list of parents
            self.tree[child_hash]["parents"].append(parent_hash)
        # self.print_tree()

    def simulation(self, child_hash: str, player: PlayerColor, minimax=False) -> float:
        """
        Simulate a game from the given child node until a terminal state is reached. Return the reward of the terminal state.

        Arguments:
            child_hash -- the hash of the child node
            player -- the player to simulate for

        Returns:
            The reward of the terminal state
            * 0.5 for a draw
            * 1 for a win
            * 0 for a loss
        """
        # Create a temporary board from the child node
        b = self.unhash(child_hash)
        temp_board = Board(b._state)
        temp_board._turn_color = PlayerColor.RED if self.tree[child_hash]["is_red_turn"] else PlayerColor.BLUE

        # Simulate play from that new state
        while not temp_board.game_over:
            # print(f"Game Over: {temp_board.game_over}")

            if minimax:
                # Using minimax agent for simulation
                minimaxAgent = MinimaxAgent(temp_board._turn_color)
                action, cost = minimaxAgent.minimax(temp_board, 3, True, float('-inf'), float('inf'))
            else:
                # Using random agent for simulation
                action = random.choice(find_possible_actions(temp_board, temp_board._turn_color, 2))
            
            # Apply the action to the temporary board
            temp_board.apply_action(action)
            # print(str(action))
            # print(temp_board.render())
        
        if temp_board.winner_color == None:
            # Draw
            return 0.5
        elif temp_board.winner_color == player:
            # Win
            return 1
        else:
            # Lost
            return 0
    
    def backpropagation(self, isWin: int, child_hash: str, visited: list[str]=[]):
        """
        Update the wins, visits and UCB of the child node and all its parents
        
        Use UCB1 formula for selection
        UCB = (num_wins / num_visits) + C * sqrt(log(parent.num_visits) / num_visits)
        
        Parameters
        ----------
        isWin : int
            1 if the player won, 0 otherwise
        child_hash : str
            hash of the child node
        new_action : Action
            action that led to the child node
        """
        if child_hash in visited:
            return
        # print(f"Backpropagating child {child_hash}, {visited}")
        # Update the wins, visits and UCB of the child node and all its parents
        # Use UCB1 formula for selection
        # UCB = (num_wins / num_visits) + C * sqrt(log(parent.num_visits) / num_visits)
        self.tree[child_hash]["wins"] += isWin
        self.tree[child_hash]["visits"] += 1
        visited.append(child_hash)

        # use the parent with maximum visits to calculate UCB of child
        parent_visits = 0
        if self.tree[child_hash]["parents"] != [None] and self.tree[child_hash]["parents"] != ["None"]:
            parent_visits = max([self.tree[parent_hash]["visits"] for parent_hash in self.tree[child_hash]["parents"]])
        
        self.tree[child_hash]["ucb"] = (self.tree[child_hash]["wins"] / self.tree[child_hash]["visits"]) + UCB_CONSTANT * (math.sqrt(math.log(parent_visits) / self.tree[child_hash]["visits"]) if parent_visits != 0 else 0)

        # update parent's wins, visits and backpropagate
        # print(f'parents: {self.tree[child_hash]["parents"]}')
        for parent_hash in self.tree[child_hash]["parents"]:
            # Root Node
            if parent_hash == None or parent_hash == "None":
                continue
            # Prevent infinite recursion if parent is a child of the current node
            # child_hashes = [c for (_, c) in self.tree[parent_hash]["parents"]]
            # print(child_hashes)
            # print(parent_hash)
            if parent_hash in visited:
                print("  recursive detected")
                continue

            # Update Parent's Wins and Visits
            # self.tree[parent_hash]["wins"] += isWin
            # self.tree[parent_hash]["visits"] += 1

            # Recursively backpropagate
            # self.print_tree()
            return self.backpropagation(isWin, parent_hash, visited)
        return
    
    
    def mcts(self, num_iterations: int, minimax=False, b: Board=Board()) -> Action:
        """
        Run monte-carlo tree search for the specified number of iterations. Return the best action given the current board.
        """
        # self.tree = get_tree_from_csv("test.csv")
        # Run MCTS for `num_iterations`
        for i in range(num_iterations):
            # print(f"\nMCTS Iteration {i}")
            parent_hash, child_hash = self.selection(self.hash(b))
            self.expansion(parent_hash, child_hash)
            # print(child_hash)
            isWin = self.simulation(child_hash, PlayerColor.RED, minimax)
            self.backpropagation(isWin, child_hash, [])
        # Find best action for current board
        parent_hash = self.hash(b)
        children = self.tree[parent_hash]["children"]
        # find for child with the highest win rate
        best_winrate = -1
        best_action = None
        for child_action, child_hash in children:
            if child_hash == None:
                continue
            curr_winrate = self.tree[child_hash]["wins"]/self.tree[child_hash]["visits"]
            if curr_winrate > best_winrate:
                best_winrate = curr_winrate
                best_action = child_action
        print(f"\nbest action: {best_action}, winrate: {best_winrate}")
        return self.unhash_action(best_action)

        # self.print_tree()

    def get_tree_from_csv(self, filename):
        """
        
        """
        tree = {}
        try:
            fp = open(filename, "r", newline="")
            reader = csv.DictReader(fp)

            # Converting string representation of children to list of tuples
            for row in reader:
                children = []
                for c in row["children"].strip("[]").split("), ("):
                    if "None" in c:
                        c = c.strip("()").replace("'", "")
                        action = c.strip(", None")
                        children.append((action, None))
                    else:
                        c = c.strip("()").split("', '")
                        c = [ele.replace("'", "") for ele in c]
                        children.append(tuple(c))
                tree[row["hash"]] = {
                    "wins": float(row["wins"]),
                    "visits": float(row["visits"]),
                    "ucb": float(row["ucb"]),
                    "children": children,
                    "parents": [p.strip("''") for p in row["parents"].strip("[]").split("', '")],
                    "is_red_turn": True if row["is_red_turn"] == "True" else False
                }
            fp.close()
        except FileNotFoundError:
            # Creating new tree
            print("File not found. Creating new tree.")
            fp = open(filename, "w", newline="")
            writer = csv.DictWriter(fp, fieldnames=["hash", "wins", "visits", "ucb", "children", "parents", "is_red_turn"])
            writer.writeheader()
            fp.close()
        return tree

    def save_tree_to_csv(self, tree, filename):
        """
        Save tree to csv file.

        Arguments:
            tree: dictionary representation of tree
            filename: name of csv file
        """
        fp = open(filename, "w", newline="")
        writer = csv.writer(fp)
        writer.writerow(["hash", "wins", "visits", "ucb", "children", "parents", "is_red_turn"])
        for key, value in self.tree.items():
            writer.writerow([key, value["wins"], value["visits"], value["ucb"], value["children"], value["parents"], value["is_red_turn"]])
        fp.close()


    