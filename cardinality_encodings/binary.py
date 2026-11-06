"""Ma hoa Binary."""

from core.variable_pool import VariablePool


def amo(literals: list[int], pool: VariablePool) -> list[list[int]]:
    n = len(literals)

    if n <= 1:
        return []

    num_bits = (n - 1).bit_length()
    bits = [pool.new_var() for _ in range(num_bits)]
    clauses = []

    for i in range(n):
        for j in range(num_bits):
            bit_value = (i >> j) & 1

            if bit_value == 1:
                clauses.append([-literals[i], bits[j]])
            else:
                clauses.append([-literals[i], -bits[j]])

    return clauses



def exactly_one(literals: list[int], pool: VariablePool) -> list[list[int]]:
    clauses = [list(literals)]
    clauses += amo(literals, pool)
    return clauses
