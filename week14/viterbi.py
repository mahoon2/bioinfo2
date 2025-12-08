import os

import numpy as np


def solve(indices, transition, emission):
    n = len(transition)
    m = len(indices)
    dp = np.zeros((n, m), dtype=np.float32)
    back = np.zeros((n, m), dtype=np.int32)

    transition = np.log(transition)
    emission = np.log(emission)

    # How can I compute transition probability from source to the very first state?
    for i in range(0, n):
        dp[i][0] = np.log(1 / n) + emission[i][indices[0]]

    for j in range(1, m):
        for i in range(0, n):
            edges = [dp[k][j - 1] + transition[k][i] + emission[i][indices[j]] for k in range(0, n)]
            dp[i][j] = np.max(edges)
            back[i][j] = np.argmax(edges)

    return dp, back


def backtrack(dp, back):
    j = len(dp[0]) - 1
    i = np.argmax(dp[:][-1])
    path = []

    while j >= 0:
        path.append(i)
        i = back[i][j]
        j -= 1

    return path[::-1]


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
    transition = np.ndarray((n, n), dtype=np.float32)
    for i in range(n):
        line = infile.readline().strip().split()[-n:]
        line = np.array(list(map(float, line)))
        transition[i] = line

    infile.readline()
    infile.readline()
    emission = np.ndarray((n, m), dtype=np.float32)
    for i in range(n):
        line = infile.readline().strip().split()[-m:]
        line = np.array(list(map(float, line)))
        emission[i] = line

    state_to_idx = {s: i for i, s in enumerate(states)}
    letter_to_idx = {s: i for i, s in enumerate(letters)}

    stringidx = [letter_to_idx[c] for c in string]
    dp, back = solve(stringidx, transition, emission)
    path = backtrack(dp, back)
    outfile.write(f'{"".join(str(states[idx]) for idx in path)}\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
