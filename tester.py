from search.__main__ import parse_input, print_sequence
from search.program import search
import sys

orig_stdout = sys.stdout
f = open('./tests/results/out2b.txt', 'w')
sys.stdout = f

FILEPATH_PREFIX = './tests/'
for file in ['gs_test1.csv', 'gs_test2.csv', 'test1.csv', 'test2.csv', 'test3.csv', 'test4.csv', 'test5.csv', 'test6.csv', 'test7.csv']:
    with open(f"{FILEPATH_PREFIX}{file}", 'r') as f:
        print(f"----------------------{file}")
        input = parse_input(f.read())
        sequence: list[tuple] = search(input, 2)
        # print_sequence(sequence)

sys.stdout = orig_stdout
f.close()