import os

import numpy as np
from scipy.spatial.distance import euclidean


def dist(x, y):
    assert x.shape == y.shape
    return euclidean(x, y)


def expectation(mat, centers, points, stiff):
    for i, center in enumerate(centers):
        temp = np.array([(-stiff) * dist(center, point) for point in points], dtype=np.float32)
        mat[i] = np.exp(temp)

    for j in range(len(points)):
        mat[:, j] /= mat[:, j].sum()

    return mat


def maximization(centers, mat, points):
    centers = np.matmul(mat, points)
    for i in range(len(centers)):
        centers[i] /= np.sum(mat[i])
    return centers


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    k, m = list(map(int, infile.readline().split()))
    stiff = float(infile.readline())
    points = []
    for line in infile.readlines():
        points.append([float(x) for x in line.split()])
    points = np.array(points, dtype=np.float32)

    mat = np.zeros((k, len(points)), dtype=np.float32)
    centers = points[:k]

    for _ in range(100):
        mat = expectation(mat, centers, points, stiff)
        centers = maximization(centers, mat, points)

    for center in centers:
        outfile.write(' '.join(map(str, map(lambda l: round(l, 3), center))) + '\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
