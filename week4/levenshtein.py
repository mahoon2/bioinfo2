import numpy as np


def main():
    infile = open('../test.in', 'r')
    outfile = open('../test.out', 'w')

    seq1, seq2 = [line.strip() for line in infile.readlines()]

    ret = np.zeros((len(seq1) + 1, len(seq2) + 1), dtype=np.int32)

    for i in range(1, len(seq1) + 1):
        ret[i][0] = ret[i - 1][0] + 1

    for j in range(1, len(seq2) + 1):
        ret[0][j] = ret[0][j] + 1

    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):
            ret[i][j] = min(
                ret[i - 1][j] + 1,
                ret[i][j - 1] + 1,
                ret[i - 1][j - 1] + (1 if seq1[i - 1] != seq2[j - 1] else 0),
            )

    outfile.write(str(ret[len(seq1)][len(seq2)]))

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
