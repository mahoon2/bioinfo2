import os

import numpy as np


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    path = infile.readline().strip()
    infile.readline()
    states = infile.readline().strip().split()
    infile.readline()
    infile.readline()

    n = len(states)
    prob = np.ndarray((n, n), dtype=np.float32)
    for i in range(n):
        line = infile.readline().strip().split()[-n:]
        line = np.array(list(map(float, line)))
        prob[i] = line

    state_to_idx = {s: i for i, s in enumerate(states)}
    ret = np.prod([prob[state_to_idx[i]][state_to_idx[j]] for i, j in zip(path, path[1:])]) / 2
    outfile.write(f'{ret}\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
