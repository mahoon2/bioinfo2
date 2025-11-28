from typing import Tuple

import numpy as np
import pandas as pd

debug = False


def windowdp(seq1, seq2) -> Tuple[np.ndarray, np.ndarray]:
    """
    Performs sequence alignment algorithm with only two rows (i.e. sliding window).
    """
    len1 = len(seq1) + 1
    len2 = len(seq2) + 1
    row1 = np.zeros(len1, dtype=np.int32)
    row2 = np.zeros(len1, dtype=np.int32)

    log = []

    for i in range(1, len1):
        row1[i] = row1[i - 1] + penalty

    if debug:
        log.append([str(i) for i in row1])

    for j in range(1, len2):
        for i in range(len1):
            if i == 0:
                row2[i] = row1[i] + penalty
            else:
                row2[i] = max(
                    row2[i - 1] + penalty,
                    row1[i] + penalty,
                    row1[i - 1] + blosum.at[seq1[i - 1], seq2[j - 1]],
                )
        if debug:
            log.append([str(i) for i in row2])
        row1, row2 = row2, row1

    # row1 holds the alignment result (last column)
    # row2 holds the result of previous column

    if debug:
        print(f"Result for {seq1} and {seq2}")
        for i in zip(*log):
            print("\t".join(i))

    return row2, row1


def linearalign(top, bottom, left, right):
    """
    Space-efficient sequence alignment algorithm with BLOSUM62 and indel penalty=5.

    .. note1:: half-open interval [top, bottom) and [left, right)
    .. note2:: middle is guaranteed to be left <= middle < right
    """
    middle = (left + right) // 2
    _, source = windowdp(seq1[top:bottom], seq2[left:middle])
    sinknext, sink = windowdp(seq1[top:bottom][::-1], seq2[middle:right][::-1])
    sinknext, sink = np.flip(sinknext), np.flip(sink)

    maxscore = -987654321
    maxrow = -1
    for i in range(bottom - top):
        if maxscore < source[i] + sink[i]:
            maxscore = source[i] + sink[i]
            maxrow = i

    if debug:
        for i, j, k in zip(source, sink, sinknext):
            print(i, j, k, sep="\t")

    print(f"({maxrow}, {middle})", end=" ")
    # Horizontal (->) cross
    if source[maxrow] + penalty + sinknext[maxrow] == maxscore:
        print(f"({maxrow}, {middle + 1})")
    # Diagonal cross
    elif (
        source[maxrow]
        + blosum.at[seq1[maxrow + top], seq2[middle]]
        + sinknext[maxrow + 1]
        == maxscore
    ):
        print(f"({maxrow + 1}, {middle + 1})")
    else:
        print("??")


infile = open("../test.in", "r")
# outfile = open('../test.out', 'w')

blosum = pd.read_csv("../week4/blosum62.mat.csv", index_col=0)
seq1, seq2 = [line.strip() for line in infile.readlines()]
penalty = -5

alignstring = linearalign(0, len(seq1), 0, len(seq2))


# outfile.write(str(ret[len(seq1)][len(seq2)]) + '\n')

infile.close()
# outfile.close()
