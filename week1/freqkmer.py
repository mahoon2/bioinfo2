import sys

infile = open(sys.argv[1], 'r')
outfile = open('freqkmer.out', 'w')

text, k = str(infile.readline()), int(infile.readline())

freq = {}
retval = [('', 0)]

for i in range(len(text) - k + 1):
    kmer = text[i:i + k]
    freq[kmer] = freq.get(kmer, 0) + 1

    if retval[0][1] < freq[kmer]:
        retval = [(kmer, freq[kmer])]
    elif retval[0][1] == freq[kmer]:
        retval.append((kmer, freq[kmer]))


outfile.write(' '.join([ret[0] for ret in retval]))

infile.close()
outfile.close()