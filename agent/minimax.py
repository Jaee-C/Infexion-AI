from argparse import Action
from .board import Board
from .transposition import Transposition
from .utils import find_possible_actions
from referee.game.player import PlayerColor

class MinimaxAgent():
    def __init__(self, color: PlayerColor, eval_func: str="eval_func1") -> None:
        self._color = color
        self._state: Board = Board()
        self.transposition_table = Transposition()
        self.opponent = PlayerColor.RED if color == PlayerColor.BLUE else PlayerColor.BLUE
        self.eval_func: str = eval_func

    def evaluate_value(self, b: Board) -> int:
        """
        Evaluate the value of the board for the agent using the difference in power.

        Args:
            b (Board): The board to evaluate

        Returns:
            int: The value of the board for the agent.

        Example:
            If the agent is red, the value is
                red power - blue power
        """
        power = 0
        for cell in b._state:
            if b[cell].power > 0:
                if b[cell].player == self._color:
                    power += b[cell].power
                else:
                    power -= b[cell].power
        return power
    
    def evaluate_value2(self, b: Board) -> int:
        """
        Evaluate the value of the board for the agent using the difference in power and the difference in number of cells.

        Args:
            b (Board): The board to evaluate

        Returns:
            int: The value of the board for the agent.

        Example:
            If the agent is red, the value is
                (red power - blue power) + (red cells - blue cells)
        """
        power = 0
        for cell in b._state:
            if b[cell].power > 0:
                if b[cell].player == self._color:
                    power += b[cell].power
                else:
                    power -= b[cell].power
        power += (len(b._player_cells(self._color)) - len(b._player_cells(self.opponent)))
        return power

    def minimax(self, b: Board, depth: int, is_max: bool, alpha: int, beta: int) -> tuple[Action, int]:
        """
        Minimax algorithm with alpha-beta pruning.

        Args:
            b (Board): The board to evaluate
            depth (int): The depth of the search tree
            is_max (bool): Whether the current node is a max node or not
            alpha (int): The alpha value
            beta (int): The beta value

        Returns:
            tuple[Action, int]: The best action and the evaluated value/cost of the board
        """
        if depth == 0:
            if self.eval_func == "eval_func1":
                return None, self.evaluate_value(b)
            return None, self.evaluate_value2(b)
        if b.game_over:
            winner = b.winner_color
            # pos or neg depending on ismax or not
            if winner == self._color:
                return None, float('inf')
            else:
                return None, float('-inf')
        
        alpha_org = alpha
        beta_org = beta
        b_hash = b.get_hash()

        # Probe the transposition table to see if we have a useable matching
        # entry from the current position. If we get a hit, return the score
        # and stop searching.
        tt_score, should_use, best_move = self.transposition_table.find(b_hash, depth, alpha, beta)

        # If we got a hit, return the score and stop searching
        if should_use:
            return best_move, tt_score

        # If we didn't get a hit, generate all possible actions from that board state
        colour = self._color if is_max else self._color.opponent
        curr_max = float('-inf')
        curr_min = float('inf')
        all_actions = find_possible_actions(b, colour)

        # Find the best action and the cost of that action
        best_action = all_actions[0]
        for action in all_actions:
            # Apply the action to the board and recursively call minimax to find the cost
            b.apply_action(action)
            _, val = self.minimax(b, depth-1, not is_max, alpha, beta)

            # Compare the cost to the current max/min and update if necessary
            if is_max and val > curr_max:
                curr_max = val
                best_action = action
                alpha = max(alpha, curr_max)
            elif not is_max and val < curr_min:
                curr_min = val
                best_action = action
                beta = min(beta, curr_min)

            # Undo the action and check if we can prune
            if beta <= alpha:
                b.undo_action()
                break
            b.undo_action()

        # Store the best action and cost in the transposition table
        if is_max:
            cost = curr_max
        else:
            cost = curr_min
        b_hash = self._state.get_hash()
        self.transposition_table.store(b_hash, cost, best_action, depth, alpha_org, beta_org)
        
        return best_action, cost
