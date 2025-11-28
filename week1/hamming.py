import sys

infile = open(sys.argv[1], 'r')
outfile = open('hamming.out', 'w')

a, b = str(infile.readline()), str(infile.readline())
outfile.write(str(sum(1 if c1 != c2 else 0 for c1, c2 in zip(a, b))))

infile.close()
outfile.close()