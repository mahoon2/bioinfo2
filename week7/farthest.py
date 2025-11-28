import os

import numpy as np


def mindist(point, centers):
    return np.min([np.sum(np.square(point - center)) for center in centers])


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    k, m = list(map(int, infile.readline().split()))
    points = []
    for line in infile.readlines():
        points.append([float(x) for x in line.split()])
    nppoints = np.array(points, dtype=np.float32)

    selected = [False for _ in range(len(points))]
    selected[0] = True
    npcenters = [nppoints[0]]

    k -= 1
    while k > 0:
        k -= 1

        maxdist = 0
        maxpoint = -1
        for i in range(len(points)):
            if selected[i]:
                continue

            dist = mindist(nppoints[i], npcenters)
            if maxdist < dist:
                maxdist = dist
                maxpoint = i

        selected[maxpoint] = True
        npcenters.append(nppoints[maxpoint])

    for i in range(len(points)):
        if selected[i]:
            outfile.write(' '.join(list(map(str, points[i]))) + '\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
