# comp30027-infexion-project

* Running the program
```
python -m search < test.csv
```

## TODO
* [ ] [WJ] `find_red_coordinates()`
  * input:
    * `BoardState` current board state
  * output:
    * `list[(r, q)]` list of coordinates of red pieces
* [ ] [WJ] `find_possible_actions()`
  * input: 
    * `BoardState` current board state
    * `(r, q)` coordinate of piece to find actions of
  * output: 
    * `list[Action]` list of possible actions for red to take 
  * to be called for each red piece on board
* [ ] [XY] `update_board_state()`
  * input
    * `BoardState` current board state
    * `Action` action to be taken
  * output
    * `BoardState` updated board state (after action taken)
* [ ] [XY] `is_goal_reached()`
  * input
    * `BoardState` current board state
  * output
    * `boolean` true if goal reached, otherwise false
* [x] BFS 