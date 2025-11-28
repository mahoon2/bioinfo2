from collections import Counter

import numpy as np
from tqdm import tqdm


def base_to_index(base: str) -> int:
    if base == 'A':
        return 0
    elif base == 'C':
        return 1
    elif base == 'G':
        return 2
    elif base == 'T':
        return 3
    else:
        return -1


def get_profile(motifs: list[str]) -> np.ndarray:
    assert len(motifs) > 0

    n = len(motifs)
    k = len(motifs[0])
    profile = np.zeros((4, k), dtype=np.float32)

    for i, bases in enumerate(zip(*motifs)):
        profile[0][i] = (bases.count('A') + 1) / (n + 4)
        profile[1][i] = (bases.count('C') + 1) / (n + 4)
        profile[2][i] = (bases.count('G') + 1) / (n + 4)
        profile[3][i] = (bases.count('T') + 1) / (n + 4)

    return profile


def calculate_score(motifs: tuple[str, ...]) -> int:
    cumscore = 0
    for bases in zip(*motifs):
        cumscore += len(motifs) - np.max(
            (bases.count('A'), bases.count('C'), bases.count('G'), bases.count('T'))
        )
    return cumscore


def get_profile_random_motif(profile: np.ndarray, text: str, K: int) -> str:
    kmers = []
    kmerprobs = np.ndarray(len(text) - K + 1, dtype=np.float32)

    for i in range(len(text) - K + 1):
        kmer = text[i : i + K]
        kmerprob = np.prod([profile[base_to_index(base)][i] for i, base in enumerate(kmer)])

        kmers.append(kmer)
        kmerprobs[i] = kmerprob

    kmerprobs /= np.sum(kmerprobs)
    assert abs(np.sum(kmerprobs) - np.float32(1.0)) <= 1e-6
    assert len(kmers) == len(kmerprobs)

    return np.random.choice(kmers, p=kmerprobs)


def gibbs_motif_search(texts: list[str], K: int, N: int) -> tuple[str, ...]:
    best_score = 987654321
    best_motifs = []
    for text in texts:
        i = int(np.random.random() * (len(text) - K + 1))
        assert i <= len(text) - K
        best_motifs.append(text[i : i + K])

    for _ in range(N):
        i = int(np.random.random() * len(texts))
        profile = get_profile(best_motifs[:i] + best_motifs[i + 1 :])
        motif = get_profile_random_motif(profile, texts[i], K)

        prev_motif = best_motifs[i]
        best_motifs[i] = motif
        score = calculate_score(tuple(best_motifs))

        if score < best_score:
            best_score = score
        else:
            best_motifs[i] = prev_motif

    return tuple(best_motifs)


def main():
    infile = open('../test.in', 'r')
    outfile = open('gibbssampler.out', 'w')

    K, T, N = infile.readline().split()
    K, T, N = int(K), int(T), int(N)
    texts = [line.strip() for line in infile.readlines() if line.strip()]

    n = len(texts[0])
    for text in texts:
        assert n == len(text), f'{text} has length {len(text)}, while n={n}'

    best_motifs = []
    for _ in tqdm(range(20)):
        best_motifs.append(gibbs_motif_search(texts, K, N))

    best_of_best_motifs = Counter(tuple(best_motifs)).most_common(1)[0][0]
    print(best_of_best_motifs)

    outfile.write('\n'.join(best_of_best_motifs))

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
