import os

import numpy as np


def transform(D, n, nodes):
    totaldist = D.sum(axis=0)
    ret = np.copy(D)
    ret *= n - 2

    for i in nodes:
        for j in nodes:
            if i == j:
                ret[i, j] = 0
            else:
                ret[i, j] = ret[i, j] - totaldist[i] - totaldist[j]

    return ret


def neighbor_joining(D, n, nodes) -> list:
    """
    The neighbor joining algorithm.

    :param D: 2D array with all diagonal elements are zero.
    :param n: Number of nodes, which diminishes from N to 2.
    :param nodes: Indices of nodes.
    """
    try:
        assert (D == D.T).all()
        assert len(nodes) == n
    except AssertionError:
        print(n)
        print(D)
        print(nodes)

    # Base case: there is only two nodes.
    if n == 2:
        return [
            (nodes[0], nodes[1], D[nodes[0], nodes[1]]),
            (nodes[1], nodes[0], D[nodes[1], nodes[0]]),
        ]

    nD = transform(D, n, nodes)
    mask = np.ma.masked_equal(nD, 0)
    i, j = np.unravel_index(mask.argmin(), mask.shape)

    newnode = nodes[-1] + 1
    nodes = nodes[(nodes != i) & (nodes != j)]

    for k in nodes:
        D[newnode, k] = D[k, newnode] = (D[k, i] + D[k, j] - D[i, j]) / 2
    nodes = np.append(nodes, newnode)

    delta = (D[i].sum() - D[j].sum()) / (n - 2)
    edgei = (D[i, j] + delta) / 2
    edgej = (D[i, j] - delta) / 2

    D[i, :] = D[:, i] = D[j, :] = D[:, j] = 0
    ret = neighbor_joining(D, n - 1, nodes)
    ret.extend([(i, newnode, edgei), (newnode, i, edgei), (j, newnode, edgej), (newnode, j, edgej)])

    return ret


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    n = int(infile.readline())
    D = np.zeros((2 * n - 1, 2 * n - 1), dtype=np.float32)
    for i, line in enumerate(infile.readlines()):
        for j, d in enumerate(map(float, line.split())):
            D[i, j] = d

    ret = neighbor_joining(D, n, np.array([i for i in range(n)]))
    ret.sort()
    for i, j, weight in ret:
        outfile.write(f'{i}->{j}:{weight:.3f}\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
