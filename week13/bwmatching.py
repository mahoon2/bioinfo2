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


def solve(first, last, pattern):
    top, bottom = 0, len(first) - 1

    for target in pattern[::-1]:
        minidx = 987654321
        maxidx = -1
        for i in range(top, bottom + 1):
            if last[i][0] == target:
                minidx = min(minidx, i)
                maxidx = max(maxidx, i)

        if minidx > maxidx:
            return 0

        top = find(first, target, last[minidx][1])
        bottom = find(first, target, last[maxidx][1])

    return bottom - top + 1


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    last = [s for s in infile.readline().strip()]
    first = list(sorted(last))

    last = transform(last)
    first = transform(first)

    patterns = infile.readline().split()

    for pattern in patterns:
        outfile.write(f'{solve(first, last, pattern)} ')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
