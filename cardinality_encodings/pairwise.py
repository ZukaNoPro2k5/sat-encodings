"""Ma hoa Pairwise."""

from core.variable_pool import VariablePool


def amo(literals: list[int], pool: VariablePool) -> list[list[int]]:
    n = len(literals)
    res = []
    for i in range(n):
        for j in range(i+1, n):
            res.append([-1 * literals[i], -1 * literals[j]])
    return res



def exactly_one(literals: list[int], pool: VariablePool) -> list[list[int]]:
    n = len(literals)
    res = []
    res = [list(literals)]
    res += amo(literals, pool)
    return res
