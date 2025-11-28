import sys
import functools
from itertools import product

def hamming(s1, s2):
    '''
        `O(n)` hamming distance calculation algorithm.
    '''
    assert len(s1) == len(s2)

    d = 0
    for i, j in zip(s1, s2):
        if i != j:
            d += 1

    return d

@functools.lru_cache(maxsize=4**10)
def neighbors(kmer, d):
    '''
        Returns neighbors with at most `d` mismatches.
    '''
    if d == 0:
        return set(kmer)

    if len(kmer) == 1:
        return set(['A', 'C', 'G', 'T'])

    suffix_neighbor = neighbors(kmer[1:], d)
    retval = set()

    for neighbor in suffix_neighbor:
        if hamming(neighbor, kmer[1:]) < d:
            for base in 'ACGT':
                retval.add(base + neighbor)
        else:
            retval.add(kmer[0] + neighbor)

    return retval

def main():
    infile = open(sys.argv[1], 'r')
    outfile = open('motifenum.out', 'w')

    k, d = infile.readline().split()
    k, d = int(k), int(d)
    texts = [line.strip() for line in infile.readlines() if line.strip()]

    found = False
    answer = set()

    for kmer in product('ACGT', repeat=k):
        kmer = ''.join(kmer)
        kmer_neighbors = neighbors(kmer, d)
        founds = True

        for line in texts:
            found = False

            for neighbor in kmer_neighbors:
                if line.find(neighbor) != -1:
                    found = True
                    break

            if not found:
                founds = False
                break

        if founds:
            answer.add(kmer)

    outfile.write(' '.join(answer))

    infile.close()
    outfile.close()

if __name__ == '__main__':
    main()