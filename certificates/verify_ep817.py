#!/usr/bin/env python3
"""Deterministic exact checks for the EP817 k=4 rate proof.

The general theorem is proved in the accompanying paper.  This program checks
the finite modular objects, small lifted languages, deletion heredity, diagonal
orbit counts, and (with --extended) the lower-bound block classification on a
bounded exhaustive domain.  It uses integers only and has no dependencies.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path

if not __debug__:
    raise SystemExit(
        "FAIL CLOSED: Python assertions are disabled; rerun without -O."
    )

P = 19
BLOCK = (1, 7, 8)
DIGITS = frozenset((0, 1, 7, 8, 9, 15, 16))
COEFFICIENTS = tuple(range(-2, 3))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def subset_sums(generators: tuple[int, ...]) -> set[int]:
    values = {0}
    for generator in generators:
        values |= {value + generator for value in tuple(values)}
    return values


def ternary_sums(generators: tuple[int, ...]) -> set[int]:
    return {
        sum(c * a for c, a in zip(coefficients, generators))
        for coefficients in product(range(3), repeat=len(generators))
    }


def four_ap_witness(values: set[int]) -> tuple[int, int] | None:
    ordered = sorted(values)
    for index, start in enumerate(ordered):
        for second in ordered[index + 1 :]:
            step = second - start
            if start + 2 * step in values and start + 3 * step in values:
                return start, step
    return None


def support(vector: tuple[int, ...]) -> frozenset[int]:
    return frozenset(index for index, value in enumerate(vector) if value)


def canonical_sign(vector: tuple[int, ...]) -> tuple[int, ...]:
    for value in vector:
        if value:
            return vector if value > 0 else tuple(-x for x in vector)
    raise ValueError("zero vector has no canonical sign")


def minimal_signed_relations(
    generators: tuple[int, ...],
) -> list[tuple[int, ...]]:
    relations = [
        coefficients
        for coefficients in product((-1, 0, 1), repeat=len(generators))
        if any(coefficients)
        and sum(c * a for c, a in zip(coefficients, generators)) == 0
    ]
    minimal = [
        relation
        for relation in relations
        if not any(support(other) < support(relation) for other in relations)
    ]
    return sorted({canonical_sign(relation) for relation in minimal})


def check_lower_structure(generators: tuple[int, ...]) -> tuple[int, ...]:
    blocks = minimal_signed_relations(generators)
    for index, first in enumerate(blocks):
        for second in blocks[index + 1 :]:
            require(
                not (support(first) & support(second)),
                f"overlapping minimal blocks for {generators}: {first}, {second}",
            )

    coordinate_block: dict[int, tuple[int, ...]] = {}
    for block in blocks:
        for index in support(block):
            coordinate_block[index] = block

    actual_short_kernel = {
        coefficients
        for coefficients in product(COEFFICIENTS, repeat=len(generators))
        if sum(c * a for c, a in zip(coefficients, generators)) == 0
    }
    proposed_short_kernel: set[tuple[int, ...]] = set()
    for scalars in product(COEFFICIENTS, repeat=len(blocks)):
        vector = [0] * len(generators)
        for scalar, block in zip(scalars, blocks):
            for index, sign in enumerate(block):
                vector[index] += scalar * sign
        require(
            all(value in COEFFICIENTS for value in vector),
            "disjoint block combination left coefficient box",
        )
        proposed_short_kernel.add(tuple(vector))
    require(
        actual_short_kernel == proposed_short_kernel,
        f"short-kernel mismatch for {generators}",
    )

    covered = sum(len(support(block)) for block in blocks)
    expected_count = 3 ** (len(generators) - covered)
    for block in blocks:
        size = len(support(block))
        require(size >= 3, f"block smaller than three for {generators}: {block}")
        expected_count *= 3**size - 2**size
    require(
        len(ternary_sums(generators)) == expected_count,
        f"ternary quotient count mismatch for {generators}",
    )
    return tuple(sorted(len(support(block)) for block in blocks))


def finite_modular_checks() -> dict[str, object]:
    kernel = sorted(
        (u, v, w)
        for u, v, w in product(COEFFICIENTS, repeat=3)
        if (u + 7 * v + 8 * w) % P == 0
    )
    expected = sorted((t, t, -t) for t in COEFFICIENTS)
    require(kernel == expected, f"bounded kernel mismatch: {kernel}")

    modular_aps = [
        (start, step, tuple((start + index * step) % P for index in range(4)))
        for start in range(P)
        for step in range(1, P)
        if all((start + index * step) % P in DIGITS for index in range(4))
    ]
    require(not modular_aps, f"nonconstant modular APs found: {modular_aps}")

    second_difference_solutions = [
        values
        for values in product(sorted(DIGITS), repeat=4)
        if (values[0] - 2 * values[1] + values[2]) % P == 0
        and (values[1] - 2 * values[2] + values[3]) % P == 0
    ]
    constants = [(digit,) * 4 for digit in sorted(DIGITS)]
    require(
        second_difference_solutions == constants,
        "digit second-difference rigidity failed",
    )
    return {
        "bounded_coefficient_triples_tested": len(COEFFICIENTS) ** 3,
        "bounded_kernel": kernel,
        "modular_ap_parameters_tested": P * (P - 1),
        "nonconstant_modular_aps": len(modular_aps),
        "digit_quadruples_tested": len(DIGITS) ** 4,
        "digit_second_difference_solutions": second_difference_solutions,
    }


def lifted_and_deletion_checks() -> dict[str, object]:
    lifted_sizes: dict[int, int] = {}
    for blocks in range(1, 5):
        generators = tuple(
            P**position * value
            for position in range(blocks)
            for value in BLOCK
        )
        from_generators = subset_sums(generators)
        from_digits = {
            sum(digit * P**position for position, digit in enumerate(digits))
            for digits in product(sorted(DIGITS), repeat=blocks)
        }
        require(from_generators == from_digits, f"digit equality failed at m={blocks}")
        require(len(from_generators) == len(DIGITS) ** blocks, "digit collision")
        require(four_ap_witness(from_generators) is None, f"lifted AP at m={blocks}")
        lifted_sizes[blocks] = len(from_generators)

    deletion_choices = 0
    for n in range(1, 10):
        blocks = (n + 2) // 3
        source = tuple(
            P**position * value
            for position in range(blocks)
            for value in BLOCK
        )
        source_sums = subset_sums(source)
        surplus = 3 * blocks - n
        for removed_indices in combinations(range(3 * blocks), surplus):
            removed = set(removed_indices)
            retained = tuple(
                value for index, value in enumerate(source) if index not in removed
            )
            deletion_choices += 1
            retained_sums = subset_sums(retained)
            require(retained_sums <= source_sums, "subset-sum heredity failed")
            require(four_ap_witness(retained_sums) is None, "deletion created an AP")
            require(max(retained) <= 8 * P ** (blocks - 1), "upper constant failed")

    diagonal_counts = {}
    for size in range(1, 11):
        representatives = {
            tuple(value - min(vector) for value in vector)
            for vector in product(range(3), repeat=size)
        }
        expected = 3**size - 2**size
        require(len(representatives) == expected, f"diagonal count failed at m={size}")
        diagonal_counts[size] = expected
    return {
        "lifted_language_sizes": lifted_sizes,
        "exact_deletion_choices": deletion_choices,
        "diagonal_counts_through_m10": diagonal_counts,
    }


def extended_lower_check(universe_max: int, size_max: int) -> dict[str, object]:
    total = 0
    by_size: Counter[int] = Counter()
    block_shapes: Counter[tuple[int, ...]] = Counter()
    for size in range(1, size_max + 1):
        for generators in combinations(range(1, universe_max + 1), size):
            if four_ap_witness(subset_sums(generators)) is not None:
                continue
            shape = check_lower_structure(generators)
            total += 1
            by_size[size] += 1
            block_shapes[shape] += 1
    return {
        "universe": [1, universe_max],
        "maximum_set_size": size_max,
        "admissible_sets_checked": total,
        "counts_by_size": {str(size): by_size[size] for size in range(1, size_max + 1)},
        "minimal_block_shapes": {
            str(key): value for key, value in sorted(block_shapes.items())
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--extended", action="store_true")
    parser.add_argument("--universe-max", type=int, default=18)
    parser.add_argument("--size-max", type=int, default=5)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if args.universe_max <= 0:
        parser.error("--universe-max must be a positive integer")
    if args.size_max <= 0:
        parser.error("--size-max must be a positive integer")

    report: dict[str, object] = {
        "schema": "ep817-certificate-v1",
        "status": "PASS",
        "finite_modular": finite_modular_checks(),
        "lifting_and_deletion": lifted_and_deletion_checks(),
    }
    if args.extended:
        report["extended_lower_structure"] = extended_lower_check(
            args.universe_max, args.size_max
        )

    source_bytes = Path(__file__).read_bytes()
    report["validator_sha256"] = hashlib.sha256(source_bytes).hexdigest()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")


if __name__ == "__main__":
    main()
