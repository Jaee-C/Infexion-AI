from enum import Enum

from referee.game.actions import Action

'''
Constants representing the different flags for a transposition table entry,
which determine what kind of entry it is. If the entry has a score from
a fail-low node (alpha wasn't raised), it's an alpha entry. If the entry has
a score from a fail-high node (a beta cutoff occured), it's a beta entry. And
if the entry has an exact score (alpha was raised), it's an exact entry.
'''
class EntryFlag(Enum):
    EXACT = 0
    ALPHA = 1
    BETA  = 2

class TableEntry():
    def __init__(self, best: Action, score: int, flag: EntryFlag, depth: int):
        self.move: Action = best
        self.score: int = score
        self.flag: EntryFlag = flag
        self.depth = depth


class Transposition:
    def __init__(self):
        self._table: dict[str, TableEntry] = {}

    def find(self, hash: str, depth: int, alpha: int, beta: int) -> tuple[int, bool, Action]:
        if hash not in self._table.keys():
            return 0, False, None
        
        entry = self._table[hash]
        shouldUse = False
        best_move = entry.move
        adjusted_score = entry.score

        # To be able to get an accurate value from this entry, the results of 
        # this entry must be from a search that is equal or greater than
        # the current depth of our search.
        if entry.depth < depth:
            return adjusted_score, False, best_move

        score = entry.score
        if entry.flag == EntryFlag.EXACT:
            # If we have an exact entry, we can used the saved score
            shouldUse = True
        elif entry.flag == EntryFlag.ALPHA and score <= alpha:
            # We know that our current alpha is the best score we can get in 
            # this node
            adjusted_score = alpha
            shouldUse = True
        elif entry.flag == EntryFlag.BETA and score >= beta:
            # While searching this node previously, we found a value greater
            # than the current beta. We have a beta-cutoff.
            adjusted_score = beta
            shouldUse = True

        print(adjusted_score, shouldUse, best_move)

        return adjusted_score, shouldUse, best_move

    def store(self, hash: str, score: int, move: Action, depth: int, alpha: int, beta: int):
        tt_flag = None

        if score <= alpha:
            # Node is alpha-pruned, actual score is less than or equal to score
            tt_flag = EntryFlag.ALPHA
        elif score >= beta:
            # Node is beta-pruned, actual score is greater or equal to score
            tt_flag = EntryFlag.BETA
        else:
            tt_flag = EntryFlag.EXACT

        new_entry = TableEntry(move, score, tt_flag, depth)
        self._table[hash] = new_entry

    def clear(self):
        self._table = {}
