"""Ma hoa Product."""

from core.variable_pool import VariablePool


def amo(literals: list[int], pool: VariablePool) -> list[list[int]]:
    """Tao CNF cho rang buoc co nhieu nhat mot literal dung."""
    raise NotImplementedError("Tu cai dat Product AMO")


def exactly_one(literals: list[int], pool: VariablePool) -> list[list[int]]:
    """Tao CNF cho rang buoc co dung mot literal dung."""
    raise NotImplementedError("Tu cai dat Product exactly-one")
