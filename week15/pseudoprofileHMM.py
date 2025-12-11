import os

import numpy as np


def read_input(infile):
    theta, pseudocount = list(map(float, infile.readline().strip().split()))
    infile.readline()
    chars = infile.readline().strip().split()
    infile.readline()
    alignments = np.array([[s for s in line.strip()] for line in infile.readlines()])
    return theta, pseudocount, chars, alignments


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


def create_transition_mask(nstates):
    mask = np.zeros((nstates, nstates), dtype=np.float64)

    # Start -> I0, M1, D1
    mask[0, [1, 2, 3]] = 1.0
    # I0 -> I0, M1, D1
    mask[1, [1, 2, 3]] = 1.0

    # General recursive structure
    for i in range(2, nstates - 4, 3):
        # From M_k, D_k, I_k to I_k, M_{k+1}, D_{k+1}
        mask[i, [i + 2, i + 3, i + 4]] = 1.0  # M_k transitions
        mask[i + 1, [i + 2, i + 3, i + 4]] = 1.0  # D_k transitions
        mask[i + 2, [i + 2, i + 3, i + 4]] = 1.0  # I_k transitions

    # Transitions to End state
    i = nstates - 4
    mask[i, [i + 2, i + 3]] = 1.0
    mask[i + 1, [i + 2, i + 3]] = 1.0
    mask[i + 2, [i + 2, i + 3]] = 1.0

    return mask


def create_emission_mask(nstates, nchars):
    mask = np.zeros((nstates, nchars), dtype=np.float64)
    # Insertion row (I0, I1, ...)
    for i in range(1, nstates, 3):
        mask[i, :] = 1.0
    # Match row (M1, M2, ...)
    for i in range(2, nstates, 3):
        mask[i, :] = 1.0
    return mask


def get_profile_hmm(seed, alignments, chars, nstates, pseudocount_ratio):
    transition = np.zeros((nstates, nstates), dtype=np.float64)
    emission = np.zeros((nstates, len(chars)), dtype=np.float64)
    char_to_idx = {c: i for i, c in enumerate(chars)}
    end_state_idx = nstates - 1

    for seq in alignments:
        prev_state_idx = 0
        match_col_idx = 0

        for i, char in enumerate(seq):
            is_match_col = seed[i] == 1
            curr_state_idx = -1

            if is_match_col:
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

    t_mask = create_transition_mask(nstates)
    e_mask = create_emission_mask(nstates, len(chars))

    t_row_sums = transition.sum(axis=1, keepdims=True)
    e_row_sums = emission.sum(axis=1, keepdims=True)

    t_factors = t_row_sums * pseudocount_ratio
    t_factors[t_row_sums == 0] = pseudocount_ratio

    e_factors = e_row_sums * pseudocount_ratio
    e_factors[e_row_sums == 0] = pseudocount_ratio

    transition += t_mask * t_factors
    emission += e_mask * e_factors

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

    for i in range(len(transition)):
        outfile.write(f'{states[i]}\t')
        outfile.write('\t'.join(map(lambda x: f'{x:.3f}' if x != 0 else '0', transition[i])))
        outfile.write('\n')

    outfile.write('--------\n')

    outfile.write('\t' + '\t'.join(chars) + '\n')
    for i in range(len(emission)):
        outfile.write(f'{states[i]}\t')
        outfile.write('\t'.join(map(lambda x: f'{x:.3f}' if x != 0 else '0', emission[i])))
        outfile.write('\n')


def main():
    path = os.path.dirname(__file__) + os.path.sep
    try:
        infile = open('test.in', 'r')
        outfile = open('test.out', 'w')
    except FileNotFoundError:
        infile = open(path + '../test.in', 'r')
        outfile = open(path + '../test.out', 'w')

    theta, pseudocount, chars, alignments = read_input(infile)
    seed = filter_alignments(alignments, theta)
    nmatches = seed.count(1)
    nstates = 2 + 3 * nmatches + 1

    transition, emission = get_profile_hmm(seed, alignments, chars, nstates, pseudocount)
    write_output(outfile, nmatches, chars, transition, emission)

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
