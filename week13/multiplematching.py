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


def solve(firstoccur, last, pattern, countarr, partialsuffix, partialindices):
    top, bottom = 0, len(last) - 1

    for target in pattern[::-1]:
        ntidx = nt_to_idx(target)

        top = firstoccur[ntidx] + countarr[top][ntidx]
        bottom = firstoccur[ntidx] + countarr[bottom + 1][ntidx] - 1

        if top > bottom:
            return []

    ret = []
    for rowidx in range(top, bottom + 1):
        backwards = 0
        while rowidx not in partialindices:
            target = last[rowidx]
            ntidx = nt_to_idx(target)
            rowidx = firstoccur[ntidx] + countarr[rowidx][ntidx]
            backwards += 1

        idx = partialindices[rowidx]
        ret.append(partialsuffix[idx][2] + backwards)

    return ret


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test1.out', 'w')

    text = infile.readline().strip() + '$'
    bwt = [[text[-i:] + text[:-i], len(text) - i] for i in range(len(text))]
    bwt[0][1] = 0
    bwt.sort()

    last = [s[-1] for s, _ in bwt]
    partialsuffixarr = [(i, s, idx) for i, (s, idx) in enumerate(bwt) if idx % 10 == 0]
    partialindices = {i: idx for idx, (i, _, _) in enumerate(partialsuffixarr)}

    # Reducing memory usage
    del bwt

    # Order: '$ A C G T'
    firstoccur = [0, 1, 0, 0, 0]
    firstoccur[2] = firstoccur[1] + last.count('A')
    firstoccur[3] = firstoccur[2] + last.count('C')
    firstoccur[4] = firstoccur[3] + last.count('G')

    countarr = get_count_array(last)

    ret = []
    for pattern in infile.readlines():
        ret.extend(
            solve(firstoccur, last, pattern.strip(), countarr, partialsuffixarr, partialindices)
        )
    ret.sort()

    outfile.write(' '.join(str(s) for s in ret) + '\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
