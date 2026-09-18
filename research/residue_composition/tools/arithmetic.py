#!/usr/bin/env python3
"""Exact arithmetic for residue and composition certificates.

Only Python's standard library is required. Original weights, radices, masks,
word multiplicities, and generator counts remain explicit. Comparisons between
rational linear combinations of logarithms use integer powers, not floats.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from math import gcd

AB = ((10, (1, 3)), (10, (2, 4)))


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def image(weights, q):
    require(q >= 2, 'coefficient arity at least two')
    out = {0}
    for a in weights:
        require(a > 0, 'positive generator required')
        out = {x + j*a for x in out for j in range(q)}
    return tuple(sorted(out))


def masks(weights):
    out = {}
    for mask in range(1 << len(weights)):
        x = sum(a for i, a in enumerate(weights) if mask >> i & 1)
        out.setdefault(x, []).append(mask)
    return out


def modular_witness(weights, b, k):
    require(k >= 3 and b > sum(weights), 'canonical modular input')
    mu = masks(weights)
    for x in sorted(mu):
        for y in sorted(mu):
            if x == y:
                continue
            d = (y-x) % b
            points = [(x+i*d) % b for i in range(k)]
            if all(z in mu for z in points):
                return {'start': x, 'step': d, 'points': points,
                        'subset_masks': [mu[z][0] for z in points]}
    return None


def shapes(q):
    require(q >= 2, 'invalid coefficient arity')
    out = set()
    for mask in range(1 << (q-2)):
        r = (0,) + tuple(j+1 for j in range(q-2) if mask >> j & 1)
        out.add(min(r, tuple(sorted(r[-1]-x for x in r))))
    return tuple(sorted(out, key=lambda r: (r[-1], len(r), r)))


def matrix(weights, b, q=5):
    require(weights and tuple(sorted(set(weights))) == tuple(weights), 'ordered distinct generators')
    require(b > sum(weights), 'canonical radix condition')
    D, rs = image(weights, q), shapes(q)
    index = {r: i for i, r in enumerate(rs)}
    out = []
    for r in rs:
        fibers = defaultdict(set)
        for x in {d+e for d in D for e in r}:
            fibers[x % b].add(x // b)
        row = [0]*len(rs)
        for fiber in fibers.values():
            h = min(fiber)
            s = tuple(sorted(x-h for x in fiber))
            s = min(s, tuple(sorted(s[-1]-x for x in s)))
            require(s in index, 'receiving shift support left proved domain')
            row[index[s]] += 1
        out.append(tuple(row))
    return tuple(out)


def rm(row, M):
    out = [0]*len(M)
    for i, x in enumerate(row):
        if x:
            for j, y in enumerate(M[i]):
                out[j] += x*y
    return tuple(out)


def mm(A, B):
    return tuple(tuple(sum(x*y for x,y in zip(row,col)) for col in zip(*B)) for row in A)


def eye(n):
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))


def power(M, n):
    require(n >= 0, 'negative matrix power')
    out = eye(len(M))
    while n:
        if n & 1:
            out = mm(out, M)
        n //= 2
        if n:
            M = mm(M, M)
    return out


def word_count(dictionary, word, q=5):
    Ms = [matrix(A,b,q) for b,A in dictionary]
    row = (1,) + (0,)*(len(Ms[0])-1)
    reward = 0
    for i in word:
        require(0 <= i < len(dictionary), 'word letter outside dictionary')
        row = rm(row, Ms[i])
        reward += len(dictionary[i][1])
    return sum(x*len(r) for x,r in zip(row,shapes(q))), reward


def generators(dictionary, word, keep=None):
    P, out = 1, []
    for j,i in enumerate(word):
        b,A = dictionary[i]
        if keep is None or j in keep:
            out.extend(P*a for a in A)
        P *= b
    require(len(out) == len(set(out)), 'generator collision across levels')
    return tuple(sorted(out)), P


def crossing(a,b):
    require(a >= 1 and b >= 1, 'positive crossed run lengths')
    x = 8*10**(a+b) + 4*10**b - 3
    require(x % 9 == 0, 'crossing divisibility')
    return x//9


def minimum(s,t):
    require(s >= 0 and t >= 0, 'negative composition')
    if not s+t:
        return 1
    if not t:
        return (16*10**s-7)//9
    if not s:
        return (4*10**t-1)//3
    if s >= t:
        a,r = divmod(s,t)
        return crossing(a,1)**(t-r)*crossing(a+1,1)**r
    return 93**(s-1)*crossing(1,t-s+1)


def attainer(s,t):
    require(s >= 0 and t >= 0, 'negative composition')
    if not s:
        return (1,)*t
    if not t:
        return (0,)*s
    if s >= t:
        a,r = divmod(s,t)
        return ((1,)+(0,)*a)*(t-r) + ((1,)+(0,)*(a+1))*r
    return (1,)*(t-s+1)+(0,)+(1,0)*(s-1)


# Expressions are sum_{b>=2} c_b log(b), with exact rational c_b.
def tidy(x):
    return {int(b): Fraction(c) for b,c in x.items() if c and b != 1}


def logint(n):
    require(n >= 1, 'logarithm input must be positive')
    return {} if n == 1 else {n: Fraction(1)}


def add(*expressions):
    out = {}
    for expr in expressions:
        for b,c in expr.items():
            out[b] = out.get(b,Fraction(0))+c
    return tidy(out)


def scale(c, expr):
    return tidy({b: Fraction(c)*v for b,v in expr.items()})


def compare(x,y):
    diff = add(x,scale(-1,y))
    L = 1
    for c in diff.values():
        L = L*c.denominator//gcd(L,c.denominator)
    numerator, denominator = 1,1
    for b,c in diff.items():
        e = int(L*c)
        if e > 0:
            numerator *= b**e
        else:
            denominator *= b**(-e)
    return (numerator > denominator)-(numerator < denominator)


def encode(expr):
    return [[b,str(c)] for b,c in sorted(expr.items())]


def decode(expr):
    return tidy({int(b): Fraction(c) for b,c in expr})


def spectrum(p):
    """Exact logarithmic count cost per level, at B frequency p."""
    p = Fraction(p)
    require(0 <= p <= 1, 'frequency outside simplex')
    if p == 0 or p == 1:
        return logint(10)
    if p >= Fraction(1,2):
        return add(scale(1-p,logint(93)),scale(2*p-1,logint(10)))
    r = (1-p)/p
    a = r.numerator//r.denominator
    u = r-a
    return add(scale(p*(1-u),logint(crossing(a,1))),
               scale(p*u,logint(crossing(a+1,1))))


def inverse(M):
    n = len(M)
    A = [[Fraction(x) for x in row] + [Fraction(i == j) for j in range(n)]
         for i,row in enumerate(M)]
    for j in range(n):
        pivot = next((i for i in range(j,n) if A[i][j]), None)
        if pivot is None:
            return None
        A[j], A[pivot] = A[pivot], A[j]
        d = A[j][j]
        A[j] = [x/d for x in A[j]]
        for i in range(n):
            if i != j and A[i][j]:
                d = A[i][j]
                A[i] = [x-d*y for x,y in zip(A[i],A[j])]
    return tuple(tuple(row[n:]) for row in A)


def finite_points(dictionary,q,m):
    d = len(dictionary)
    Ms = [matrix(A,b,q) for b,A in dictionary]
    v = tuple(len(r) for r in shapes(q))
    states = {((1,)+(0,)*(len(v)-1),(0,)*d): ((),1)}
    for _ in range(m):
        nxt = {}
        for (row,counts),(word,mass) in states.items():
            for i,M in enumerate(Ms):
                c = list(counts); c[i] += 1; c = tuple(c)
                key, w = (rm(row,M),c), word+(i,)
                if key in nxt:
                    old,number = nxt[key]
                    nxt[key] = (min(old,w),number+mass)
                else:
                    nxt[key] = (w,mass)
        states = nxt
    require(sum(v[1] for v in states.values()) == d**m, 'literal word count was lost')
    points = {}
    for (row,c),(word,mass) in states.items():
        F = sum(x*y for x,y in zip(row,v))
        if c not in points or (F,word) < points[c]:
            points[c] = (F,word)
    return points,len(states)


def composition_lp(dictionary,q,m,profile):
    p = tuple(Fraction(x) for x in profile)
    d = len(dictionary)
    require(m >= 1 and len(p) == d and min(p) >= 0 and sum(p) == 1, 'invalid LP input')
    points,states = finite_points(dictionary,q,m)
    keys = sorted(points)
    examined = 0
    for basis in combinations(keys,d):
        inv = inverse(tuple(tuple(basis[j][i] for j in range(d)) for i in range(d)))
        if inv is None:
            continue
        lam = tuple(sum(inv[i][j]*m*p[j] for j in range(d)) for i in range(d))
        if min(lam) < 0:
            continue
        examined += 1
        logs = tuple(logint(points[c][0]) for c in basis)
        dual = tuple(add(*(scale(inv[j][i],logs[j]) for j in range(d))) for i in range(d))
        if any(compare(add(*(scale(c[i],dual[i]) for i in range(d))),logint(points[c][0])) > 0 for c in keys):
            continue
        value = add(*(scale(p[i],dual[i]) for i in range(d)))
        primal = add(*(scale(lam[j]/m,logs[j]) for j in range(d)))
        require(sum(lam) == 1 and compare(value,primal) == 0, 'LP certificate inconsistency')
        return {'q':q,'horizon':m,
                'dictionary':[{'radix':b,'weights':list(A)} for b,A in dictionary],
                'profile':[str(x) for x in p],
                'points':[{'counts':list(c),'image_count':points[c][0],'word':list(points[c][1])} for c in keys],
                'basis':[list(c) for c in basis],'mixture':[str(x) for x in lam],
                'dual_prices':[encode(x) for x in dual],
                'upper_log_per_level':encode(value),
                'lower_log_per_level':encode(add(value,scale(Fraction(-1,m),logint(q-1)))),
                'mean_reward':str(sum(p[i]*len(dictionary[i][1]) for i in range(d))),
                'literal_words':d**m,'row_count_states':states,
                'feasible_bases_examined':examined}
    raise AssertionError('No primal/dual basis found')


def phase_word(p,stages):
    p = Fraction(p)
    require(Fraction(1,2) < p < 1 and stages >= 1, 'phase-separated domain')
    word = []
    for j in range(1,stages+1):
        a = ((1-p)*j).__floor__()
        b = ((2*p-1)*j).__floor__()
        word.extend((1,0)*a)
        word.extend((1,)*b)
    return tuple(word)
