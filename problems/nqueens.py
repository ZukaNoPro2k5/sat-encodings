"""Khung mo rong sang bai toan N-Queens."""

from collections.abc import Callable

from core.variable_pool import VariablePool

Encoder = Callable[[list[int], VariablePool], list[list[int]]]


def build_nqueens(
    n: int, amo: Encoder, exactly_one: Encoder
) -> tuple[list[list[int]], dict[tuple[int, int], int]]:
    """Tra ve CNF va bang anh xa (hang, cot) sang ID bien SAT."""
    raise NotImplementedError("Tu cai dat N-Queens khi san sang")
