import sys
import numpy as np

def nt_to_idx(nt):
    if nt == 'A':
        return 0
    elif nt == 'C':
        return 1
    elif nt == 'G':
        return 2
    elif nt == 'T':
        return 3
    else:
        return -1


def main():
    infile = open(sys.argv[1], 'r')
    outfile = open('profilekmer.out', 'w')

    text = infile.readline()
    k = int(infile.readline())

    profile = np.zeros((4, k), dtype=np.float32)
    for i, line in enumerate(infile.readlines()):
        profile[i] = np.fromstring(line, dtype=np.float32, sep=' ')

    maxscore = -1
    retval = ''
    for i in range(len(text) - k):
        kmer = text[i:i + k]
        score = np.prod([profile[nt_to_idx(nt)][i] for i, nt in enumerate(kmer)])

        if maxscore < score:
            maxscore = score
            retval = kmer

    outfile.write(retval)

    infile.close()
    outfile.close()

if __name__ == '__main__':
    main()