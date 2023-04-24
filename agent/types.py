from referee.game.hex import HexPos

# BoardState:
# - key: coordinate - (HexPos)
# - value: cell state - (color, power)
BoardState = dict[HexPos, tuple]
