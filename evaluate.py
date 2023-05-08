import subprocess

# Run multiple games between red and blue
red_wins = 0
blue_wins = 0
total_num_moves = 0
NUM_GAMES = 100

for i in range(NUM_GAMES):
    print(f"Game {i}")
    num_moves = 0
    # Create a child subprocess that runs the referee
    p = subprocess.Popen("python -m referee agent agent -c", shell="True", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        line = line.decode("utf-8") 
        print(line, end="")
        if "game board" in line:
            num_moves += 1
        if "winner" in line:
            if "BLUE" in line:
                blue_wins += 1
                print(f"  BLUE won, num_moves: {num_moves}")
            else:
                red_wins += 1
                print(f"  RED won, num_moves: {num_moves}")
    total_num_moves += num_moves

print(f"Num RED Wins: {red_wins} - win percentage: {red_wins/NUM_GAMES * 100:.2f}")
print(f"Num BLUE wins: {blue_wins} - win percentage: {blue_wins/NUM_GAMES * 100:.2f}")
print(f"Average number of moves per game: {total_num_moves/NUM_GAMES:.2f}")