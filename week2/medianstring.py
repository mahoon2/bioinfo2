import sys
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

def main():
    infile = open(sys.argv[1], 'r')
    outfile = open('medianstring.out', 'w')

    k = int(infile.readline().strip())
    texts = [line.strip() for line in infile.readlines() if line.strip()]

    min_sum_hamming_dist = 987654321 * len(texts)
    retkmer = ''

    for kmer in product('ACGT', repeat=k):
        kmer = ''.join(kmer)

        sum_hamming_dist = 0
        for text in texts:
            min_hamming_dist = 987654321

            for i in range(len(text) - k):
                dist = hamming(kmer, text[i:i + k])
                min_hamming_dist = min(min_hamming_dist, dist)

            sum_hamming_dist += min_hamming_dist

        if min_sum_hamming_dist > sum_hamming_dist:
            min_sum_hamming_dist = sum_hamming_dist
            retkmer = kmer

    outfile.write(retkmer)

    infile.close()
    outfile.close()

if __name__ == '__main__':
    main()