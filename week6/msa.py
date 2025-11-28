import os


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + '../test.in', 'r')
    outfile = open(path + '../test.out', 'w')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
