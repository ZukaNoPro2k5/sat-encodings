from pysat.solvers import Solver

from core.variable_pool import VariablePool


def solve(
    n: int,
    edges: list[tuple[int, int, int]],
    max_color: int,
) -> list[int] | None:
    pool = VariablePool()
    variables = {}
    clauses = []

    for u in range(n):
        for color in range(2, max_color + 1):
            variables[u, color] = pool.new_var()

    def threshold(u: int, color: int):
        if color <= 1:
            return True
        if color > max_color:
            return False
        return variables[u, color]

    def negate(value):
        if isinstance(value, bool):
            return not value
        return -value

    def add_clause(*values):
        if any(value is True for value in values):
            return
        clauses.append([value for value in values if value is not False])

    for u in range(n):
        for color in range(2, max_color):
            add_clause(-variables[u, color + 1], variables[u, color])

    for u, v, distance in edges:
        for color in range(1, max_color + 1):
            add_clause(
                negate(threshold(u, color)),
                threshold(u, color + 1),
                negate(threshold(v, color - distance + 1)),
                threshold(v, color + distance),
            )

    with Solver(bootstrap_with=clauses) as solver:
        if not solver.solve():
            return None
        model = {literal for literal in solver.get_model() if literal > 0}

    colors = []
    for u in range(n):
        colors.append(max(
            color
            for color in range(1, max_color + 1)
            if threshold(u, color) is True or threshold(u, color) in model
        ))
    return colors


def verify(colors: list[int], edges: list[tuple[int, int, int]]) -> bool:
    return all(abs(colors[u] - colors[v]) >= distance for u, v, distance in edges)
