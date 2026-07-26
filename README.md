# python-statistics-score-summary-lab

A deterministic, Python stdlib-only correctness lab for summarizing a few fixed ML-style evaluation score sets using `statistics`.

Four narrow questions, fixed literal inputs, exact expected outputs:

1. **mean vs median** – one extreme score changes `mean` more than `median`
2. **stdev vs pstdev** – sample and population standard deviation answer different questions
3. **mode vs multimode** – tied score buckets, first-seen ordering
4. **quantiles inclusive vs exclusive** – different quartile boundaries on the same observations

No NumPy, pandas, SciPy, randomness, downloaded data, model training, concurrency, C extensions, plotting, or timing benchmarks.

These are summary statistics on fixed toy score lists. They do not establish model quality.

---

## Hacker News opinions

Source: https://news.ycombinator.com/item?id=6194023 – "PEP 450: Adding A Statistics Module To The Standard Library" (2013, 83 comments)

Representative positions from the thread:

- **fiatmoney**: "It's not a terrible idea to support the absolute basics like mean & variance, but anything beyond that (particularly … models or tests) is not a good idea for a standard library. … Basically, the idea of 'batteries included' should also mean that if something looks like you can put a D-cell in there, you're unlikely to blow your arm off."
- **clutchski / bayesianhorse / zokier**: anti-stdlib-growth – pip install is easy, stdlib APIs freeze permanently, reference to "The Python Standard Library - Where Modules Go To Die"
- **cabalamat**: the "people in corporate environments can't install numpy" argument is not a good justification for stdlib inclusion – "use virtualenv"
- **aristus**: "About damned time. Writing your own stats library is like writing your own crypto."
- **andrewflnr**: pro – "I was surprised and annoyed to find there wasn't a standard library for doing excel-level statistics"
- **bachback**: "the problem is numpy itself … I don't quite understand why a package has to depend on LINPACK"
- **bthomas**: "this would accelerate the adoption of Python 3 in the scientific community"
- others: put it in `math` instead, mention pandas, note PHP is ahead among dynamic languages

Overall split: pro = "calculator-level basics belong in stdlib, DIY stats is numerically treacherous"; con = "stdlib freezes, use PyPI".

---

## PEP rationale

Source: https://peps.python.org/pep-0450/ – PEP 450, Steven D'Aprano, Python 3.4, Final

- Target level: graphing / scientific calculators, explicitly **not** NumPy / SciPy / SAS / Matlab
- Design principle: **"Correctness over speed. It is easier to speed up a correct but slow function than to correct a fast but buggy one."**
- DIY `mean = sum(data)/len(data)` loses precision on floats of wildly differing magnitude
- DIY variance using the Computational Formula gives `0.0` then `-1239429440.1` on shifted data where the true answer is `7.5`; "completely unsuitable for computation by computer"
- Functions conserve input numeric type: mean of `Decimal`s → `Decimal`, mean of `Fraction`s → `Fraction`
- Population and sample variance / standard deviation both included, matching scientific calculators, with optional pre-computed mean argument
- Original PEP 450 API (Python 3.4): `mean, median, median_low, median_high, median_grouped, mode, variance, stdev, pvariance, pstdev`

---

## Current documentation

Source: https://docs.python.org/3/library/statistics.html (Python 3.14)

Additions since PEP 450:

- `fmean, geometric_mean, harmonic_mean` (3.6 / 3.8)
- `mode()` changed in 3.8: now returns the first mode encountered instead of raising `StatisticsError` on multimodal data
- **`multimode(data)` (3.8)** – returns a list of all modes, in first-seen order
- **`quantiles(data, n=4, method='exclusive'|'inclusive')` (3.8)** – exclusive = data sampled from a population that can have more extreme values; inclusive = describing population data or samples known to include extremes
- `covariance, correlation, linear_regression` (3.10–3.11)
- `NormalDist` class (3.8, expanded in 3.9+)
- `kde, kde_random` (3.13)

Other notes from the current docs:

- "not intended to be a competitor to NumPy / SciPy"
- Supports `int`, `float`, `Decimal`, `Fraction`; mixed types undefined
- `mode()` is the only statistic accepting nominal (non-numeric) data
- NaN handling caveat explicitly documented for `median()`, `mode()`, `multimode()`, `quantiles()`

---

## Local observations

Running CPython 3.12.3 (`statistics` module version as shipped with CPython).

**Q1 – mean vs median**
```
base    = [4,4,4,4,4]    → mean=4, median=4
extreme = [4,4,4,4,14]   → mean=6, median=4
```
Mean shifts by +2.0, median is unchanged. Median is robust to the outlier.

**Q2 – stdev vs pstdev**
```
scores = [2,4,4,4,5,5,7,9]  (as Fractions)
mean = 5
pvariance = 4
variance  = 32/7
pstdev ≈ 2.0
stdev  ≈ 2.138089935299395
```
`variance * (n-1) == pvariance * n == 32`. `stdev > pstdev`. The sample standard deviation uses Bessel's correction (N-1 degrees of freedom); the population standard deviation does not. Inputs are `Fraction` objects so variance/pvariance are exact; stdev floats are checked via `math.isclose(sqrt(expected_variance))` with squared round-trip verification.

**Q3 – mode vs multimode**
```
tied_a = [7,7,8,8,9,9]  → mode=7,  multimode=[7,8,9]
tied_b = [9,9,8,8,7,7]  → mode=9,  multimode=[9,8,7]
single = [7,7,7,8,9]    → mode=7,  multimode=[7]
```
Equal counts in both tied permutations. `mode()` and `multimode()` ordering follows first encounter, not numeric sorting.

**Q4 – quantiles inclusive vs exclusive**
```
data = [1..11], n=4
exclusive → [3.0, 6.0, 9.0]
inclusive → [3.5, 6.0, 8.5]
```
Q2/median identical; Q1/Q3 differ by 0.5. Exclusive assumes samples from a larger population; inclusive assumes you have the population extremes.

**Q5 – invalid / undersized inputs**

- `statistics.variance([42])` → `StatisticsError: variance requires at least two data points`
- `statistics.mean([])` → `StatisticsError: mean requires at least one data point`

Exception *types* are asserted in tests; message text is recorded here as an observation only (it can change across Python versions).

See `RESULTS.md` for the full machine-generated output.

---

## Running

```bash
python3 check.py
python3 -m unittest -v
```

Both should PASS.
