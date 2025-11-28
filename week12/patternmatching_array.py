import os


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    text = infile.readline().strip()
    suffarray = [(text[-i:], len(text) - i) for i in range(1, len(text) + 1)]
    suffarray.sort()

    patterns = [line.strip() for line in infile.readlines()]

    ret = []
    for i, (suffix, idx) in enumerate(suffarray):
        for p in patterns:
            if suffix.startswith(p):
                ret.append(idx)

    ret.sort()
    outfile.write(' '.join(map(str, ret)))
    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
