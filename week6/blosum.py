import numpy as np
import pandas as pd
from tqdm import tqdm


def main():
    infile = open("../test.in", "r")
    outfile = open("../test.out", "w")

    blosum = pd.read_csv("../week4/blosum62.mat.csv", index_col=0)
    seq1, seq2 = [line.strip() for line in infile.readlines()]

    ret = np.zeros((len(seq1) + 1, len(seq2) + 1), dtype=np.int32)
    backtrack = [[None for _ in range(len(seq2) + 1)] for _ in range(len(seq1) + 1)]
    gaps = [[0 for _ in range(len(seq2) + 1)] for _ in range(len(seq1) + 1)]
    gap_opening = -11
    gap_extension = -1

    # Deletions
    ret[1][0] = gap_opening
    for i in range(2, len(seq1) + 1):
        ret[i][0] = ret[i - 1][0] + gap_extension
        backtrack[i][0] = (i - 1, 0)
        gaps[i][0] = 1

    # Insertions
    ret[0][1] = gap_opening
    for j in range(2, len(seq2) + 1):
        ret[0][j] = ret[0][j - 1] + gap_extension
        backtrack[0][j] = (0, j - 1)
        gaps[0][j] = -1

    for i in tqdm(range(1, len(seq1) + 1)):
        seq1aa = seq1[i - 1]
        for j in range(1, len(seq2) + 1):
            seq2aa = seq2[j - 1]

            deletion_penalty = gap_opening if gaps[i - 1][j] != 1 else gap_extension
            insertion_penalty = gap_opening if gaps[i][j - 1] != -1 else gap_extension

            temp = [
                (i - 1, j, ret[i - 1][j] + deletion_penalty),
                (i, j - 1, ret[i][j - 1] + insertion_penalty),
                (i - 1, j - 1, ret[i - 1][j - 1] + blosum.loc[seq1aa, seq2aa]),
            ]
            temp.sort(key=lambda l: l[2], reverse=True)

            ret[i][j] = temp[0][2]
            backtrack[i][j] = (temp[0][0], temp[0][1])

            if (i - 1, j) == backtrack[i][j]:
                gaps[i][j] = 1
            elif (i, j - 1) == backtrack[i][j]:
                gaps[i][j] = -1

    outfile.write(str(ret[len(seq1)][len(seq2)]) + "\n")

    i, j = len(seq1), len(seq2)
    out1 = ""
    out2 = ""
    while i > 0 or j > 0:
        nexti, nextj = backtrack[i][j][0], backtrack[i][j][1]

        if i != nexti and j != nextj:
            out1 += seq1[nexti]
            out2 += seq2[nextj]
        elif i != nexti:
            out1 += seq1[nexti]
            out2 += "-"
        else:
            out1 += "-"
            out2 += seq2[nextj]

        i, j = nexti, nextj

    outfile.write(out1[::-1] + "\n" + out2[::-1])

    infile.close()
    outfile.close()


if __name__ == "__main__":
    main()
