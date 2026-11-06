import unittest
import random
from itertools import permutations, product

from pysat.solvers import Solver

from cardinality_encodings.new_sequential import alk, amk, exactly_k
from cardinality_encodings.scl import ladder_amk
from core.variable_pool import VariablePool
from problems.anti_bandwidth import solve as solve_anti_bandwidth
from problems.anti_bandwidth import verify as verify_anti_bandwidth
from problems.bandwidth_coloring import solve as solve_bandwidth_coloring
from problems.bandwidth_coloring import verify as verify_bandwidth_coloring


class TestNewSequential(unittest.TestCase):
    def check_encoding(self, encoder, expected, n, k):
        literals = list(range(1, n + 1))
        clauses = encoder(literals, k, VariablePool(n))

        with Solver(bootstrap_with=clauses) as solver:
            for values in product([False, True], repeat=n):
                assumptions = [
                    literal if value else -literal
                    for literal, value in zip(literals, values)
                ]
                self.assertEqual(solver.solve(assumptions=assumptions), expected(sum(values), k))

    def test_amk(self):
        for n in range(6):
            for k in range(-1, n + 2):
                self.check_encoding(amk, lambda total, bound: total <= bound, n, k)

    def test_alk(self):
        for n in range(6):
            for k in range(-1, n + 2):
                self.check_encoding(alk, lambda total, bound: total >= bound, n, k)

    def test_exactly_k(self):
        for n in range(6):
            for k in range(-1, n + 2):
                self.check_encoding(exactly_k, lambda total, bound: total == bound, n, k)

    def test_ladder_amk(self):
        for n in range(7):
            literals = list(range(1, n + 1))
            for width in range(1, n + 3):
                for k in range(-1, width + 1):
                    clauses = ladder_amk(literals, width, k, VariablePool(n))
                    with Solver(bootstrap_with=clauses) as solver:
                        for values in product([False, True], repeat=n):
                            assumptions = [
                                literal if value else -literal
                                for literal, value in zip(literals, values)
                            ]
                            expected = all(
                                sum(values[start:start + width]) <= k
                                for start in range(n - width + 1)
                            )
                            self.assertEqual(solver.solve(assumptions=assumptions), expected)

    def test_bandwidth_coloring(self):
        edges = [(0, 1, 2), (1, 2, 1)]
        colors = solve_bandwidth_coloring(3, edges, 3)
        self.assertIsNotNone(colors)
        self.assertTrue(verify_bandwidth_coloring(colors, edges))

    def test_anti_bandwidth(self):
        rng = random.Random(0)
        for n in range(2, 7):
            pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
            for _ in range(10):
                edges = rng.sample(pairs, rng.randint(1, len(pairs)))
                edges = [(v, u) if rng.random() < 0.5 else (u, v) for u, v in edges]
                expected = max(
                    min(abs(labels[u] - labels[v]) for u, v in edges)
                    for labels in permutations(range(1, n + 1))
                )
                best, labels = solve_anti_bandwidth(n, edges)
                self.assertEqual(best, expected)
                self.assertTrue(verify_anti_bandwidth(edges, labels, best))
