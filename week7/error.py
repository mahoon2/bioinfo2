import os

import numpy as np


def mindist(point, centers):
    return np.min([np.sum(np.square(point - center)) for center in centers])


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    k, m = list(map(int, infile.readline().split()))
    centers = []
    while True:
        line = infile.readline()

        if line.startswith('-'):
            break

        centers.append([float(x) for x in line.split()])
    centers = np.array(centers, dtype=np.float32)

    points = []
    for line in infile.readlines():
        points.append([float(x) for x in line.split()])
    points = np.array(points, dtype=np.float32)

    outfile.write(str(np.round(np.mean([mindist(point, centers) for point in points]), 3)) + '\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
