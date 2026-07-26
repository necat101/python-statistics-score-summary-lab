# test_statistics_lab.py
# Independent unittest suite – does NOT import check.py

import math
import statistics
import unittest
from collections import Counter
from fractions import Fraction


class TestQ1MeanMedian(unittest.TestCase):
    def test_mean_median_robustness(self):
        base = [4, 4, 4, 4, 4]
        extreme = [4, 4, 4, 4, 14]

        base_mean = statistics.mean(base)
        base_median = statistics.median(base)
        extreme_mean = statistics.mean(extreme)
        extreme_median = statistics.median(extreme)

        self.assertEqual(base_mean, 4)
        self.assertEqual(base_median, 4)
        self.assertEqual(extreme_mean, 6)
        self.assertEqual(extreme_median, 4)
        self.assertEqual(extreme_mean - base_mean, 2)
        self.assertEqual(extreme_median - base_median, 0)


class TestQ2StdevPstdev(unittest.TestCase):
    def test_sample_vs_population(self):
        # Fraction inputs for exact variance
        data = [Fraction(x) for x in [2, 4, 4, 4, 5, 5, 7, 9]]
        n = 8

        mean_val = statistics.mean(data)
        self.assertEqual(mean_val, Fraction(5, 1))

        pvar = statistics.pvariance(data)
        var = statistics.variance(data)

        self.assertEqual(pvar, Fraction(4, 1))
        self.assertEqual(var, Fraction(32, 7))

        # variance identity: var*(n-1) == pvar*n
        self.assertEqual(var * (n - 1), pvar * n)

        pstdev_val = statistics.pstdev(data)
        stdev_val = statistics.stdev(data)

        # Float checks – compare against sqrt(expected), not a frozen literal
        self.assertTrue(
            math.isclose(pstdev_val, math.sqrt(float(pvar)), rel_tol=1e-15)
        )
        self.assertTrue(
            math.isclose(stdev_val, math.sqrt(float(var)), rel_tol=1e-15)
        )
        # Squared round-trip
        self.assertTrue(
            math.isclose(pstdev_val * pstdev_val, float(pvar), rel_tol=1e-15)
        )
        self.assertTrue(
            math.isclose(stdev_val * stdev_val, float(var), rel_tol=1e-15)
        )
        # stdev > pstdev
        self.assertGreater(stdev_val, pstdev_val)


class TestQ3ModeMultimode(unittest.TestCase):
    def test_tied_first_seen_ordering(self):
        # Permutation A: 7,8,9 first-seen order
        tied_a = [7, 7, 8, 8, 9, 9]
        mode_a = statistics.mode(tied_a)
        multimode_a = statistics.multimode(tied_a)
        self.assertEqual(mode_a, 7)
        self.assertEqual(multimode_a, [7, 8, 9])
        self.assertEqual(mode_a, multimode_a[0])

        # Permutation B: same counts, different first-seen order
        tied_b = [9, 9, 8, 8, 7, 7]
        mode_b = statistics.mode(tied_b)
        multimode_b = statistics.multimode(tied_b)
        self.assertEqual(mode_b, 9)
        self.assertEqual(multimode_b, [9, 8, 7])
        self.assertEqual(mode_b, multimode_b[0])

        # Verify frequency maps are identical
        counts_a = Counter(tied_a)
        counts_b = Counter(tied_b)
        self.assertEqual(counts_a, counts_b)
        # Each value appears exactly twice
        self.assertEqual(set(counts_a.values()), {2})

        # Ordering follows first encounter, not numeric sort
        self.assertNotEqual(multimode_a, multimode_b)

    def test_single_mode_control(self):
        single = [7, 7, 7, 8, 9]
        self.assertEqual(statistics.mode(single), 7)
        self.assertEqual(statistics.multimode(single), [7])


class TestQ4Quantiles(unittest.TestCase):
    def test_inclusive_vs_exclusive(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        excl = statistics.quantiles(data, n=4, method="exclusive")
        incl = statistics.quantiles(data, n=4, method="inclusive")

        self.assertEqual(excl, [3, 6, 9])
        self.assertEqual(incl, [3.5, 6.0, 8.5])

        # Median identical, ends differ
        self.assertEqual(excl[1], incl[1])
        self.assertNotEqual(excl[0], incl[0])
        self.assertNotEqual(excl[2], incl[2])


class TestQ5InvalidInputs(unittest.TestCase):
    def test_variance_requires_two_points(self):
        with self.assertRaises(statistics.StatisticsError) as cm:
            statistics.variance([42])
        # Message text is NOT asserted – it varies across Python versions.
        # Recorded in RESULTS.md as an observation.

    def test_mean_requires_one_point(self):
        with self.assertRaises(statistics.StatisticsError) as cm:
            statistics.mean([])
        # Message text is NOT asserted.


if __name__ == "__main__":
    unittest.main()
