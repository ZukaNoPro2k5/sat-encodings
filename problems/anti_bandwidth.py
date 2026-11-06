from pysat.solvers import Solver

from core.variable_pool import VariablePool


def exactly_one(literals: list[int]) -> list[list[int]]:
    clauses = [list(literals)]

    for i in range(len(literals)):
        for j in range(i + 1, len(literals)):
            clauses.append([-literals[i], -literals[j]])

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
    prefixes = [at_least_one_chain(block, pool, clauses) for block in blocks]
    suffixes = [at_least_one_chain(block[::-1], pool, clauses) for block in blocks]
    windows = []

    for start in range(len(literals) - width + 1):
        block, offset = divmod(start, width)
        if offset == 0:
            windows.append([prefixes[block][width - 1]])
        else:
            windows.append([
                suffixes[block][width - offset - 1],
                prefixes[block + 1][offset - 1],
            ])

    return windows


def check(n: int, edges: list[tuple[int, int]], distance: int) -> list[int] | None:
    variables = {(u, label): u * n + label for u in range(n) for label in range(1, n + 1)}
    pool = VariablePool(n * n)
    clauses = []

    for u in range(n):
        clauses += exactly_one([variables[u, label] for label in range(1, n + 1)])

    for label in range(1, n + 1):
        clauses += exactly_one([variables[u, label] for u in range(n)])

    if distance > 1:
        windows = {}
        for u in {vertex for edge in edges for vertex in edge}:
            labels = [variables[u, label] for label in range(1, n + 1)]
            windows[u] = window_indicators(labels, distance, pool, clauses)

        for u, v in edges:
            for left, right in zip(windows[u], windows[v]):
                for a in left:
                    for b in right:
                        clauses.append([-a, -b])

    with Solver(bootstrap_with=clauses) as solver:
        if not solver.solve():
            return None
        model = {literal for literal in solver.get_model() if literal > 0}

    return [next(label for label in range(1, n + 1) if variables[u, label] in model) for u in range(n)]


def solve(n: int, edges: list[tuple[int, int]]) -> tuple[int, list[int]]:
    best = 0
    labels = check(n, edges, 0)

    for distance in range(1, n):
        current = check(n, edges, distance)
        if current is None:
            break
        best = distance
        labels = current

    return best, labels


def verify(edges: list[tuple[int, int]], labels: list[int], distance: int) -> bool:
    return all(abs(labels[u] - labels[v]) >= distance for u, v in edges)
