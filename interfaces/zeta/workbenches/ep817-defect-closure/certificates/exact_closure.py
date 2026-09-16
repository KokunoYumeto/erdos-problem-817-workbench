#!/usr/bin/env python3
"""Exact finite-source progression closure and integer observation construction.

Standard-library only. Source vectors and witnesses remain literal integers;
Gaussian elimination is used only to certify rational span membership. Every
returned membership coefficient refers to the retained original basis vectors.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd, lcm
from typing import Sequence

Vector = tuple[int, ...]

def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)

def dot(a, b):
    return sum(x*y for x,y in zip(a,b))

def sub(a,b):
    return tuple(x-y for x,y in zip(a,b))

def rref(rows, n):
    a=[[F(x) for x in row] for row in rows]
    p=[]; at=0
    for col in range(n):
        row=next((j for j in range(at,len(a)) if a[j][col]),None)
        if row is None: continue
        a[at],a[row]=a[row],a[at]
        v=a[at][col];a[at]=[x/v for x in a[at]]
        for j in range(len(a)):
            if j!=at and a[j][col]:
                v=a[j][col];a[j]=[x-v*y for x,y in zip(a[j],a[at])]
        p.append(col);at+=1
        if at==len(a):break
    return a,p

def coefficients(basis, v):
    """One rational expression for v in the supplied original rows, or None."""
    n=len(v); d=len(basis)
    if d==0:return [] if not any(v) else None
    a,p=rref([[basis[j][i] for j in range(d)]+[v[i]] for i in range(n)],d)
    if any(not any(row[:d]) and row[d] for row in a): return None
    sol=[F(0)]*d
    for row,col in zip(a,p):sol[col]=row[d]
    require(all(sum(sol[j]*basis[j][i] for j in range(d))==v[i] for i in range(n)),
            'span expression failed')
    return sol

def independent(rows, n):
    ans=[]
    for row in rows:
        row=tuple(row)
        if coefficients(ans,row) is None:ans.append(row)
    return ans

def annihilator(basis,n):
    a,p=rref(basis,n); free=[i for i in range(n) if i not in p]; ans=[]
    for col in free:
        v=[F(0)]*n;v[col]=1
        for row,j in zip(a,p):v[j]=-row[col]
        scale=lcm(*(x.denominator for x in v))
        ans.append(tuple(int(scale*x) for x in v))
    require(all(dot(v,w)==0 for v in ans for w in basis),'annihilator failed')
    return ans

def projected_progressions(source,basis,k):
    """Enumerate numerical tuples in the rational quotient, with actual lifts."""
    n=len(source[0]); Q=annihilator(basis,n); fibres={}
    for s in sorted(set(source)):fibres.setdefault(tuple(dot(a,s) for a in Q),s)
    points=sorted(fibres)
    for i,x in enumerate(points):
        for y in points[i+1:]:
            v=sub(y,x)
            path=[x,y]+[tuple(a+j*b for a,b in zip(x,v)) for j in range(2,k)]
            if all(z in fibres for z in path[2:]):yield [fibres[z] for z in path]

def closure(source, initial, k):
    require(k>=3 and bool(source),'invalid closure input')
    n=len(source[0]);require(all(len(s)==n for s in source),'dimension mismatch')
    W=independent(initial,n); initial_rank=len(W); record=[]
    while True:
        old=list(W); steps=[]
        for xs in projected_progressions(source,old,k):
            v=sub(xs[1],xs[0])
            if coefficients(W,v) is not None:continue
            defects=[tuple(xs[i][h]-2*xs[i+1][h]+xs[i+2][h] for h in range(n))
                     for i in range(k-2)]
            cs=[coefficients(old,z) for z in defects]
            require(all(c is not None for c in cs),'uncertified progression premise')
            steps.append({'points':xs,'step':v,'defects':defects,
                          'premise_coefficients':[[str(x) for x in c] for c in cs]})
            W.append(v)
        if not steps:break
        record.append({'original_basis':old,'steps':steps})
    require(len(record)<=n-initial_rank,'closure rank bound exceeded')
    require(next(projected_progressions(source,W,k),None) is None,'not a fixed point')
    return W,record

def positive_point(basis,n):
    """Find an exact rational point a>=1, Wa=0 by vertex enumeration."""
    d=n-len(independent(basis,n))
    for I in combinations(range(n),d):
        rows=[list(w)+[0] for w in basis]
        rows += [[int(i==j) for j in range(n)]+[1] for i in I]
        a,p=rref(rows,n)
        if len(p)!=n or any(not any(x[:n]) and x[n] for x in a):continue
        v=[F(0)]*n
        for row,j in zip(a,p):v[j]=row[n]
        if all(x>=1 for x in v):
            scale=lcm(*(x.denominator for x in v))
            return tuple(int(scale*x) for x in v)
    return None

def infeasibility_certificate(basis,n):
    for i in range(n):
        for j in range(i+1,n):
            v=tuple(int(h==i)-int(h==j) for h in range(n))
            c=coefficients(basis,v)
            if c is not None:
                return {'kind':'forced-equality','vector':v,'coefficients':list(map(str,c))}
    Q=annihilator(basis,n)
    equations=[list(q)+[0] for q in Q]+[[1]*n+[1]]
    _,p=rref(equations,n); dimension=n-len(p)
    for I in combinations(range(n),dimension):
        rows=equations+[[int(i==j) for j in range(n)]+[0] for i in I]
        a,p=rref(rows,n)
        if len(p)!=n or any(not any(x[:n]) and x[n] for x in a):continue
        v=[F(0)]*n
        for row,j in zip(a,p):v[j]=row[n]
        if all(x>=0 for x in v) and any(v):
            scale=lcm(*(x.denominator for x in v));v=tuple(int(scale*x) for x in v)
            c=coefficients(basis,v);require(c is not None,'cone alternative outside relation space')
            return {'kind':'positive-obstruction','vector':v,'coefficients':list(map(str,c))}
    raise AssertionError('no exact infeasibility alternative')

def scalar_realization(source,basis):
    """Positive integer observer retaining pair and second-difference equations.

Returns None exactly when positivity or distinct coordinate values is blocked.
The theorem in the note proves this completeness for a closed relation space.
"""
    n=len(source[0]); a0=positive_point(basis,n)
    if a0 is None:return None
    if any(coefficients(basis,tuple(int(h==i)-int(h==j) for h in range(n))) is not None
           for i in range(n) for j in range(i+1,n)):return None
    Q=annihilator(basis,n);d=len(Q)
    errors={sub(x,y) for x in source for y in source}
    errors|={tuple(x[i]-2*y[i]+z[i] for i in range(n)) for x in source for y in source for z in source}
    errors={w for w in errors if coefficients(basis,w) is None}
    T=max(1,d*len(errors)+1)
    C=1+sum(T**(j+1)*max(map(abs,v),default=0) for j,v in enumerate(Q))
    for t in range(1,T+1):
        a=tuple(C*a0[i]+sum(t**(j+1)*Q[j][i] for j in range(d)) for i in range(n))
        if all(dot(a,v)!=0 for v in errors):
            require(min(a)>0 and len(set(a))==n,'invalid positive/distinct realization')
            require(all(dot(a,w)==0 for w in basis),'realization left annihilator')
            return {'weights':a,'positive_anchor':a0,'annihilator_basis':Q,
                    'candidate_bound':T,'dominant_coefficient':C,'chosen_parameter':t,
                    'forbidden_forms':len(errors)}
    raise AssertionError('finite avoidance bound failed')

def integer_ap(values,k):
    s=sorted(set(values));P=set(s)
    for i,a in enumerate(s):
        for b in s[i+1:]:
            d=b-a
            if a+(k-1)*d>s[-1]:break
            if all(a+j*d in P for j in range(2,k)):return tuple(a+j*d for j in range(k))
    return None
