import os

import numpy as np


def read_input(infile):
    theta = float(infile.readline().strip())
    infile.readline()
    chars = infile.readline().strip().split()
    infile.readline()
    alignments = np.array([[s for s in line.strip()] for line in infile.readlines()])
    return theta, chars, alignments


def count(iterable, obj):
    return sum([1 for i in iterable if i == obj])


def filter_alignments(alignments, theta):
    n_seqs, n_cols = alignments.shape
    threshold = n_seqs * theta

    seed = []
    for j in range(n_cols):
        col = alignments[:, j]
        if count(col, '-') >= threshold:
            seed.append(0)
        else:
            seed.append(1)
    return seed


def get_state_idx(state_type, k):
    if state_type == 'Start':
        return 0
    elif state_type == 'Insertion':
        return 3 * k + 1
    elif state_type == 'Match':
        return 3 * k - 1
    elif state_type == 'Deletion':
        return 3 * k
    else:
        raise ValueError(f'Unknown state type: {state_type}')


def get_profile_hmm(seed, alignments, chars, nstates):
    # S, I0, M1, D1, I1, M2, D2, I2, ..., E
    transition = np.zeros((nstates, nstates), dtype=np.float64)
    emission = np.zeros((nstates, len(chars)), dtype=np.float64)
    char_to_idx = {c: i for i, c in enumerate(chars)}

    # End state index
    end_state_idx = nstates - 1

    for seq in alignments:
        prev_state_idx = 0
        match_col_idx = 0

        for i, char in enumerate(seq):
            curr_state_idx = -1

            if seed[i]:
                match_col_idx += 1
                if char == '-':
                    curr_state_idx = get_state_idx('Deletion', match_col_idx)
                else:
                    curr_state_idx = get_state_idx('Match', match_col_idx)
                    char_idx = char_to_idx[char]
                    emission[curr_state_idx, char_idx] += 1
            else:
                if char == '-':
                    continue
                else:
                    curr_state_idx = get_state_idx('Insertion', match_col_idx)
                    char_idx = char_to_idx[char]
                    emission[curr_state_idx, char_idx] += 1

            transition[prev_state_idx, curr_state_idx] += 1
            prev_state_idx = curr_state_idx

        transition[prev_state_idx, end_state_idx] += 1

    row_sums_t = transition.sum(axis=1, keepdims=True)
    transition = np.divide(
        transition, row_sums_t, out=np.zeros_like(transition), where=row_sums_t != 0
    )

    row_sums_e = emission.sum(axis=1, keepdims=True)
    emission = np.divide(emission, row_sums_e, out=np.zeros_like(emission), where=row_sums_e != 0)

    return transition, emission


def write_output(outfile, n_match_cols, chars, transition, emission):
    states = ['S', 'I0']
    for i in range(1, n_match_cols + 1):
        states.extend([f'M{i}', f'D{i}', f'I{i}'])
    states.append('E')

    outfile.write('\t'.join(states) + '\n')

    # Transition Matrix Output
    for i in range(len(transition)):
        outfile.write(f'{states[i]}\t')
        outfile.write('\t'.join(map(lambda x: f'{x:.3g}' if x != 0 else '0', transition[i])))
        outfile.write('\n')

    outfile.write('--------\n')

    # Emission Matrix Output
    outfile.write('\t' + '\t'.join(chars) + '\n')
    for i in range(len(emission)):
        outfile.write(f'{states[i]}\t')
        outfile.write('\t'.join(map(lambda x: f'{x:.3g}' if x != 0 else '0', emission[i])))
        outfile.write('\n')


def main():
    path = os.path.dirname(__file__) + os.path.sep
    try:
        infile = open('test.in', 'r')
        outfile = open('test.out', 'w')
    except FileNotFoundError:
        infile = open(path + '../test.in', 'r')
        outfile = open(path + '../test.out', 'w')

    theta, chars, alignments = read_input(infile)

    seed = filter_alignments(alignments, theta)

    nmatches = seed.count(1)
    nstates = 2 + 3 * nmatches + 1

    transition, emission = get_profile_hmm(seed, alignments, chars, nstates)
    write_output(outfile, nmatches, chars, transition, emission)

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
