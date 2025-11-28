import os

import numpy as np
from numba import jit


@jit(nopython=True)
def floyd(dist, n):
    for k in range(n):
        for i in range(n):
            if dist[i][k] == np.inf:
                continue

            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    maxn = 1000
    dist = np.ones((maxn, maxn), dtype=np.int32) * np.inf
    indegree = np.zeros((maxn), dtype=np.int8)

    trim = 0
    infile.readline()
    for line in infile.readlines():
        i, line = line.split('->')
        j, cost = line.split(':')
        i, j, cost = int(i), int(j), int(cost)

        trim = max(trim, i, j)
        dist[i, j] = cost
        indegree[j] += 1

    trim += 1
    dist = dist[:trim, :trim]
    np.fill_diagonal(dist, 0)

    floyd(dist, trim)

    leaves = [i for i, val in enumerate(indegree == 1) if val]
    for i in dist[leaves, :][:, leaves]:
        for j in i:
            outfile.write(str(int(j)) + '\t')
        outfile.write('\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
