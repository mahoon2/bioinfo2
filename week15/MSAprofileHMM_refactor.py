import numpy as np

# 0으로 나누기 경고 무시 (로그 계산 시)
np.seterr(divide="ignore", invalid="ignore")


def parse_input(input_data):
    lines = [line.strip() for line in input_data.strip().split("\n")]
    # 구분선 기준으로 데이터 나누기
    sep_indices = [i for i, line in enumerate(lines) if "--------" in line]

    sequence = lines[0]
    thresh_line = lines[sep_indices[0] + 1].split()
    threshold = float(thresh_line[0])
    pseudocount = np.float128(thresh_line[1])
    alphabet = lines[sep_indices[1] + 1].split()
    msa = lines[sep_indices[2] + 1 :]

    return sequence, threshold, pseudocount, alphabet, msa


def determine_match_columns(msa, threshold):
    msa_arr = np.array([list(row) for row in msa])
    rows, cols = msa_arr.shape
    gap_fractions = np.sum(msa_arr == "-", axis=0) / rows
    match_cols = np.where(gap_fractions < threshold)[0]
    return match_cols


def build_profile_hmm(msa, alphabet, match_cols, pseudocount):
    rows = len(msa)
    cols = len(msa[0])
    num_match = len(match_cols)
    num_states = num_match + 1
    alphabet_map = {char: i for i, char in enumerate(alphabet)}
    vocab_size = len(alphabet)

    # State Encoding: 0=M, 1=I, 2=D
    transitions = np.zeros((num_states, 3, 3), dtype=np.float128)
    emissions = np.zeros((num_states, 2, vocab_size), dtype=np.float128)  # + pseudocount

    # # Pseudocounts 적용 (유효한 전이에만)
    # # M(0) -> M(0), I(1), D(2)
    # transitions[:, 0, 0] += pseudocount
    # transitions[:, 0, 1] += pseudocount
    # transitions[:, 0, 2] += pseudocount

    # # I(1) -> M(0), I(1)
    # transitions[:, 1, 0] += pseudocount
    # transitions[:, 1, 1] += pseudocount

    # # D(2) -> M(0), D(2)
    # transitions[:, 2, 0] += pseudocount
    # transitions[:, 2, 2] += pseudocount

    for seq in msa:
        current_node = 0
        current_state = 0  # 0: M/Start

        match_idx = 0
        col_idx = 0

        while col_idx < cols:
            symbol = seq[col_idx]

            if match_idx < num_match and col_idx == match_cols[match_idx]:
                # Match column 진입
                next_node = match_idx + 1
                if symbol == "-":
                    next_state = 2  # D
                else:
                    next_state = 0  # M
                    sym_idx = alphabet_map[symbol]
                    emissions[next_node, 0, sym_idx] += 1

                transitions[current_node, current_state, next_state] += 1
                current_node = next_node
                current_state = next_state
                match_idx += 1
            else:
                # Insert column
                if symbol != "-":
                    next_state = 1  # I
                    sym_idx = alphabet_map[symbol]
                    transitions[current_node, current_state, 1] += 1
                    emissions[current_node, 1, sym_idx] += 1
                    current_state = 1

            col_idx += 1

        # End transition (M type으로 간주하여 0번 인덱스 사용)
        transitions[current_node, current_state, 0] += 1

    # 확률 정규화 (Log Space가 아닌 선형 확률 반환 -> 출력용)
    t_sums = transitions.sum(axis=2, keepdims=True)
    t_probs = transitions / np.maximum(t_sums, 1e-20)
    t_probs += np.divide(pseudocount, 1 - pseudocount)
    t_sums = t_probs.sum(axis=2, keepdims=True)
    t_probs = t_probs / np.maximum(t_sums, 1e-20)

    e_sums = emissions.sum(axis=2, keepdims=True)
    e_probs = emissions / np.maximum(e_sums, 1e-20)
    e_probs += np.divide(pseudocount, 1 - pseudocount)
    e_sums = e_probs.sum(axis=2, keepdims=True)
    e_probs = e_probs / np.maximum(e_sums, 1e-20)

    return t_probs, e_probs, alphabet_map, num_match


def print_matrices(t_probs, e_probs, alphabet, num_match):
    # 출력할 상태 리스트 생성 (S, I0, M1, D1, I1, ..., E)
    states = ["S", "I0"]
    # (layer_index, state_type) 매핑. 0=M, 1=I, 2=D
    state_coords = [(0, 0), (0, 1)]

    for i in range(1, num_match + 1):
        states.extend([f"M{i}", f"D{i}", f"I{i}"])
        state_coords.extend([(i, 0), (i, 2), (i, 1)])  # 순서: M, D, I

    states.append("E")
    # E는 별도 좌표 없이 로직으로 처리

    # 1. Transition Matrix 출력
    print("\t" + "\t".join(states))

    for r_label, (r_node, r_type) in zip(states[:-1], state_coords):
        row_vals = [r_label]
        for c_label in states:
            val = 0.0

            # End State 처리
            if c_label == "E":
                if r_node == num_match:  # 마지막 노드에서만 E로 갈 수 있음
                    # 코드상 M(0) 방향이 다음 노드로 가는 것인데, 마지막 노드에선 그게 End임
                    val = t_probs[r_node, r_type, 0]
            elif c_label in ["S", "I0"]:
                # S로 돌아오는 경우는 없음 (I0는 아래 로직에서 처리됨)
                if c_label == "S":
                    val = 0.0
                elif c_label == "I0":
                    # node 0에서 I(1)로 가는 경우
                    if r_node == 0:
                        val = t_probs[0, r_type, 1]
            else:
                # 일반적인 M, D, I 처리
                # c_label 파싱 (예: "M1" -> type="M", idx=1)
                c_type_char = c_label[0]
                c_idx = int(c_label[1:])

                # 내부 인코딩 변환
                if c_type_char == "M":
                    c_enc = 0
                elif c_type_char == "I":
                    c_enc = 1
                elif c_type_char == "D":
                    c_enc = 2

                # 연결 로직 확인
                # 1. 같은 노드 내 이동 (M->I, I->I, D->I)
                if c_idx == r_node:
                    if c_enc == 1:  # Target is I
                        val = t_probs[r_node, r_type, 1]

                # 2. 다음 노드로 이동 (M/I/D -> M_next/D_next)
                elif c_idx == r_node + 1:
                    if c_enc == 0:  # Target M
                        val = t_probs[r_node, r_type, 0]
                    elif c_enc == 2:  # Target D
                        val = t_probs[r_node, r_type, 2]

            # 0이면 정수 0으로, 아니면 소수점 포맷팅 (0.333 등)
            if val == 0:
                row_vals.append("0")
            else:
                row_vals.append(f"{val:.3g}")  # 유효숫자 고려하여 깔끔하게 출력

        print("\t".join(row_vals))

    # E 행 출력 (모두 0)
    print("E\t" + "\t".join(["0"] * len(states)))

    print("--------")

    # 2. Emission Matrix 출력
    print("\t" + "\t".join(alphabet))
    for label, (node, st_type) in zip(states[:-1], state_coords):
        row_vals = [label]
        # S, D 상태는 방출하지 않음
        if label == "S" or label.startswith("D"):
            vals = [0.0] * len(alphabet)
        else:
            # M(0) 또는 I(1)
            vals = e_probs[node, st_type, :]

        for v in vals:
            if v == 0:
                row_vals.append("0")
            else:
                row_vals.append(f"{v:.3g}")
        print("\t".join(row_vals))

    # E 행 출력
    print("E\t" + "\t".join(["0"] * len(alphabet)))


def viterbi_alignment(sequence, t_probs, e_probs, alphabet_map, num_match):
    # Viterbi 계산을 위해 Log Space로 변환
    t_log = np.log(t_probs)
    e_log = np.log(e_probs)

    seq_len = len(sequence)
    dp = np.full((seq_len + 1, num_match + 1, 3), -np.inf)
    backtrack = np.zeros((seq_len + 1, num_match + 1, 3), dtype=int)

    # Initialization
    dp[0, 0, 0] = 0

    # i=0 (Sequence 시작 전)에서의 Silent State(Deletion) 전파
    for j in range(1, num_match + 1):
        score_m = dp[0, j - 1, 0] + t_log[j - 1, 0, 2]
        score_d = dp[0, j - 1, 2] + t_log[j - 1, 2, 2]
        score_i = dp[0, j - 1, 1] + t_log[j - 1, 1, 2]

        best_score = max(score_m, score_d, score_i)
        dp[0, j, 2] = best_score

        if best_score == score_m:
            backtrack[0, j, 2] = 0
        elif best_score == score_d:
            backtrack[0, j, 2] = 2
        else:
            backtrack[0, j, 2] = 1

    # DP Fill
    for i in range(1, seq_len + 1):
        sym_idx = alphabet_map.get(sequence[i - 1], -1)

        for j in range(num_match + 1):
            # I(j) state
            emission_i = e_log[j, 1, sym_idx]
            from_m = dp[i - 1, j, 0] + t_log[j, 0, 1]
            from_i = dp[i - 1, j, 1] + t_log[j, 1, 1]
            from_d = dp[i - 1, j, 2] + t_log[j, 2, 1]

            best_i = max(from_m, from_i, from_d) + emission_i
            dp[i, j, 1] = best_i

            if best_i == from_m + emission_i:
                backtrack[i, j, 1] = 0
            elif best_i == from_i + emission_i:
                backtrack[i, j, 1] = 1
            else:
                backtrack[i, j, 1] = 2

            # M(j) state
            if j > 0:
                emission_m = e_log[j, 0, sym_idx]
                from_m_prev = dp[i - 1, j - 1, 0] + t_log[j - 1, 0, 0]
                from_i_prev = dp[i - 1, j - 1, 1] + t_log[j - 1, 1, 0]
                from_d_prev = dp[i - 1, j - 1, 2] + t_log[j - 1, 2, 0]

                best_m = max(from_m_prev, from_i_prev, from_d_prev) + emission_m
                dp[i, j, 0] = best_m

                if best_m == from_m_prev + emission_m:
                    backtrack[i, j, 0] = 0
                elif best_m == from_i_prev + emission_m:
                    backtrack[i, j, 0] = 1
                else:
                    backtrack[i, j, 0] = 2

        # Silent State (D)는 현재 i 단계에서 전파
        for j in range(1, num_match + 1):
            from_m_curr = dp[i, j - 1, 0] + t_log[j - 1, 0, 2]
            from_i_curr = dp[i, j - 1, 1] + t_log[j - 1, 1, 2]
            from_d_curr = dp[i, j - 1, 2] + t_log[j - 1, 2, 2]

            best_d = max(from_m_curr, from_i_curr, from_d_curr)
            dp[i, j, 2] = best_d

            if best_d == from_m_curr:
                backtrack[i, j, 2] = 0
            elif best_d == from_i_curr:
                backtrack[i, j, 2] = 1
            else:
                backtrack[i, j, 2] = 2

    # Termination
    last_m = dp[seq_len, num_match, 0] + t_log[num_match, 0, 0]
    last_i = dp[seq_len, num_match, 1] + t_log[num_match, 1, 0]
    last_d = dp[seq_len, num_match, 2] + t_log[num_match, 2, 0]

    best_last = max(last_m, last_i, last_d)

    if best_last == last_m:
        curr_state = 0
    elif best_last == last_i:
        curr_state = 1
    else:
        curr_state = 2

    # Backtracking
    path = []
    i, j = seq_len, num_match

    while i > 0 or j > 0:
        if curr_state == 0:  # M
            path.append(f"M{j}")
            prev_state = backtrack[i, j, 0]
            i -= 1
            j -= 1
        elif curr_state == 1:  # I
            path.append(f"I{j}")
            prev_state = backtrack[i, j, 1]
            i -= 1
        else:  # D
            path.append(f"D{j}")
            prev_state = backtrack[i, j, 2]
            j -= 1
        curr_state = prev_state

    return " ".join(path[::-1])


def solve_profile_hmm_alignment(input_str):
    sequence, threshold, pseudocount, alphabet, msa = parse_input(input_str)
    match_cols = determine_match_columns(msa, threshold)

    # Log값이 아닌 실제 확률을 받아옴
    t_probs, e_probs, alpha_map, num_match = build_profile_hmm(
        msa, alphabet, match_cols, pseudocount
    )

    # 행렬 출력
    print_matrices(t_probs, e_probs, alphabet, num_match)

    # Viterbi 수행 (내부에서 Log 변환)
    result = viterbi_alignment(sequence, t_probs, e_probs, alpha_map, num_match)
    return result


if __name__ == "__main__":
    f = open("../test.in")
    input_str = f.read()
    f.close()
    print(solve_profile_hmm_alignment(input_str))
