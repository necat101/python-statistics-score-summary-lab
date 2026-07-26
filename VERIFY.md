# VERIFY.md

Fresh-clone verification of `python-statistics-score-summary-lab`.

This supersedes the verification at commit 85aaad867317d676bf2647dfbd8214ac16e6b8e8.

## Source commit verified

```
commit 498f53f3f1af860ee2c60697f4638f00aff7d689
Fix Q3 Counter check and Q2 Fraction input type in RESULTS
```

Repository: https://github.com/necat101/python-statistics-score-summary-lab

## Verification transcript

```bash
$ git clone https://github.com/necat101/python-statistics-score-summary-lab.git verify-stats
Cloning into 'verify-stats'...

$ cd verify-stats

$ git checkout --detach 498f53f3f1af860ee2c60697f4638f00aff7d689
HEAD is now at 498f53f Fix Q3 Counter check and Q2 Fraction input type in RESULTS

$ git rev-parse HEAD
498f53f3f1af860ee2c60697f4638f00aff7d689

$ python3 --version
Python 3.12.3

$ python3 check.py
[PASS] Q1 mean vs median robustness
[PASS] Q2 stdev vs pstdev (sample vs population)
[PASS] Q3 mode vs multimode (tied buckets)
[PASS] Q4 quantiles inclusive vs exclusive
[PASS] Q5 invalid / undersized inputs

Overall: PASS (5/5)
$ echo $?
0

$ python3 -m unittest -v
test_mean_median_robustness (test_statistics_lab.TestQ1MeanMedian.test_mean_median_robustness) ... ok
test_sample_vs_population (test_statistics_lab.TestQ2StdevPstdev.test_sample_vs_population) ... ok
test_single_mode_control (test_statistics_lab.TestQ3ModeMultimode.test_single_mode_control) ... ok
test_tied_first_seen_ordering (test_statistics_lab.TestQ3ModeMultimode.test_tied_first_seen_ordering) ... ok
test_inclusive_vs_exclusive (test_statistics_lab.TestQ4Quantiles.test_inclusive_vs_exclusive) ... ok
test_mean_requires_one_point (test_statistics_lab.TestQ5InvalidInputs.test_mean_requires_one_point) ... ok
test_variance_requires_two_points (test_statistics_lab.TestQ5InvalidInputs.test_variance_requires_two_points) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.003s

OK
$ echo $?
0

$ git diff --exit-code -- RESULTS.md
$ echo $?
0

$ git status --short
# (no output – working tree clean)
```

## Environment

- Python: CPython 3.12.3
- OS: Linux 6.17.0-1009-aws x86_64
- Date: 2026-07-26 UTC

All 5 case groups PASS, 7 unittest methods PASS. RESULTS.md regenerates byte-identically.
