# check.py
# stdlib-only correctness checks for python-statistics-score-summary-lab

import math
import statistics
from collections import Counter
from fractions import Fraction

import cases


def run_q1():
    base_mean = statistics.mean(cases.Q1_BASE)
    base_median = statistics.median(cases.Q1_BASE)
    extreme_mean = statistics.mean(cases.Q1_EXTREME)
    extreme_median = statistics.median(cases.Q1_EXTREME)

    passed = (
        base_mean == cases.Q1_EXPECT["base_mean"]
        and base_median == cases.Q1_EXPECT["base_median"]
        and extreme_mean == cases.Q1_EXPECT["extreme_mean"]
        and extreme_median == cases.Q1_EXPECT["extreme_median"]
        and (extreme_mean - base_mean) == cases.Q1_EXPECT["mean_delta"]
        and (extreme_median - base_median) == cases.Q1_EXPECT["median_delta"]
    )

    return {
        "name": "Q1 mean vs median robustness",
        "passed": passed,
        "details": {
            "base": cases.Q1_BASE,
            "base_mean": base_mean,
            "base_median": base_median,
            "extreme": cases.Q1_EXTREME,
            "extreme_mean": extreme_mean,
            "extreme_median": extreme_median,
            "mean_delta": extreme_mean - base_mean,
            "median_delta": extreme_median - base_median,
        },
    }


def run_q2():
    data = cases.Q2_SCORES
    mean_val = statistics.mean(data)
    pvar = statistics.pvariance(data)
    var = statistics.variance(data)
    pstdev_val = statistics.pstdev(data)
    stdev_val = statistics.stdev(data)

    # Exact Fraction checks for mean / variance
    mean_ok = mean_val == cases.Q2_EXPECT["mean"]
    pvar_ok = pvar == cases.Q2_EXPECT["pvariance"]
    var_ok = var == cases.Q2_EXPECT["variance"]

    # Float stdev checks: compare against sqrt(expected_variance),
    # and check squared round-trip
    expected_pstdev = math.sqrt(float(cases.Q2_EXPECT["pvariance"]))
    expected_stdev = math.sqrt(float(cases.Q2_EXPECT["variance"]))

    pstdev_ok = math.isclose(pstdev_val, expected_pstdev, rel_tol=1e-15, abs_tol=0.0)
    stdev_ok = math.isclose(stdev_val, expected_stdev, rel_tol=1e-15, abs_tol=0.0)

    pstdev_squared_ok = math.isclose(
        pstdev_val * pstdev_val, float(cases.Q2_EXPECT["pvariance"]), rel_tol=1e-15
    )
    stdev_squared_ok = math.isclose(
        stdev_val * stdev_val, float(cases.Q2_EXPECT["variance"]), rel_tol=1e-15
    )

    # stdev > pstdev for n > 1 with non-zero spread
    order_ok = stdev_val > pstdev_val

    # population/sample variance identity: var*(n-1) == pvar*n
    n = cases.Q2_N
    identity_ok = (var * (n - 1) == pvar * n)

    passed = all(
        [
            mean_ok,
            pvar_ok,
            var_ok,
            pstdev_ok,
            stdev_ok,
            pstdev_squared_ok,
            stdev_squared_ok,
            order_ok,
            identity_ok,
        ]
    )

    return {
        "name": "Q2 stdev vs pstdev (sample vs population)",
        "passed": passed,
        "details": {
            "data": [str(x) for x in data],
            "data_input_type": type(data[0]).__name__ if data else None,
            "n": n,
            "mean": str(mean_val),
            "pvariance": str(pvar),
            "variance": str(var),
            "pvariance_ok": pvar_ok,
            "variance_ok": var_ok,
            "pstdev": pstdev_val,
            "stdev": stdev_val,
            "pstdev_squared_ok": pstdev_squared_ok,
            "stdev_squared_ok": stdev_squared_ok,
            "stdev_gt_pstdev": order_ok,
            "variance_identity_var*(n-1)==pvar*n": identity_ok,
        },
    }


def run_q3():
    def check_one(data, expect):
        mode_val = statistics.mode(data)
        multimode_val = statistics.multimode(data)
        mode_ok = mode_val == expect["mode"]
        multimode_ok = multimode_val == expect["multimode"]
        first_match_ok = mode_val == multimode_val[0] if multimode_val else False
        return {
            "data": data,
            "mode": mode_val,
            "multimode": multimode_val,
            "mode_ok": mode_ok,
            "multimode_ok": multimode_ok,
            "first_match_ok": first_match_ok,
            "passed": mode_ok and multimode_ok and first_match_ok,
        }

    a = check_one(cases.Q3_TIED_A, cases.Q3_TIED_A_EXPECT)
    b = check_one(cases.Q3_TIED_B, cases.Q3_TIED_B_EXPECT)
    single = check_one(cases.Q3_SINGLE, cases.Q3_SINGLE_EXPECT)

    # Compute frequency maps and verify they are identical
    counts_a = dict(Counter(cases.Q3_TIED_A))
    counts_b = dict(Counter(cases.Q3_TIED_B))
    tie_counts_equal = counts_a == counts_b

    # Ordering follows first encounter, not numeric sort
    tie_order_differs = a["multimode"] != b["multimode"]

    passed = (
        a["passed"]
        and b["passed"]
        and single["passed"]
        and tie_order_differs
        and tie_counts_equal
    )

    return {
        "name": "Q3 mode vs multimode (tied buckets)",
        "passed": passed,
        "details": {
            "tied_a": a,
            "tied_b": b,
            "single": single,
            "tie_order_differs_by_first_seen": tie_order_differs,
            "tie_counts_equal": tie_counts_equal,
            "counts_a": counts_a,
            "counts_b": counts_b,
        },
    }


def run_q4():
    data = cases.Q4_DATA
    excl = statistics.quantiles(data, n=cases.Q4_N, method="exclusive")
    incl = statistics.quantiles(data, n=cases.Q4_N, method="inclusive")

    excl_ok = excl == cases.Q4_EXPECT_EXCLUSIVE
    incl_ok = incl == cases.Q4_EXPECT_INCLUSIVE

    # Q2 / median is identical in both methods for this odd-length case
    median_same = excl[1] == incl[1] if len(excl) >= 2 and len(incl) >= 2 else False
    # Q1/Q3 differ
    ends_differ = excl[0] != incl[0] and excl[2] != incl[2]

    passed = excl_ok and incl_ok and median_same and ends_differ

    return {
        "name": "Q4 quantiles inclusive vs exclusive",
        "passed": passed,
        "details": {
            "data": data,
            "n": cases.Q4_N,
            "exclusive": excl,
            "inclusive": incl,
            "exclusive_ok": excl_ok,
            "inclusive_ok": incl_ok,
            "median_same": median_same,
            "ends_differ": ends_differ,
        },
    }


def run_q5():
    results = []
    all_passed = True
    for name, func_name, arg, expected_exc_name in cases.Q5_CASES:
        func = getattr(statistics, func_name)
        raised = False
        exc_type_name = None
        exc_msg = None
        try:
            func(arg)
        except Exception as e:
            raised = True
            exc_type_name = type(e).__name__
            exc_msg = str(e)

        # Pass condition: correct exception type is raised. Message is recorded, not asserted.
        passed = raised and exc_type_name == expected_exc_name
        all_passed = all_passed and passed
        results.append(
            {
                "case": name,
                "func": func_name,
                "arg": arg,
                "raised": raised,
                "exc_type": exc_type_name,
                "exc_message": exc_msg,
                "expected_exc": expected_exc_name,
                "passed": passed,
            }
        )

    return {
        "name": "Q5 invalid / undersized inputs",
        "passed": all_passed,
        "details": {"cases": results},
    }


def main():
    import sys
    import json

    rows = [
        run_q1(),
        run_q2(),
        run_q3(),
        run_q4(),
        run_q5(),
    ]

    # Print summary
    for r in rows:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"[{status}] {r['name']}")

    print()
    all_passed = all(r["passed"] for r in rows)
    print(f"Overall: {'PASS' if all_passed else 'FAIL'} ({sum(r['passed'] for r in rows)}/{len(rows)})")

    # Write RESULTS.md from the same structured rows
    with open("RESULTS.md", "w") as f:
        f.write("# RESULTS.md\n\n")
        f.write("Generated by `python3 check.py`.\n\n")
        for r in rows:
            status = "PASS" if r["passed"] else "FAIL"
            f.write(f"## {r['name']} – {status}\n\n")
            f.write("```\n")
            f.write(json.dumps(r["details"], indent=2, default=str))
            f.write("\n```\n\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
