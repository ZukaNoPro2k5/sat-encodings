"""Quan ly ID bien SAT, bao gom bien goc va bien phu."""


class VariablePool:
    def __init__(self, max_existing: int = 0):
        self.current = max_existing

    def new_var(self) -> int:
        self.current += 1
        return self.current
