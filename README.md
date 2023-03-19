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
* [ ] [WJ] Update `search()` with `heapq` and `A*`
  * insert nodes into min heap based on estimated cost
* [ ] `evaluation_function()`
  * $f(x) = c(x) + d(x) + r(x)$
  * $c(x)$ cost to current node
  * [x] [XY] $d(x)$ `distance_to_blues()`
    * minimum manhattan distance between red and blue cells within the current board
  * [ ] [WJ] $r(x)$ `red_power()`
    * current red power

> * idea for future: travelling salesman
>   * each red going to multiple blue (path)
