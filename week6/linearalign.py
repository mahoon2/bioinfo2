import csv
from pathlib import Path
from typing import Dict, Tuple

import numpy as np

NUMBA_AVAILABLE = True
try:
    from numba import njit
except ImportError:
    NUMBA_AVAILABLE = False

    def njit(*args, **kwargs):  # type: ignore
        if args and callable(args[0]) and not kwargs:
            return args[0]

        def decorator(func):
            return func

        return decorator


GAP_PENALTY = -5


def load_substitution_matrix(filepath: Path) -> Tuple[np.ndarray, Dict[str, int]]:
    """
    Parse a CSV substitution matrix into a dense numpy array and residue lookup table.
    """
    with filepath.open('r', newline='') as handle:
        reader = csv.reader(handle)
        header = next(reader)[1:]
        row_labels = []
        rows = []
        for row in reader:
            row_labels.append(row[0])
            rows.append([int(value) for value in row[1:]])

    substitution = np.array(rows, dtype=np.int16)
    if row_labels != header:
        row_lookup = {symbol: idx for idx, symbol in enumerate(row_labels)}
        reorder = [row_lookup[symbol] for symbol in header]
        substitution = substitution[reorder, :]

    return substitution, {symbol: idx for idx, symbol in enumerate(header)}


@njit(cache=True)
def _window_dp_kernel(
    query_codes: np.ndarray,
    target_codes: np.ndarray,
    substitution: np.ndarray,
    gap_penalty: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Hirschberg's forward/backward scoring kernel implemented with two rolling rows.
    """
    query_len = query_codes.shape[0] + 1
    target_len = target_codes.shape[0] + 1

    previous_col = np.zeros(query_len, dtype=np.int32)
    current_col = np.zeros(query_len, dtype=np.int32)

    for i in range(1, query_len):
        previous_col[i] = previous_col[i - 1] + gap_penalty

    for j in range(1, target_len):
        residue_target = target_codes[j - 1]
        current_col[0] = previous_col[0] + gap_penalty
        for i in range(1, query_len):
            diagonal = previous_col[i - 1] + substitution[query_codes[i - 1], residue_target]
            vertical = previous_col[i] + gap_penalty
            horizontal = current_col[i - 1] + gap_penalty

            best = diagonal
            if vertical > best:
                best = vertical
            if horizontal > best:
                best = horizontal

            current_col[i] = best

        previous_col, current_col = current_col, previous_col

    return current_col, previous_col


class HirschbergAligner:
    """
    Space-efficient global aligner using Hirschberg's divide-and-conquer dynamic programming.
    """

    def __init__(self, query: str, target: str, substitution: np.ndarray, residue_lookup: Dict[str, int]):
        self.query = query
        self.target = target
        self.substitution = substitution.astype(np.int16, copy=False)
        self.residue_lookup = residue_lookup
        self.gap_penalty = GAP_PENALTY
        self.query_codes = np.array([residue_lookup[aa] for aa in query], dtype=np.int16)
        self.target_codes = np.array([residue_lookup[aa] for aa in target], dtype=np.int16)
        self.best_score: int | None = None

    def align(self) -> Tuple[int, str]:
        """
        Compute the optimal alignment score and the associated edit script.
        """
        script = self._align_block(0, self.query_codes.size, 0, self.target_codes.size)
        assert self.best_score is not None  # score is assigned during the first split
        return self.best_score, script

    def _half_scores(self, query_slice: np.ndarray, target_slice: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        return _window_dp_kernel(query_slice, target_slice, self.substitution, self.gap_penalty)

    def _align_block(self, top: int, bottom: int, left: int, right: int) -> str:
        if top >= bottom:
            return 'H' * (right - left)
        if left >= right:
            return 'V' * (bottom - top)

        midpoint = (left + right) // 2

        _, forward_scores = self._half_scores(
            self.query_codes[top:bottom],
            self.target_codes[left:midpoint],
        )
        backward_prev, backward_scores = self._half_scores(
            self.query_codes[top:bottom][::-1],
            self.target_codes[midpoint:right][::-1],
        )
        backward_prev = backward_prev[::-1]
        backward_scores = backward_scores[::-1]

        total_scores = forward_scores + backward_scores
        split_row = int(np.argmax(total_scores))
        split_score = int(total_scores[split_row])

        if self.best_score is None:
            self.best_score = split_score

        forward_at_split = int(forward_scores[split_row])

        if forward_at_split + self.gap_penalty + int(backward_prev[split_row]) == split_score:
            left_part = self._align_block(top, top + split_row, left, midpoint)
            right_part = self._align_block(top + split_row, bottom, midpoint + 1, right)
            return left_part + 'H' + right_part

        diagonal_possible = split_row + 1 < backward_prev.size and midpoint < right
        if diagonal_possible:
            diag_score = (
                forward_at_split
                + int(self.substitution[self.query_codes[top + split_row], self.target_codes[midpoint]])
                + int(backward_prev[split_row + 1])
            )
            if diag_score == split_score:
                left_part = self._align_block(top, top + split_row, left, midpoint)
                right_part = self._align_block(top + split_row + 1, bottom, midpoint + 1, right)
                return left_part + 'D' + right_part

        left_part = self._align_block(top, top + split_row, left, midpoint)
        right_part = self._align_block(top + split_row + 1, bottom, midpoint, right)
        return left_part + 'V' + right_part


def materialize_alignment(script: str, query: str, target: str) -> Tuple[str, str]:
    """
    Convert Hirschberg edit script into aligned sequence strings.
    """
    aligned_query: list[str] = []
    aligned_target: list[str] = []
    qi = 0
    ti = 0

    for step in script:
        if step == 'V':
            aligned_query.append(query[qi])
            aligned_target.append('-')
            qi += 1
        elif step == 'H':
            aligned_query.append('-')
            aligned_target.append(target[ti])
            ti += 1
        else:  # 'D'
            aligned_query.append(query[qi])
            aligned_target.append(target[ti])
            qi += 1
            ti += 1

    return ''.join(aligned_query), ''.join(aligned_target)


def load_sequences(filepath: Path) -> Tuple[str, str]:
    with filepath.open('r') as handle:
        lines = [line.strip() for line in handle if line.strip()]
    if len(lines) != 2:
        raise ValueError(f'Expected exactly two sequences in {filepath}')
    return lines[0], lines[1]


def write_alignment(filepath: Path, score: int, aligned_query: str, aligned_target: str) -> None:
    with filepath.open('w') as handle:
        handle.write(f'{score}\n{aligned_query}\n{aligned_target}\n')


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    input_path = (base_dir / '../test.in').resolve()
    output_path = (base_dir / '../test.out').resolve()
    matrix_path = (base_dir / '../week4/blosum62.mat.csv').resolve()

    query, target = load_sequences(input_path)
    substitution, residue_lookup = load_substitution_matrix(matrix_path)

    aligner = HirschbergAligner(query, target, substitution, residue_lookup)
    score, script = aligner.align()

    aligned_query, aligned_target = materialize_alignment(script, query, target)
    write_alignment(output_path, score, aligned_query, aligned_target)


if __name__ == '__main__':
    main()
