# comp30027-infexion-project

* Running the program
```
python -m search < test.csv
```

## TODO
### Initial Functions with Uninformed Search (BFS)
* [x] [WJ] `find_red_coordinates()`
  * input:
    * `BoardState` current board state
  * output:
    * `list[(r, q)]` list of coordinates of red pieces
* [x] [WJ] `find_possible_actions()`
  * input: 
    * `BoardState` current board state
    * `(r, q)` coordinate of piece to find actions of
  * output: 
    * `list[Action]` list of possible actions for red to take 
  * to be called for each red piece on board
* [x] [XY] `update_board_state()`
  * input
    * `BoardState` current board state
    * `Action` action to be taken
  * output
    * `BoardState` updated board state (after action taken)
* [x] [XY] `is_goal_reached()`
  * input
    * `BoardState` current board state
  * output
    * `boolean` true if goal reached, otherwise false
* [x] BFS 

### Using Informed Search (A*)
* [x] [WJ] Update `search()` with `heapq` and `A*`
  * insert nodes into min heap based on estimated cost
* [x] `evaluation_function()`
  * $f(x) = c(x) + d(x) + 2*b(x)$
  * $c(x)$ cost to current node
  * [x] [XY] $d(x)$ `distance_to_blues()`
    * minimum manhattan distance between red and blue cells within the current board
  * [x] [XY] $b(x)$
    * current blue power

> * idea for future: travelling salesman
>   * each red going to multiple blue (path)

## Testing

`test1.csv`: Wrap around - 2 moves
`test2.csv`: Capture in reverse direction first - 3 moves
`test3.csv`: 6 equidistant, with only one optimal move - 1 move
`test4.csv`: 3 moves
`test5.csv`: Another wrap around - 2 moves
`test6.csv`: Go through a path - 6 moves
`test7.csv`: very sparse - 4 moves
  - Weakness of our heuristic: if graph is sparse, and we are not making much captures, search devolves into a BFS
