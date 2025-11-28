import os

import numpy as np


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    string = infile.readline().strip()
    infile.readline()
    letters = infile.readline().strip().split()
    infile.readline()
    path = infile.readline().strip()
    infile.readline()
    states = infile.readline().strip().split()
    infile.readline()
    infile.readline()

    n = len(states)
    m = len(letters)
    prob = np.ndarray((n, m), dtype=np.float32)
    for i in range(n):
        line = infile.readline().strip().split()[-m:]
        line = np.array(list(map(float, line)))
        prob[i] = line

    state_to_idx = {s: i for i, s in enumerate(states)}
    letter_to_idx = {s: i for i, s in enumerate(letters)}
    ret = np.prod([prob[state_to_idx[i]][letter_to_idx[j]] for i, j in zip(path, string)])
    outfile.write(f'{ret}\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
