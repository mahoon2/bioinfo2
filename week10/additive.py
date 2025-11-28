import os

import numpy as np
from numba import jit


@jit(nopython=True)
def limb(D, j) -> tuple[int, tuple[int, int]]:
    ret = np.inf
    pair = (-1, -1)

    for i in range(j):
        for k in range(i + 1, j):
            dist = (D[i, j] + D[j, k] - D[i, k]) / 2
            if dist < ret:
                ret = dist
                pair = (i, k)

    return int(ret), pair


def dfs(here, end, dist, visited, adj):
    if here == end:
        return [(end, dist)]

    for there, weight in adj[here]:
        if not visited[there]:
            visited[there] = True
            ret = dfs(there, end, dist + weight, visited, adj)

            if ret is not None:
                return ret + [(here, dist)]


def find_insert_point(start, end, dist, adj):
    """
    Perform DFS from start to end, returns an edge to be splitted.
    New internal node (or an existing one) will be the parent of the caller node.
    """
    path = dfs(start, end, 0, [False for _ in range(len(adj))], adj)
    path = path[::-1]

    for i in range(1, len(path)):
        if path[i][1] > dist:
            return (
                path[i - 1][0],  # Start node
                path[i][0],  # End node
                path[i][1] - path[i - 1][1],  # Edge weight
                path[i - 1][1],  # Cumulative sum of weights
            )
        elif path[i][1] == dist:
            return (path[i][0],)  # Use this existing internal node


def additive_phylogeny(D, n):
    """
    @param n: n-th leaf (1-based indexing)
    """
    global counter

    # Base case: only two nodes connected with one edge
    if n == 2:
        ret = [[] for _ in range(D.shape[0])]
        ret[0].append((1, D[0, 1]))
        ret[1].append((0, D[1, 0]))
        return ret

    # Find limb length and corresponding (i, k) nodes
    limblen, (i, k) = limb(D, n - 1)

    # Assume limb length 0
    D[n - 1, :n] -= limblen
    D[:n, n - 1] -= limblen
    D[n - 1, n - 1] = 0

    ret = additive_phylogeny(D, n - 1)

    # Restore limb length
    D[n - 1, :n] += limblen
    D[:n, n - 1] += limblen
    D[n - 1, n - 1] = 0

    nodes = find_insert_point(i, k, D[i, n - 1] - limblen, ret)

    # Use an exisiting internal node to attach leaf `n`
    if len(nodes) == 1:
        node = nodes[0]
        ret[node].append((n, limblen))
        ret[n].append((node, limblen))
    # Create a new internal node instead by splitting existing edge
    else:
        (prev, next, edgeweight, cumweight) = nodes
        ret[prev].remove((next, edgeweight))
        ret[next].remove((prev, edgeweight))

        newnode = next(counter)

        ret.append([])

        ret[n - 1].append((newnode, limblen))
        ret[newnode].append((n - 1, limblen))

        forwarddist = D[i, n - 1] - limblen - cumweight
        ret[prev].append((newnode, forwarddist))
        ret[newnode].append((prev, forwarddist))

        backwarddist = edgeweight - forwarddist
        ret[next].append((newnode, backwarddist))
        ret[newnode].append((next, backwarddist))

    return ret


counter = None


def main():
    from itertools import count

    global counter

    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    n = int(infile.readline())
    counter = count(n)
    dist = np.ndarray((n, n), dtype=np.int32)
    for i in range(n):
        line = map(int, infile.readline().split())
        dist[i] = np.array(list(line))

    ret = additive_phylogeny(dist, n)

    for i, adj in enumerate(ret):
        for j, weight in adj:
            outfile.write(f'{i}->{j}:{weight}\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
