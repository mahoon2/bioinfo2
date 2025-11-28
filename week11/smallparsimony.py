import os

import numpy as np


def char_to_idx(c):
    if c == 'A':
        return 0
    if c == 'C':
        return 1
    if c == 'G':
        return 2
    if c == 'T':
        return 3

    raise ValueError


def idx_to_char(i):
    if i == 0:
        return 'A'
    if i == 1:
        return 'C'
    if i == 2:
        return 'G'
    if i == 3:
        return 'T'

    raise ValueError


def hamming(a, b):
    return np.sum([ca != cb for ca, cb in zip(a, b)])


def parsimony(n, chars, adj, parent):
    """
    :param n: Total number of nodes.
    :param chars: List of single characters. Internal nodes have blank character.
    :param adj: Adjacency list.
    """

    score = np.ones((n, 4), dtype=np.int32) * np.inf
    backtrack = np.zeros((n, 2, 4), dtype=np.int32)

    for i in range(n):
        if len(adj[i]) == 0:  # i is a leaf node
            idx = char_to_idx(chars[i])
            score[i][idx] = 0
        else:
            assert len(adj[i]) == 2

            left, right = adj[i][0], adj[i][1]
            for idx in range(4):
                leftscore = [
                    score[left][idx1] + 1 if idx1 != idx else score[left][idx1] for idx1 in range(4)
                ]
                rightscore = [
                    score[right][idx2] + 1 if idx2 != idx else score[right][idx2]
                    for idx2 in range(4)
                ]

                score[i][idx] = np.min(leftscore) + np.min(rightscore)
                backtrack[i][0][idx] = np.argmin(leftscore)
                backtrack[i][1][idx] = np.argmin(rightscore)

    chars[-1] = idx_to_char(np.argmin(score[-1]))
    for i in range(n - 2, -1, -1):
        p = parent[i]
        idx = char_to_idx(chars[p])

        if adj[p][0] == i:
            pos = 0
        else:
            pos = 1

        cidx = backtrack[p][pos][idx]
        chars[i] = idx_to_char(cidx)

    return chars, int(np.min(score[-1]))


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    n = int(infile.readline())  # Number of leaves.
    n = 2 * n - 1  # Total number of nodes.
    characters = ['' for _ in range(n)]
    adj = [list() for _ in range(n)]
    parent = [-1 for _ in range(n)]

    leafcnt = 0
    for line in infile.readlines():
        i, j = line.strip().split('->')
        i = int(i)

        # Let's assume that i is parent of j.
        if j.isdecimal():
            j = int(j)
            adj[i].append(j)
            parent[j] = i
        else:
            adj[i].append(leafcnt)
            parent[leafcnt] = i
            characters[leafcnt] = j
            leafcnt += 1

    ret = []

    m = len(characters[0])
    sumscore = 0
    for k in range(m):
        charsubset = [char[k] if char != '' else char for char in characters]

        charsubset, score = parsimony(n, charsubset, adj, parent)
        ret.append(charsubset)
        sumscore += score

    characters = [''.join(string) for string in zip(*ret)]

    outfile.write(str(sumscore) + '\n')
    for i in range(n - 1):
        p = parent[i]
        outfile.write(f'{characters[i]}->{characters[p]}:{hamming(characters[i], characters[p])}\n')
        outfile.write(f'{characters[p]}->{characters[i]}:{hamming(characters[p], characters[i])}\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
