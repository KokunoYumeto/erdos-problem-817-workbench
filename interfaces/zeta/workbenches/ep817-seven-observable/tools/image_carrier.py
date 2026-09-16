#!/usr/bin/env python3
"""Exact translated-image carriers. Standard-library arithmetic only.

Every residue translation is returned with its actual offset. Symmetry reduction
is explicit and is used only for a centrally symmetric source/tail. The code
counts distinct numerical values, not original word multiplicities.
"""
from __future__ import annotations
from collections import defaultdict
from itertools import combinations
from math import comb
from typing import Iterable


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def image(weights: Iterable[int], q: int) -> tuple[int, ...]:
    require(q >= 2, "coefficient arity must be at least two")
    values = {0}
    for a in weights:
        values = {v + c * a for v in values for c in range(q)}
    return tuple(sorted(values))


def image_masses(weights: Iterable[int], q: int) -> dict[int, int]:
    masses = {0: 1}
    for a in weights:
        nxt: dict[int, int] = defaultdict(int)
        for v, mass in masses.items():
            for c in range(q):
                nxt[v + c * a] += mass
        masses = dict(nxt)
    return masses


def translated_shape(values: Iterable[int]) -> tuple[int, tuple[int, ...]]:
    values = tuple(sorted(set(values)))
    require(bool(values), "empty support has no translation coordinate")
    shift = values[0]
    return shift, tuple(x - shift for x in values)


def reflection(shape: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(shape[-1] - x for x in shape))


def shape_basis(q: int, symmetric: bool = False) -> tuple[tuple[int, ...], ...]:
    require(q >= 2, "invalid arity")
    width = q - 2
    shapes = [(0,) + tuple(j + 1 for j in range(width) if bits >> j & 1)
              for bits in range(1 << width)]
    if symmetric:
        shapes = list({min(R, reflection(R)) for R in shapes})
    return tuple(sorted(shapes, key=lambda R: (R[-1], len(R), R)))


def is_symmetric(values: Iterable[int]) -> bool:
    values = set(values)
    return bool(values) and {min(values) + max(values) - x for x in values} == values


def observed(values: Iterable[int], q: int, symmetric: bool = False, moment: int = 0) -> list[int]:
    values = tuple(values)
    require(bool(values), "observed numerical source must be nonempty")
    if symmetric:
        require(moment == 0 and is_symmetric(values), "invalid reflection reduction")
    return [sum(x**moment for x in {y + r for y in values for r in R})
            for R in shape_basis(q, symmetric)]


def carrier(digits: Iterable[int], base: int, q: int, symmetric: bool = False) -> tuple[list[list[int]], list[list[dict]]]:
    D = tuple(sorted(set(digits)))
    require(base >= 2 and q >= 2 and bool(D), "invalid finite carrier input")
    require(D[0] >= 0 and D[-1] <= (q - 1) * (base - 1), "actual digits leave stated range")
    if symmetric:
        require(is_symmetric(D), "source is not centrally symmetric")
    basis = shape_basis(q, symmetric)
    indices = {R: i for i, R in enumerate(basis)}
    matrix: list[list[int]] = []
    labels: list[list[dict]] = []
    for R in basis:
        E = {d + r for d in D for r in R}
        fibers: dict[int, set[int]] = defaultdict(set)
        for x in E:
            fibers[x % base].add(x // base)
        row = [0] * len(basis)
        row_labels = []
        for z, fiber in sorted(fibers.items()):
            h, F = translated_shape(fiber)
            reflected = symmetric and reflection(F) < F
            target = reflection(F) if reflected else F
            row[indices[target]] += 1
            row_labels.append({"residue": z, "quotients": sorted(fiber), "translation": h,
                               "shape_before_reflection": list(F), "reflected": reflected,
                               "target": indices[target], "offset": z + base * h})
        require(sum(row) <= base, "residue labels exceed base")
        matrix.append(row)
        labels.append(row_labels)
    return matrix, labels


def mv(M: list[list[int]], v: list[int]) -> list[int]:
    return [sum(a * b for a, b in zip(row, v)) for row in M]


def mm(A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
    return [[sum(x * y for x, y in zip(row, column)) for column in zip(*B)] for row in A]


def identity(n: int) -> list[list[int]]:
    return [[int(i == j) for j in range(n)] for i in range(n)]


def power(M: list[list[int]], n: int) -> list[list[int]]:
    require(n >= 0, "negative matrix exponent")
    out = identity(len(M))
    while n:
        if n & 1:
            out = mm(out, M)
        n >>= 1
        if n:
            M = mm(M, M)
    return out


def moment_step(labels: list[list[dict]], base: int, moments: list[list[int]]) -> list[list[int]]:
    """Raw (unreflected) moments. Each affine residue map is retained."""
    require(all(not lab["reflected"] for row in labels for lab in row), "raw moments require unreflected labels")
    top = len(moments) - 1
    out = [[0] * len(labels) for _ in range(top + 1)]
    for p in range(top + 1):
        for i, row in enumerate(labels):
            out[p][i] = sum(comb(p, j) * lab["offset"] ** (p - j) * base**j * moments[j][lab["target"]]
                            for lab in row for j in range(p + 1))
    return out


def polynomial_matrix(coefficients: list[int], M: list[list[int]]) -> list[list[int]]:
    """Coefficients in descending degree, evaluated without floating point."""
    I = identity(len(M))
    out = [[0] * len(M) for _ in M]
    for c in coefficients:
        out = mm(out, M)
        out = [[x + c * I[i][j] for j, x in enumerate(row)] for i, row in enumerate(out)]
    return out


def bareiss(A: list[list[int]]) -> int:
    a = [row[:] for row in A]
    n = len(a)
    if not n:
        return 1
    sign, old = 1, 1
    for k in range(n - 1):
        pivot = next((j for j in range(k, n) if a[j][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        p = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * p - a[i][k] * a[k][j]
                require(numerator % old == 0, "fraction-free determinant lost divisibility")
                a[i][j] = numerator // old
            a[i][k] = 0
        old = p
    return sign * a[-1][-1]


def union_to_pattern(q: int) -> list[list[int]]:
    basis = shape_basis(q)
    idx = {R: i for i, R in enumerate(basis)}
    M = []
    for R in basis:
        row = [0] * len(basis)
        for n in range(1, len(R) + 1):
            for T in combinations(R, n):
                _, Q = translated_shape(-t for t in T)
                row[idx[Q]] += (-1) ** (n + 1)
        M.append(row)
    return M


def occurrences(Y: Iterable[int], pattern: tuple[int, ...]) -> int:
    Y = set(Y)
    return sum(all(a + r in Y for r in pattern) for a in Y)


def bit_image(weights: Iterable[int], q: int) -> int:
    bits = 1
    for a in weights:
        nxt = 0
        for c in range(q):
            nxt |= bits << (a * c)
        bits = nxt
    return bits


def has_ap(values: Iterable[int], k: int) -> bool:
    xs = sorted(set(values))
    present = set(xs)
    for i, x in enumerate(xs):
        for y in xs[i + 1:]:
            d = y - x
            if x + (k - 1) * d > xs[-1]:
                break
            if all(x + j * d in present for j in range(2, k)):
                return True
    return False
