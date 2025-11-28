import numpy as np


def base_to_index(base: str) -> int:
    if base == "A":
        return 0
    elif base == "C":
        return 1
    elif base == "G":
        return 2
    elif base == "T":
        return 3
    else:
        return -1


def get_profile(motifs: list[str]) -> np.ndarray:
    assert len(motifs) > 0

    n = len(motifs)
    k = len(motifs[0])
    profile = np.zeros((4, k), dtype=np.float32)

    for i, bases in enumerate(zip(*motifs)):
        profile[0][i] = (bases.count("A") + 1) / (n + 4)
        profile[1][i] = (bases.count("C") + 1) / (n + 4)
        profile[2][i] = (bases.count("G") + 1) / (n + 4)
        profile[3][i] = (bases.count("T") + 1) / (n + 4)

    return profile


def get_profile_probable_kmer(profile: np.ndarray, text: str, k: int) -> str:
    assert profile.shape[0] == 4 and profile.shape[1] == k

    best_score = -1
    best_kmer = ""

    for i in range(len(text) - k + 1):
        kmer = text[i : i + k]
        score = np.prod(
            [profile[base_to_index(base)][i] for i, base in enumerate(kmer)]
        )

        if best_score < score:
            best_score = score
            best_kmer = kmer

    return best_kmer


def calculate_score(profile: np.ndarray, motifs: list[str]) -> np.float32:
    cumscore = []

    for motif in motifs:
        cumscore.append(
            np.prod([profile[base_to_index(base)][i] for i, base in enumerate(motif)])
        )

    return np.sum(cumscore)


def main():
    infile = open("../test.in", "r")
    outfile = open("greedymotif.out", "w")

    k, t = infile.readline().split()
    k, t = int(k), int(t)
    texts = [line.strip() for line in infile.readlines() if line.strip()]

    n = len(texts[0])
    for text in texts:
        assert n == len(text), f"{text} has length {len(text)}, while n={n}"

    best_motifs = [text[:k] for text in texts]
    best_score = -1

    for i in range(len(texts[0]) - k + 1):
        motif = texts[0][i : i + k]
        motifs = [motif]
        profile = np.zeros((4, k), dtype=np.float32)

        for j in range(1, t):
            profile = get_profile(motifs)
            probable_kmer = get_profile_probable_kmer(profile, texts[j], k)
            motifs.append(probable_kmer)

        score = calculate_score(profile, motifs)
        if best_score < score:
            best_score = score
            best_motifs = motifs

    outfile.write("\n".join(best_motifs))

    infile.close()
    outfile.close()


if __name__ == "__main__":
    main()
