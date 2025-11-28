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
    first = list(sorted(last))

    last = transform(last)
    first = transform(first)

    print(first)
    print(last)

    target = '$'
    targetcount = 0
    for _ in range(len(last) - 1):
        idx = find(last, target, targetcount)
        target, targetcount = first[idx]
        outfile.write(target)

    outfile.write('$\n')
    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
