import os


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    text = infile.readline().strip()
    ret = ''.join([s[-1] for s in sorted([text[-i:] + text[:-i] for i in range(len(text))])])
    outfile.write(ret + '\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
