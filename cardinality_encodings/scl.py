from core.variable_pool import VariablePool
from cardinality_encodings.new_sequential import build_counter


def ladder_amk(
    literals: list[int],
    width: int,
    k: int,
    pool: VariablePool,
) -> list[list[int]]:
    n = len(literals)

    if width <= 0:
        raise ValueError("width phai lon hon 0")
    if n < width:
        return []
    if k < 0:
        return [[]]
    if k >= width:
        return []
    if k == 0:
        return [[-literal] for literal in literals]

    clauses = []
    blocks = [literals[i:i + width] for i in range(0, n, width)]
    prefixes = []
    suffixes = []

    for block in blocks:
        prefix = build_counter(block, k, pool, clauses)
        suffix = build_counter(list(reversed(block)), k, pool, clauses)
        prefixes.append(prefix)
        suffixes.append(suffix)

        for i in range(k + 1, len(block) + 1):
            clauses.append([-block[i - 1], -prefix[i - 1, k]])

    for i in range(len(blocks) - 1):
        left = blocks[i]
        right = blocks[i + 1]

        for right_length in range(1, width):
            left_length = width - right_length

            if left_length > len(left) or right_length > len(right):
                continue

            for left_count in range(1, k + 1):
                right_count = k + 1 - left_count

                if left_count > left_length or right_count > right_length:
                    continue

                clauses.append([
                    -suffixes[i][left_length, left_count],
                    -prefixes[i + 1][right_length, right_count],
                ])

    return clauses


def at_least_one_chain(
    literals: list[int],
    pool: VariablePool,
    clauses: list[list[int]],
) -> list[int]:
    chain = [literals[0]]

    for literal in literals[1:]:
        current = pool.new_var()
        clauses.append([-chain[-1], current])
        clauses.append([-literal, current])
        chain.append(current)

    return chain


def window_indicators(
    literals: list[int],
    width: int,
    pool: VariablePool,
    clauses: list[list[int]],
) -> list[list[int]]:
    blocks = [literals[i:i + width] for i in range(0, len(literals), width)]
    last = len(blocks) - 1
    prefixes = [
        at_least_one_chain(block, pool, clauses) if i > 0 or last == 0 else None
        for i, block in enumerate(blocks)
    ]
    suffixes = [
        at_least_one_chain(block[::-1], pool, clauses) if i < last else None
        for i, block in enumerate(blocks)
    ]
    windows = []

    for start in range(len(literals) - width + 1):
        block, offset = divmod(start, width)
        if offset == 0:
            chain = suffixes[block] if block < last else prefixes[block]
            windows.append([chain[width - 1]])
        else:
            windows.append([
                suffixes[block][width - offset - 1],
                prefixes[block + 1][offset - 1],
            ])

    return windows
