import os


def get_count_array(string):
    ret = [[0, 0, 0, 0, 0] for _ in range(len(string) + 1)]

    for i, c in enumerate(string):
        for j in range(5):
            ret[i + 1][j] = ret[i][j]
        idx = nt_to_idx(c)
        ret[i + 1][idx] += 1

    return ret


def nt_to_idx(c):
    assert len(c) == 1

    if c == '$':
        return 0
    elif c == 'A':
        return 1
    elif c == 'C':
        return 2
    elif c == 'G':
        return 3
    elif c == 'T':
        return 4

    return -1


def solve(firstoccur, pattern, countarr):
    top, bottom = 0, len(countarr) - 2

    for target in pattern[::-1]:
        ntidx = nt_to_idx(target)

        top = firstoccur[ntidx] + countarr[top][ntidx]
        bottom = firstoccur[ntidx] + countarr[bottom + 1][ntidx] - 1

        if top > bottom:
            return 0

    return bottom - top + 1


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    last = [s for s in infile.readline().strip()]
    # Order: '$ A C G T'
    firstoccur = [0, 1, 0, 0, 0]
    firstoccur[2] = firstoccur[1] + last.count('A')
    firstoccur[3] = firstoccur[2] + last.count('C')
    firstoccur[4] = firstoccur[3] + last.count('G')

    countarr = get_count_array(last)

    patterns = infile.readline().split()
    for pattern in patterns:
        outfile.write(f'{solve(firstoccur, pattern, countarr)} ')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
