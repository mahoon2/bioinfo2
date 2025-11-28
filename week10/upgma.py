import os

import numpy as np


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    n = int(infile.readline())
    D = np.zeros((n, n), dtype=np.float32)

    for i in range(n):
        D[i] = np.array(list(map(float, infile.readline().split())), dtype=np.float32)

    graph = [[] for _ in range(2 * n - 1)]
    parent = [i for i in range(2 * n - 1)]
    age = np.zeros(2 * n - 1, dtype=np.float32)
    idx_to_cluster = [i for i in range(n)]
    cluster_to_idx = [set([i]) for i in range(n)]
    counter = n

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

                dist = np.mean(D[idx1, :][:, idx2])

                if dist < mindist:
                    mindist = dist
                    minc1, minc2 = c1, c2

        p1 = parent[minc1]  # The closest parent of c1 to root
        p2 = parent[minc2]  # The closest parent of c2 to root

        mindist /= 2
        # Add internal node `counter`
        graph[p1].append((counter, mindist - age[p1]))
        graph[p2].append((counter, mindist - age[p2]))
        graph[counter].extend([(p1, mindist - age[p1]), (p2, mindist - age[p2])])

        # Now `counter` becomes the closest parent of c1 and c2 to root
        parent[minc1] = counter
        parent[minc2] = counter

        age[counter] = mindist

        print(f'{minc1}, {p1} and {minc2}, {p2} merged with {counter}, dist {mindist}')
        counter += 1

        cluster_to_idx[minc1] = cluster_to_idx[minc1].union(cluster_to_idx[minc2])
        cluster_to_idx[minc2] = set()

    for i, adj in enumerate(graph):
        for j, weight in adj:
            outfile.write(f'{i}->{j}:{weight:.3f}\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
