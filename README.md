# comp30027-infexion-project

- Running the program

```
python -m search < test.csv
```

## TODO

### Initial Functions with Uninformed Search (BFS)

- [x] [WJ] `find_red_coordinates()`
  - input:
    - `BoardState` current board state
  - output:
    - `list[(r, q)]` list of coordinates of red pieces
- [x] [WJ] `find_possible_actions()`
  - input:
    - `BoardState` current board state
    - `(r, q)` coordinate of piece to find actions of
  - output:
    - `list[Action]` list of possible actions for red to take
  - to be called for each red piece on board
- [x] [XY] `update_board_state()`
  - input
    - `BoardState` current board state
    - `Action` action to be taken
  - output
    - `BoardState` updated board state (after action taken)
- [x] [XY] `is_goal_reached()`
  - input
    - `BoardState` current board state
  - output
    - `boolean` true if goal reached, otherwise false
- [x] BFS

### Using Informed Search (A\*)

- [x] [WJ] Update `search()` with `heapq` and `A*`
  - insert nodes into min heap based on estimated cost
- [x] `evaluation_function()`
  - $f(x) = c(x) + d(x) + 2*b(x)$
  - $c(x)$ cost to current node
  - [x] [XY] $d(x)$ `distance_to_blues()`
    - minimum manhattan distance between red and blue cells within the current board
  - [x] [XY] $b(x)$
    - current blue power

> - idea for future: travelling salesman
>   - each red going to multiple blue (path)

## Testing

`test1.csv`: Wrap around - 2 moves
`test2.csv`: Capture in reverse direction first - 3 moves
`test3.csv`: 6 equidistant, with only one optimal move - 1 move
`test4.csv`: 3 moves
`test5.csv`: Another wrap around - 2 moves
`test6.csv`: Go through a path - 6 moves
`test7.csv`: very sparse - 4 moves

- Weakness of our heuristic: if graph is sparse, and we are not making much captures, search devolves into a BFS

## Heuristic Testing

- run tester using `py tester.py`
- `self.cost + get_distance(self.state)`
  - output in [`./tests/results/out1.txt`](./tests/results/out1.txt)
  ```
  ----------------------gs_test1.csv
  Nodes visited: 23, Cost: 5
  ----------------------gs_test2.csv
  Nodes visited: 26, Cost: 3
  ----------------------test1.csv
  Nodes visited: 3, Cost: 2
  ----------------------test2.csv
  Nodes visited: 7, Cost: 3
  ----------------------test3.csv
  Nodes visited: 2, Cost: 1
  ----------------------test4.csv
  Nodes visited: 6, Cost: 3
  ----------------------test5.csv
  Nodes visited: 4, Cost: 2
  ----------------------test6.csv
  Nodes visited: 30, Cost: 6
  ----------------------test7.csv
  Nodes visited: 52, Cost: 5
  ```
- `self.cost + get_distance(self.state) - get_colour_power(self.state, "r")`
- - output in [`./tests/results/out2.txt`](./tests/results/out2.txt)
  ```
  ----------------------gs_test1.csv
  Nodes visited: 17, Cost: 5
  ----------------------gs_test2.csv
  Nodes visited: 12, Cost: 3
  ----------------------test1.csv
  Nodes visited: 3, Cost: 2
  ----------------------test2.csv
  Nodes visited: 6, Cost: 4
  ----------------------test3.csv
  Nodes visited: 2, Cost: 1
  ----------------------test4.csv
  Nodes visited: 4, Cost: 3
  ----------------------test5.csv
  Nodes visited: 3, Cost: 2
  ----------------------test6.csv
  Nodes visited: 7, Cost: 6
  ----------------------test7.csv
  Nodes visited: 49, Cost: 5
  ```
  - Other Heuristic Function we thought about
    ```py
        # return self.cost + len(find_colour_coordinates(self.state, "b"))
        # return self.cost + get_distance(self.state) + 2*get_colour_power(self.state, "b")
    ```
