#!/usr/bin/env python3
"""Exact, bounded checks for the EP817 unweighted ternary-variance refinement.

No floating-point arithmetic or external dependencies. Finite checks corroborate
notes/ternary-variance-lower-bound.md; they do not prove its general statements.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

BASE_COMMIT = "23c0110c95b5a2036bdc04a1f352b6e5e27742c8"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def digit_sums(a: tuple[int, ...], alphabet: int) -> set[int]:
    values = {0}
    for weight in a:
        values = {value + digit * weight for value in values for digit in range(alphabet)}
    return values


def has_four_ap(values: set[int]) -> bool:
    ordered = sorted(values)
    for i, start in enumerate(ordered):
        for second in ordered[i + 1:]:
            step = second - start
            if start + 3 * step > ordered[-1]:
                break
            if start + 2 * step in values and start + 3 * step in values:
                return True
    return False


def dot(x: tuple[int, ...], a: tuple[int, ...]) -> int:
    return sum(c * weight for c, weight in zip(x, a))


def minimal_blocks(a: tuple[int, ...]) -> list[tuple[int, ...]]:
    relations = []
    for c in product((-1, 0, 1), repeat=len(a)):
        if next((x for x in c if x), 0) != 1 or dot(c, a) != 0:
            continue
        mask = sum(1 << i for i, x in enumerate(c) if x)
        relations.append((mask, c))
    return [c for mask, c in relations
            if not any(other != mask and other & mask == other
                       for other, _ in relations)]


def multiply(p: dict[int, int], q: dict[int, int]) -> dict[int, int]:
    out: Counter[int] = Counter()
    for i, x in p.items():
        for j, y in q.items():
            out[i + j] += x * y
    return {i: x for i, x in out.items() if x}


def digit_polynomial(a: tuple[int, ...], alphabet: int) -> dict[int, int]:
    out = {0: 1}
    for weight in a:
        out = multiply(out, {digit * weight: 1 for digit in range(alphabet)})
    return out


def block_polynomial(a: tuple[int, ...], shift_error: int = 0) -> dict[int, int]:
    require(sum(a) % 2 == 0, "block weight sum is not even")
    out = digit_polynomial(a, 3)
    shift = sum(a) // 2 + shift_error
    for exponent, coefficient in digit_polynomial(a, 2).items():
        target = exponent + shift
        out[target] = out.get(target, 0) - coefficient
    return {i: x for i, x in out.items() if x}


def kappa(m: int) -> Fraction:
    require(m >= 3, "minimal block must have at least three coordinates")
    return Fraction(8 * 3**m - 3 * 2**m, 12 * (3**m - 2**m))


def minimum_classes(n: int) -> int:
    q, r = divmod(n, 3)
    return 19**q * 3**r


def squared_sum_max(n: int, upper: int) -> int:
    return (n * upper**2 - n * (n - 1) * upper
            + n * (n - 1) * (2 * n - 1) // 6)


def finite_lower(n: int) -> int:
    require(n > 0, "n must be positive")
    m = minimum_classes(n)
    interval = (m + n * (n - 1) - 1 + 2 * n - 1) // (2 * n)
    lo, hi = n - 1, max(n, interval)
    def valid(upper: int) -> bool:
        return 192 * squared_sum_max(n, upper) >= 19 * (m * m - 1)
    while not valid(hi):
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if valid(mid):
            hi = mid
        else:
            lo = mid
    return max(n, interval, hi)


def check_set(a: tuple[int, ...]) -> dict[str, object]:
    require(bool(a) and tuple(sorted(set(a))) == a and a[0] > 0,
            "generators must be sorted, distinct and positive")
    require(not has_four_ap(digit_sums(a, 2)), f"not admissible: {a}")
    blocks = minimal_blocks(a)
    covered: set[int] = set()
    polynomial = {0: 1}
    variance = Fraction(0)
    shape = []
    for block in blocks:
        indices = {i for i, c in enumerate(block) if c}
        require(not covered & indices, f"overlapping minimal blocks: {a}")
        covered |= indices
        weights = tuple(a[i] for i in sorted(indices))
        size = len(indices)
        shape.append(size)
        polynomial = multiply(polynomial, block_polynomial(weights))
        variance += kappa(size) * sum(x * x for x in weights)
    free = tuple(weight for i, weight in enumerate(a) if i not in covered)
    polynomial = multiply(polynomial, digit_polynomial(free, 3))
    variance += Fraction(2, 3) * sum(x * x for x in free)

    actual_kernel = {c for c in product(range(-2, 3), repeat=len(a)) if dot(c, a) == 0}
    predicted_kernel = {
        tuple(sum(s * b[i] for s, b in zip(scalars, blocks)) for i in range(len(a)))
        for scalars in product(range(-2, 3), repeat=len(blocks))
    }
    require(actual_kernel == predicted_kernel, f"short-kernel mismatch: {a}")
    values = digit_sums(a, 3)
    require(polynomial == {value: 1 for value in values}, f"unweighted polynomial mismatch: {a}")
    size, center = len(values), sum(a)
    require(sum(values) == size * center, f"incorrect center: {a}")
    direct_variance = Fraction(sum((value - center)**2 for value in values), size)
    require(variance == direct_variance, f"moment mismatch: {a}")
    expected_size = 3**len(free)
    for m in shape:
        expected_size *= 3**m - 2**m
    require(size == expected_size, f"cardinality mismatch: {a}")
    require(size >= minimum_classes(len(a)), f"residue lower count failed: {a}")
    require((size == minimum_classes(len(a))) ==
            (len(shape) == len(a) // 3 and all(m == 3 for m in shape)),
            f"equality characterization failed: {a}")
    require(Fraction(size * size - 1, 12) <= variance, f"integer variance bound failed: {a}")
    require(variance <= Fraction(16, 19) * sum(x * x for x in a), f"variance cap failed: {a}")
    require(19 * (size * size - 1) <= 192 * sum(x * x for x in a), f"squared bound failed: {a}")
    require(finite_lower(len(a)) <= max(a), f"finite bound failed: {a}")
    return {"generators": list(a), "block_sizes": sorted(shape), "classes": size,
            "variance": str(variance)}


def abstract_checks() -> dict[str, object]:
    minima = [1]
    for n in range(1, 201):
        minima.append(min([3 * minima[n - 1]] +
                          [(3**m - 2**m) * minima[n - m] for m in range(3, n + 1)]))
        require(minima[n] == minimum_classes(n), f"partition optimizer failed: {n}")
    for m in range(3, 257):
        require(kappa(m) <= Fraction(16, 19), f"kappa cap failed: {m}")
        require(3**m - 2**m >= 19 * 3**(m - 3), f"block lower count failed: {m}")
    cubes = []
    for m in range(3, 9):
        coefficients = tuple(range(1, m)) + (-m * (m - 1) // 2,)
        moments = [dot(z, coefficients) for z in product(range(3), repeat=m) if min(z) == 0]
        require(len(moments) == 3**m - 2**m, "canonical count failed")
        require(sum(moments) == 0, "canonical mean failed")
        require(Fraction(sum(x * x for x in moments), len(moments)) ==
                kappa(m) * sum(c * c for c in coefficients), "canonical moment failed")
        cubes.append({"dimension": m, "canonical_vectors": len(moments)})
    base = (1, 4, 5)
    require(Fraction(2, 3) * sum(x * x for x in base) != kappa(3) * sum(x * x for x in base),
            "weighted/unweighted regression did not distinguish distributions")
    require(block_polynomial(base, shift_error=1) != {x: 1 for x in digit_sums(base, 3)},
            "wrong-shift mutation went undetected")
    rejected = 0
    for bad in ((1, 2, 3), (1, 1), (0, 1), ()):
        try:
            check_set(bad)
        except AssertionError:
            rejected += 1
        else:
            raise AssertionError(f"invalid-input regression failed: {bad}")
    return {"partition_optimizer_through_n": 200, "coefficient_cap_through_m": 256,
            "canonical_cubes": cubes, "regressions_passed": 2 + rejected}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--universe-max", type=int, default=24)
    parser.add_argument("--size-max", type=int, default=5)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not 1 <= args.size_max <= 7 or not 1 <= args.universe_max <= 40:
        parser.error("bounded runner requires size-max in [1,7] and universe-max in [1,40]")
    counts: Counter[int] = Counter()
    shapes: Counter[str] = Counter()
    digest = hashlib.sha256()
    candidates = 0
    for n in range(1, args.size_max + 1):
        for a in combinations(range(1, args.universe_max + 1), n):
            candidates += 1
            if has_four_ap(digit_sums(a, 2)):
                continue
            result = check_set(a)
            counts[n] += 1
            shapes[str(result["block_sizes"])] += 1
            digest.update((json.dumps(result, sort_keys=True) + "\n").encode())
    targeted = [(1, 7, 8, 19, 133, 152), (1, 7, 8, 19, 57),
                (1, 4, 5, 41, 205, 1025, 1271)]
    for m in range(3, 7):
        prefix = tuple(5**i for i in range(m - 1))
        targeted.append(prefix + (sum(prefix),))
    report = {
        "schema": "ep817-ternary-variance-certificate-v1", "status": "PASS",
        "base_commit": BASE_COMMIT, "lean_checked": False,
        "scope": "Exact bounded computations; general proof is in the companion note.",
        "exhaustive_domain": {"universe": [1, args.universe_max], "max_size": args.size_max,
                              "candidate_sets": candidates, "admissible_sets": sum(counts.values()),
                              "counts_by_size": {str(n): counts[n] for n in range(1, args.size_max + 1)},
                              "block_shapes": dict(sorted(shapes.items())),
                              "transcript_sha256": digest.hexdigest()},
        "targeted_cases": [check_set(a) for a in targeted],
        "abstract_checks": abstract_checks(),
        "finite_lower_table": {str(n): finite_lower(n) for n in (1, 2, 3, 4, 5, 6, 9, 12, 30)},
        "validator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
