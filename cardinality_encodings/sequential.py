"""Ma hoa Sequential."""

from core.variable_pool import VariablePool


def amo(literals: list[int], pool: VariablePool) -> list[list[int]]:
    n = len(literals)

    if n <= 1:
        return []

    aux = [pool.new_var() for _ in range(n - 1)]
    clauses = []
    for i in range(n-1):
        clauses.append([-literals[i],aux[i]])
        clauses.append([-aux[i],-literals[i+1]])

    for i in range(n-2):
        clauses.append([-aux[i],aux[i+1]])

    return clauses

def exactly_one(literals: list[int], pool: VariablePool) -> list[list[int]]:
    clauses = [list(literals)]
    clauses += amo(literals, pool)
    return clauses 
