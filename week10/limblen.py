import os

import numpy as np


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    N = int(infile.readline())
    j = int(infile.readline())

    dist = np.ndarray((N, N), dtype=np.int32)
    for i in range(N):
        line = map(int, infile.readline().split())
        dist[i] = np.array(list(line))

    ret = np.inf
    for i in range(N):
        if i == j:
            continue

        for k in range(i + 1, N):
            if k == j:
                continue

            ret = min(ret, (dist[i, j] + dist[j, k] - dist[i, k]) / 2)
    outfile.write(str(int(ret)) + '\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
