# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

import heapq

from .utils import render_board, find_colour_coordinates, find_possible_actions, is_goal_reached, update_board_states
from .types import BoardState, Action
from .node import Node

def search(input: BoardState) -> list[Action]:
    """
    This is the entry point for your submission. The input is a dictionary
    of board cell states, where the keys are tuples of (r, q) coordinates, and
    the values are tuples of (p, k) cell states. The output should be a list of 
    actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    See the specification document for more details.
    """

    # The render_board function is useful for debugging -- it will print out a 
    # board state in a human-readable format. Try changing the ansi argument 
    # to True to see a colour-coded version (if your terminal supports it).
    # print(render_board(input, ansi=False))

    # Initialise tree with the first action
    tree: list[Node] = []
    heapq.heappush(tree, Node(input, [], 0))

    while True:
        # Check if tree is empty - goal state cannot be reached
        if len(tree) == 0:
            return []
        
        # Pop head of queue
        curr_node = heapq.heappop(tree)

        # Check if goal state is reached
        if is_goal_reached(curr_node.state):
            return curr_node.actions

        # Find all red coordinates and the possible actions that red can take
        for red_coor in find_colour_coordinates(curr_node.state, "r"):
            for action in find_possible_actions(curr_node.state, red_coor):
                updated_board_state = update_board_states(curr_node.state, action)
                new_node = Node(updated_board_state, curr_node.actions.copy(), curr_node.cost + 1)
                new_node.actions.append(action)
                heapq.heappush(tree, new_node)
