from core.variable_pool import VariablePool


def build_counter(
    literals: list[int],
    max_count: int,
    pool: VariablePool,
    clauses: list[list[int]],
) -> dict[tuple[int, int], int]:
    counter = {}

    for i, literal in enumerate(literals, start=1):
        for j in range(1, min(i, max_count) + 1):
            if i == 1:
                counter[i, j] = literal
                continue

            current = pool.new_var()
            counter[i, j] = current

            if j == 1:
                previous = counter[i - 1, 1]
                clauses.append([-previous, current])
                clauses.append([-literal, current])
                clauses.append([-current, previous, literal])
            elif j == i:
                previous = counter[i - 1, j - 1]
                clauses.append([-literal, -previous, current])
                clauses.append([-current, literal])
                clauses.append([-current, previous])
            else:
                same = counter[i - 1, j]
                lower = counter[i - 1, j - 1]
                clauses.append([-same, current])
                clauses.append([-literal, -lower, current])
                clauses.append([-current, same, literal])
                clauses.append([-current, same, lower])

    return counter


def amk(literals: list[int], k: int, pool: VariablePool) -> list[list[int]]:
    n = len(literals)

    if k < 0:
        return [[]]
    if k >= n:
        return []
    if k == 0:
        return [[-literal] for literal in literals]

    clauses = []
    counter = build_counter(literals, k, pool, clauses)

    for i in range(k + 1, n + 1):
        clauses.append([-literals[i - 1], -counter[i - 1, k]])

    return clauses


def alk(literals: list[int], k: int, pool: VariablePool) -> list[list[int]]:
    return amk([-literal for literal in literals], len(literals) - k, pool)


def exactly_k(literals: list[int], k: int, pool: VariablePool) -> list[list[int]]:
    clauses = amk(literals, k, pool)
    clauses += alk(literals, k, pool)
    return clauses
