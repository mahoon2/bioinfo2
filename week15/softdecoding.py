import os

import numpy as np


def parse_input(infile):
    symbols = infile.readline().strip()
    infile.readline()

    alphabets = infile.readline().strip().split()
    infile.readline()

    states = infile.readline().strip().split()
    infile.readline()

    infile.readline()
    nstates = len(states)
    transition = np.ndarray((nstates, nstates), dtype=np.float64)
    for i in range(nstates):
        row = infile.readline().strip().split()[1:]
        transition[i] = np.array(list(map(np.float64, row)), dtype=np.float64)
    infile.readline()

    infile.readline()
    nalphabets = len(alphabets)
    emission = np.ndarray((nstates, nalphabets), dtype=np.float64)
    for i in range(nstates):
        row = infile.readline().strip().split()[1:]
        emission[i] = np.array(list(map(np.float64, row)), dtype=np.float64)
    return symbols, alphabets, states, transition, emission


def forward_path(symbols, alphabets, states, transition, emission):
    nstates = len(states)
    nalphabets = len(alphabets)
    alphabet_to_idx = {a: i for i, a in enumerate(alphabets)}
    dp = np.zeros((len(symbols), nstates), dtype=np.float64)

    symbolidx = alphabet_to_idx[symbols[0]]
    for j in range(nstates):
        dp[0][j] = (1 / nstates) * emission[j][symbolidx]

    for i in range(1, len(symbols)):
        symbolidx = alphabet_to_idx[symbols[i]]

        for j in range(nstates):
            dp[i][j] = np.sum(
                [dp[i - 1][k] * transition[k][j] * emission[j][symbolidx] for k in range(nstates)]
            )

    return dp


def backward_path(symbols, alphabets, states, transition, emission):
    nstates = len(states)
    nalphabets = len(alphabets)
    alphabet_to_idx = {a: i for i, a in enumerate(alphabets)}
    dp = np.zeros((len(symbols), nstates), dtype=np.float64)
    dp[-1] = 1.0

    for i in range(len(symbols) - 2, -1, -1):
        nextsymbolidx = alphabet_to_idx[symbols[i + 1]]

        for j in range(nstates):
            dp[i][j] = np.sum(
                [
                    dp[i + 1][k] * transition[j][k] * emission[k][nextsymbolidx]
                    for k in range(nstates)
                ]
            )

    return dp


def solve(forward, backward, nsymbols, nstates):
    ret = forward * backward
    ret /= forward[-1].sum()
    return ret


def write_output(outfile, states, ret):
    outfile.write("\t".join(states) + "\n")
    for row in ret:
        for data in row:
            outfile.write(f"{data:.4f}\t")
        outfile.write("\n")


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + "../test.in", "r")
    outfile = open(path + "../test.out", "w")

    symbols, alphabets, states, transition, emission = parse_input(infile)
    forward = forward_path(symbols, alphabets, states, transition, emission)
    backward = backward_path(symbols, alphabets, states, transition, emission)
    ret = solve(forward, backward, len(symbols), len(states))
    write_output(outfile, states, ret)

    infile.close()
    outfile.close()


if __name__ == "__main__":
    main()
