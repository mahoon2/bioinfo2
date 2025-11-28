import os

import numpy as np


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    n = int(infile.readline())
    arr = np.zeros((n, n), dtype=np.float32)

    for i in range(n):
        arr[i] = np.array(list(map(float, infile.readline().split())), dtype=np.float32)

    idx_to_cluster = [i for i in range(n)]
    cluster_to_idx = [set([i]) for i in range(n)]

    for _ in range(n - 1):
        mindist = 987654321
        minc1, minc2 = -1, -1

        for c1 in range(len(cluster_to_idx)):
            idx1 = list(cluster_to_idx[c1])

            if len(idx1) == 0:
                continue

            for c2 in range(c1 + 1, len(cluster_to_idx)):
                idx2 = list(cluster_to_idx[c2])

                if len(idx2) == 0:
                    continue

                dist = np.mean(arr[idx1, :][:, idx2])

                if dist < mindist:
                    mindist = dist
                    minc1, minc2 = c1, c2

        outfile.write(' '.join([str(i + 1) for i in cluster_to_idx[minc1]]))
        outfile.write(' ')
        outfile.write(' '.join([str(i + 1) for i in cluster_to_idx[minc2]]))
        outfile.write('\n')

        cluster_to_idx[minc1] = cluster_to_idx[minc1].union(cluster_to_idx[minc2])
        cluster_to_idx[minc2] = set()

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
