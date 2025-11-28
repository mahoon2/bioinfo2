import os

import numpy as np


def dist(x, y):
    assert x.shape == y.shape
    return np.sum(np.square(x - y))


def centers_to_cluster(centers, points):
    label = np.zeros(len(points), dtype=np.int32)

    for i, point in enumerate(points):
        label[i] = np.argmin([dist(point, center) for center in centers])

    return label


def clusters_to_center(label, points, k, m):
    sets = [list() for _ in range(k)]

    for i, d in enumerate(label):
        sets[d].append(points[i])

    centers = np.zeros(shape=(k, m), dtype=np.float32)
    for i, s in enumerate(sets):
        centers[i] = np.mean(s, axis=0)

    return centers


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    k, m = list(map(int, infile.readline().split()))
    points = []
    for line in infile.readlines():
        points.append([float(x) for x in line.split()])
    points = np.array(points, dtype=np.float32)

    centers = points[:k]

    while True:
        prev_centers = np.array([center.copy() for center in centers])

        label = centers_to_cluster(centers, points)
        centers = clusters_to_center(label, points, k, m)

        if np.sum(np.abs(prev_centers - centers)) < 0.0001:
            break

    for center in centers:
        outfile.write(' '.join(map(str, np.round(center, 3))) + '\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
