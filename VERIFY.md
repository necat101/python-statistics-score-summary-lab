# VERIFY.md

Fresh-clone verification of `python-statistics-score-summary-lab`.

## Source commit verified

```
commit 5ba6493591a98f2361760bfbbe14ae0698c79d56
Add lab source, tests, and generated RESULTS.md
```

Repository: https://github.com/necat101/python-statistics-score-summary-lab

## Steps

```bash
git clone https://github.com/necat101/python-statistics-score-summary-lab.git verify-stats
cd verify-stats
git rev-parse HEAD
# 5ba6493591a98f2361760bfbbe14ae0698c79d56
```

## check.py

```bash
$ python3 check.py
[PASS] Q1 mean vs median robustness
[PASS] Q2 stdev vs pstdev (sample vs population)
[PASS] Q3 mode vs multimode (tied buckets)
[PASS] Q4 quantiles inclusive vs exclusive
[PASS] Q5 invalid / undersized inputs

Overall: PASS (5/5)
```

## unittest

```bash
$ python3 -m unittest -v
test_mean_median_robustness (test_statistics_lab.TestQ1MeanMedian.test_mean_median_robustness) ... ok
test_sample_vs_population (test_statistics_lab.TestQ2StdevPstdev.test_sample_vs_population) ... ok
test_single_mode_control (test_statistics_lab.TestQ3ModeMultimode.test_single_mode_control) ... ok
test_tied_first_seen_ordering (test_statistics_lab.TestQ3ModeMultimode.test_tied_first_seen_ordering) ... ok
test_inclusive_vs_exclusive (test_statistics_lab.TestQ4Quantiles.test_inclusive_vs_exclusive) ... ok
test_mean_requires_one_point (test_statistics_lab.TestQ5InvalidInputs.test_mean_requires_one_point) ... ok
test_variance_requires_two_points (test_statistics_lab.TestQ5InvalidInputs.test_variance_requires_two_points) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.002s

OK
```

## RESULTS.md reproducibility

Regenerated `RESULTS.md` via `python3 check.py` in the clean clone. No diff against the committed artifact:

```bash
$ git diff HEAD -- RESULTS.md
# (no output – files identical)
```

Working tree clean.

## Environment

- Python: CPython 3.12.3
- OS: Linux 6.17.0-1009-aws x86_64
- Date: 2026-07-26 UTC

All 5 case groups PASS, 7 unittest methods PASS.
