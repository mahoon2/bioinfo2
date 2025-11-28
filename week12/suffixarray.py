import os


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    text = infile.readline().strip()
    suffarray = [(text[-i:], len(text) - i) for i in range(1, len(text) + 1)]
    suffarray.sort()

    _, idx = zip(*suffarray)
    outfile.write(', '.join(map(str, idx)) + '\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
