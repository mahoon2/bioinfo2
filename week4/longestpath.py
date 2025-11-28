def main():
    infile = open('../test.in', 'r')
    outfile = open('../parsed.in', 'w')

    source = int(infile.readline())
    sink = int(infile.readline())

    lines = [line.strip() for line in infile.readlines() if line.strip()]

    parsed = []
    for line in lines:
        begin, end = line.split('->')
        end, weight = end.split(':')
        parsed.append((begin, end, weight))

    outfile.write(f'{source} {sink}\n')
    outfile.write(f'{len(parsed)}\n')
    for data in parsed:
        begin, end, weight = data
        outfile.write(f'{begin} {end} {weight}\n')

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
