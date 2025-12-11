import os

import numpy as np


def parse_input(infile):
    lines = [line.strip() for line in infile.readlines() if not line.startswith("-")]
    return lines[0], lines[1].split(), lines[2], lines[3].split()


def estimate(symbols, alphabets, path, states):
    nalphabets = len(alphabets)
    nstates = len(states)

    transition = np.zeros((nstates, nstates))
    emission = np.zeros((nstates, nalphabets))

    # Estimate transition

    state_to_idx = {s: i for i, s in enumerate(states)}
    for si, sj in zip(path[:-1], path[1:]):
        i, j = state_to_idx[si], state_to_idx[sj]
        transition[i][j] += 1
    for i in range(nstates):
        if transition[i].sum() == 0:
            transition[i] += 1
    transition_sum = transition.sum(axis=1, keepdims=True)
    transition /= transition_sum
    print(transition)

    # Estimate emission
    alphabet_to_idx = {a: i for i, a in enumerate(alphabets)}
    for si, ai in zip(path, symbols):
        state, alphabet = state_to_idx[si], alphabet_to_idx[ai]
        emission[state][alphabet] += 1
    for i in range(nstates):
        if emission[i].sum() == 0:
            emission[i] += 1
    emission_sum = emission.sum(axis=1, keepdims=True)
    emission /= emission_sum
    print(emission)

    return transition, emission


def write_output(outfile, transition, emission, states, alphabets):
    idx_to_states = {i: s for i, s in enumerate(states)}

    outfile.write("\t" + "\t".join(states) + "\n")
    for i in range(len(states)):
        outfile.write(f"{idx_to_states[i]}")
        for j in range(len(states)):
            outfile.write(f"\t{transition[i][j]:.3g}")
        outfile.write("\n")

    outfile.write("--------\n")

    outfile.write("\t" + "\t".join(alphabets) + "\n")
    for i in range(len(states)):
        outfile.write(f"{idx_to_states[i]}")
        for j in range(len(alphabets)):
            outfile.write(f"\t{emission[i][j]:.3g}")
        outfile.write("\n")


def main():
    path = os.path.dirname(__file__) + os.path.sep
    infile = open(path + "../test.in", "r")
    outfile = open(path + "../test.out", "w")

    symbols, alphabets, path, states = parse_input(infile)
    transition, emission = estimate(symbols, alphabets, path, states)
    write_output(outfile, transition, emission, states, alphabets)

    infile.close()
    outfile.close()


if __name__ == "__main__":
    main()
