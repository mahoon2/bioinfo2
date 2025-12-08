import os

import numpy as np


def solve(indices, transition, emission):
    n = len(transition)
    m = len(indices)
    dp = np.zeros((n, m), dtype=np.float64)

    for i in range(0, n):
        dp[i][0] = (1 / n) * emission[i][indices[0]]

    for j in range(1, m):
        for i in range(0, n):
            edges = [
                np.prod([dp[k][j - 1], transition[k][i], emission[i][indices[j]]])
                for k in range(0, n)
            ]
            dp[i][j] = np.sum(edges)

    return dp[:, -1].sum()


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    string = infile.readline().strip()
    infile.readline()
    letters = infile.readline().strip().split()
    infile.readline()
    states = infile.readline().strip().split()
    infile.readline()
    infile.readline()

    n = len(states)
    m = len(letters)
    transition = np.ndarray((n, n), dtype=np.float64)
    for i in range(n):
        line = infile.readline().strip().split()[-n:]
        line = np.array(list(map(float, line)))
        transition[i] = line

    infile.readline()
    infile.readline()
    emission = np.ndarray((n, m), dtype=np.float64)
    for i in range(n):
        line = infile.readline().strip().split()[-m:]
        line = np.array(list(map(float, line)))
        emission[i] = line

    state_to_idx = {s: i for i, s in enumerate(states)}
    letter_to_idx = {s: i for i, s in enumerate(letters)}

    stringidx = [letter_to_idx[c] for c in string]
    ret = solve(stringidx, transition, emission)
    outfile.write(f'{ret}\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
