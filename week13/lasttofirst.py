import os
from itertools import count


def transform(stringlist):
    counters = {}
    ret = []

    for c in stringlist:
        if c not in counters:
            counters[c] = count()
        ret.append((c, next(counters[c])))

    return ret


def find(stringlist, c, count):
    for i, (c1, count1) in enumerate(stringlist):
        if c1 == c and count1 == count:
            return i

    return -1


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    last = [s for s in infile.readline().strip()]
    idx = int(infile.readline().strip())
    first = list(sorted(last))

    last = transform(last)
    first = transform(first)

    target, targetcount = last[idx]
    outfile.write(f'{find(first, target, targetcount)}\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
