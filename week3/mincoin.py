import os
import sys
from functools import lru_cache

import numpy as np

coins = []
sys.setrecursionlimit(20000000)


@lru_cache(maxsize=1_000_000)
def solve(money: int) -> int:
    if money <= 0:
        return 0

    if money in coins:
        return 1

    return np.min([solve(money - c) + 1 for c in coins if money - c >= 0])


def main():
    global coins

    infile = open('../test.in', 'r')
    outfile = open(os.path.basename(__file__).replace('py', 'out'), 'w')

    money = int(infile.readline().strip())
    coins = tuple(map(int, infile.readline().strip().split(',')))

    outfile.write(str(solve(money)))

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
