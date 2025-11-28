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


def get_profile(motifs: tuple[str, ...]) -> np.ndarray:
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


def get_profile_probable_kmer(profile: np.ndarray, text: str, k: int) -> str:
    assert profile.shape[0] == 4 and profile.shape[1] == k

    best_score = -1
    best_kmer = ''

    for i in range(len(text) - k + 1):
        kmer = text[i : i + k]
        score = np.prod([profile[base_to_index(base)][i] for i, base in enumerate(kmer)])

        if best_score < score:
            best_score = score
            best_kmer = kmer

    return best_kmer


def calculate_score(profile: np.ndarray, motifs: tuple[str, ...]) -> np.float32:
    cumscore = []

    for motif in motifs:
        cumscore.append(np.prod([profile[base_to_index(base)][i] for i, base in enumerate(motif)]))

    return np.sum(cumscore)


def random_motif_search(texts: list[str], k: int) -> tuple[str, ...]:
    """
    Implements `RandomizedMotifSearch` from textbook.
    This function iteratively calculates k-mer profile and selects profile-most probable k-mers.

    :Example:

    ```
    motifs = random_motif_search(['ATC', 'GCG'], 2)
    ```

    :param texts: List of sequences.
    :type texts: List[str, ...]
    :param k: An integer specifing k-mer.
    :type k: int

    :raises AssertionError: When index is out-of-range.

    :return: Tuple of k-mers.
    :rtype: Tuple[str, ...]

    .. seealso:: `calculate_score()`
    .. warnings:: This function may fall to local optima.
    .. note:: See textbook for pseudocode.
    .. todo:: speed-up the calculation process.
    """
    best_score = -1
    best_motifs = []
    for text in texts:
        i = int(np.random.random() * (len(text) - k + 1))
        assert i <= len(text) - k
        best_motifs.append(text[i : i + k])

    best_motifs = tuple(best_motifs)
    while True:
        profile = get_profile(best_motifs)

        motifs = tuple(get_profile_probable_kmer(profile, text, k) for text in texts)
        score = calculate_score(profile, motifs)

        if best_score < score:
            best_score = score
            best_motifs = motifs
        else:
            return best_motifs


def main():
    """
    Main function with no arguments.

    :param: None
    :return: None
    """
    infile = open('../test.in', 'r')
    outfile = open('randommotif.out', 'w')

    k, t = infile.readline().split()
    k, t = int(k), int(t)
    texts = [line.strip() for line in infile.readlines() if line.strip()]

    n = len(texts[0])
    for text in texts:
        assert n == len(text), f'{text} has length {len(text)}, while n={n}'

    best_motifs = []
    for _ in tqdm(range(1000)):
        best_motifs.append(random_motif_search(texts, k))

    best_of_best_motifs = Counter(tuple(best_motifs)).most_common(1)[0][0]
    print(best_of_best_motifs)

    outfile.write('\n'.join(best_of_best_motifs))

    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
