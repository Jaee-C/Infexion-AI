* `python -m referee agent agent`
* `python -m referee --help`

ToDos (24/4)
- [ ] `update_board_state(b: BoardState)` Update board state after every turn -- Heavy inspo from `referee.game.Board`
- [ ] Implement Minimax
    - [ ] `terminal_test(b: BoardState) -> bool` check if game has ended -- Use Board.winner_color()
    - [ ] [XY] `find_possible_actions(b: BoardState) -> list[Action]` Find all possible actions from current state (SPREAD/SPAWN)optimizing minimax algorithm
      - [ ] [WJ]`find_spread_actions(b: BoardState) -> list[Action]`
        - migrate from part A
      - [ ] [XY] `find_spawn_actions(b: BoardState) -> list[Action]`
        - start with only returning 1 spawn action (first available spawn position)
        - think about best spawn positions
        - we probably don't want to generate all spawn actions as it would be bad for branching factor
    - [ ] [XY] `evaluate_value(b: BoardState) -> int` Cost function (prev eval function?)
        - Number of blue remaining
        - number of red - blue
        - Note: function only needs to show ordering of states (which is better which is worse), does not need to be admissible
    - [ ] determine max tree depth
      - 3 for now
    - [ ] [WJ] `minimax(b: BoardState, depth:int, is_max:bool) -> (Action, Cost)`
        ```py3
        def minimax(b:BoardState, depth:int, is_max:bool) -> (Action, Cost):
            if depth == 0:
                return null, evaluate_value(b)
            if (winner=terminal_test(b)):
                return null, INF if winner == Agent.color else -INF # pos or neg depending on ismax or not

            curr_max = -INF
            curr_min = INF
            best_action = null
            for action in find_possible_actions():
                b.apply_action(action)
                _, val = minimax(b, depth-1, not is_max)
                if is_max:
                    curr_max = max(val, curr_max)
                    best_action = action
                else:
                    curr_min = min(val, curr_min)
                    best_action = action
                b.undo_action()
            
            if is_max:
                cost = curr_max
            else:
                const = curr_min
            return best_action, cost
        ```

- [ ] alpha-beta pruning

Next Steps: Monte-Carlo Tree search

```py3
function Minimax-Decision(game) returns an operator
  for each op in Operators[game] do
  	Value[op] ← Minimax-Value(Apply(op, game), game)
  end
  return the op with the highest Value[op]

function Minimax-Value(state, game) returns a utility value
  if Terminal-Test[game](state) then
  	return Utility[game](state)
  else if max is to move in state then
  	return the highest Minimax-Value of Successors(state)
  else
  	return the lowest Minimax-Value of Successors(state)
```
