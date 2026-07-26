# cases.py
# Fixed inputs and exact expected outputs for python-statistics-score-summary-lab
# stdlib only

from fractions import Fraction

# Q1 – mean vs median, one extreme score
Q1_BASE = [4, 4, 4, 4, 4]
Q1_EXTREME = [4, 4, 4, 4, 14]

Q1_EXPECT = {
    "base_mean": 4,
    "base_median": 4,
    "extreme_mean": 6,
    "extreme_median": 4,
    "mean_delta": 2,
    "median_delta": 0,
}

# Q2 – stdev vs pstdev, sample vs population
# Use Fraction inputs for exact variance checks.
# Classic dataset: [2,4,4,4,5,5,7,9], mean = 5, sum_sq = 32, n=8
Q2_SCORES = [Fraction(x) for x in [2, 4, 4, 4, 5, 5, 7, 9]]
Q2_N = 8
Q2_EXPECT = {
    "mean": Fraction(5, 1),
    "pvariance": Fraction(4, 1),
    "variance": Fraction(32, 7),
    "pstdev_squared": Fraction(4, 1),  # pstdev == 2.0 exactly
}
# stdev / pstdev float values are checked via isclose, not frozen literals

# Q3 – mode vs multimode, tied buckets
# First permutation: 7,8,9 in ascending first-seen order
Q3_TIED_A = [7, 7, 8, 8, 9, 9]
Q3_TIED_A_EXPECT = {
    "mode": 7,
    "multimode": [7, 8, 9],
}
# Second permutation: same counts, different first-seen order
Q3_TIED_B = [9, 9, 8, 8, 7, 7]
Q3_TIED_B_EXPECT = {
    "mode": 9,
    "multimode": [9, 8, 7],
}
# Single-mode control
Q3_SINGLE = [7, 7, 7, 8, 9]
Q3_SINGLE_EXPECT = {
    "mode": 7,
    "multimode": [7],
}

# Q4 – quantiles inclusive vs exclusive
Q4_DATA = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
Q4_N = 4
Q4_EXPECT_EXCLUSIVE = [3, 6, 9]
Q4_EXPECT_INCLUSIVE = [3.5, 6.0, 8.5]

# Q5 – invalid / undersized inputs
# We assert the exception type only; message text is recorded as an observation.
Q5_CASES = [
    ("variance_one_element", "variance", [42], "StatisticsError"),
    ("mean_empty", "mean", [], "StatisticsError"),
]
