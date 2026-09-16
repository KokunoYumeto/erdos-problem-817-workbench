"""Exact finite arithmetic for retained higher-arity image and boundary maps.

Standard library only. No function treats representation multiplicity as image
cardinality. All scale factors, carry values, and terminal observations remain
explicit in the returned objects.
"""
from __future__ import annotations
from collections import Counter, deque
from fractions import Fraction
from itertools import product
from math import comb

A6 = (1,4,5,17,21,22)
A10 = (3,4,7,34,37,41,216,250,253,257)
A3 = (1,7,8)


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def digit_weights(A: tuple[int,...], q: int) -> dict[int,int]:
    require(q >= 2 and bool(A) and tuple(sorted(set(A))) == A and A[0]>0,
            "invalid literal generator input")
    c = Counter({0:1})
    for a in A:
        out = Counter()
        for x,n in c.items():
            for j in range(q):
                out[x+j*a] += n
        c = out
    return dict(sorted(c.items()))


def runs(D) -> list[tuple[int,int]]:
    out = []
    for x in sorted(D):
        if out and x == out[-1][1]+1:
            out[-1] = (out[-1][0],x)
        else:
            out.append((x,x))
    return out


def carry_machine(D, b: int) -> dict:
    D = tuple(sorted(D))
    require(b>=2 and D and D[0]==0 and len(set(D))==len(D),"invalid digit set")
    W=max(D); C=W//(b-1)
    residues = [[] for _ in range(b)]
    for d in D:
        residues[d % b].append(d)
    states=[1]; index={1:0}; transitions=[]
    for R in states:
        row=[]
        for z in range(b):
            S=0
            for c in range(C+1):
                if (R>>c)&1:
                    for d in residues[(z-c)%b]:
                        u=(d+c-z)//b
                        require(d+c == z+b*u and 0<=u<=C,"carry box failed")
                        S |= 1<<u
            if S not in index:
                index[S]=len(states); states.append(S)
            row.append(index[S])
        transitions.append(row)
    matrix=[[row.count(j) for j in range(len(states))] for row in transitions]
    return {"base":b,"maximum_digit":W,"carry_bound":C,"states":states,
            "transitions":transitions,"matrix":matrix,
            "terminal":[R.bit_count() for R in states]}


def matvec(M, v):
    return [sum(a*b for a,b in zip(row,v)) for row in M]


def moments(machine: dict, last: int, degree: int=2) -> list[list[int]]:
    b=machine['base']; C=machine['carry_bound']; states=machine['states']
    f=[[sum(c**p for c in range(C+1) if (R>>c)&1) for R in states]
       for p in range(degree+1)]
    out=[[f[p][0] for p in range(degree+1)]]
    groups=[]
    for row in machine['transitions']:
        g={}
        for z,target in enumerate(row):
            if target not in g:g[target]=[0]*(degree+1)
            for p in range(degree+1):g[target][p]+=z**p
        groups.append(g)
    for _ in range(last):
        f=[[sum(comb(p,j)*b**j*zs[p-j]*f[j][target]
                for target,zs in g.items() for j in range(p+1))
            for g in groups] for p in range(degree+1)]
        out.append([f[p][0] for p in range(degree+1)])
    return out


def moment_matrix(machine: dict, degree: int=2):
    b=machine['base']; C=machine['carry_bound']; states=machine['states']; n=len(states)
    M=[[0]*((degree+1)*n) for _ in range((degree+1)*n)]
    for p in range(degree+1):
        for s,row in enumerate(machine['transitions']):
            for z,target in enumerate(row):
                for j in range(p+1):
                    M[p*n+s][j*n+target] += comb(p,j)*b**j*z**(p-j)
    f=[sum(c**p for c in range(C+1) if (R>>c)&1)
       for p in range(degree+1) for R in states]
    return M,f,degree*n


def poly_from_roots(roots):
    p=[1]
    for x in roots:
        q=[0]*(len(p)+1)
        for i,a in enumerate(p): q[i]-=x*a; q[i+1]+=a
        p=q
    return p


def check_observed_recurrence(M, f, out_index: int, polynomial, shift: int=0):
    for _ in range(shift):f=matvec(M,f)
    residual=[0]*len(f); v=f[:]
    for a in polynomial:
        residual=[x+a*y for x,y in zip(residual,v)]
        v=matvec(M,v)
    observations=[]
    for _ in range(len(M)):
        observations.append(residual[out_index]);residual=matvec(M,residual)
    require(not any(observations),"claimed all-length recurrence fails")
    return observations


def solve_square(A,b):
    n=len(A);R=[[Fraction(x)for x in row]+[Fraction(bi)]for row,bi in zip(A,b)]
    for j in range(n):
        k=next((i for i in range(j,n)if R[i][j]),None)
        require(k is not None,"singular interpolation system")
        R[j],R[k]=R[k],R[j];p=R[j][j];R[j]=[x/p for x in R[j]]
        for i in range(n):
            if i!=j and R[i][j]:
                c=R[i][j];R[i]=[x-c*y for x,y in zip(R[i],R[j])]
    return [row[-1]for row in R]


def rational_rank(A):
    if not A:return 0
    R=[[Fraction(x)for x in row]for row in A];i=0
    for j in range(len(R[0])):
        k=next((h for h in range(i,len(R))if R[h][j]),None)
        if k is None:continue
        R[i],R[k]=R[k],R[i];a=R[i][j];R[i]=[x/a for x in R[i]]
        for h in range(i+1,len(R)):
            if R[h][j]:
                a=R[h][j];R[h]=[x-a*y for x,y in zip(R[h],R[i])]
        i+=1
        if i==len(R):break
    return i


def hole_certificate(D, b):
    D=set(D);w=max(D)
    require(b<w<=2*b-2,"run theorem width condition failed")
    require(D=={w-d for d in D},"reflection failed")
    H=sorted(set(range(w//2+1))-D)
    require(H and max(H)<=w-b and not (set(H)&{w-b-h for h in H}),
            "boundary hole compatibility failed")
    require(D==set(range(w+1))-set(H)-{w-h for h in H},"hidden holes")
    expected=set(range(w+b+1))-set(H)-{w+b-h for h in H}
    require(D|{b+d for d in D}==expected,"two-translate certificate failed")
    return {"width":w,"size":len(D),"holes":H,"runs":runs(D),"kappa":len(runs(D))}


def count_run_formula(t,b,k,m):
    if b==k:return b**m+(t-b)*m*b**max(m-1,0)
    return Fraction(t-k,b-k)*b**m-Fraction(t-b,b-k)*k**m


def endpoint_moments(hole: dict,b: int,last: int):
    rs=hole['runs'];a=max(hole['holes'])
    middle=next(i for i,(l,u)in enumerate(rs)if l<=a+1<=u)
    L=[1,0,0,0];U=L[:];out=[]
    for _ in range(last+1):
        M=U[1]-L[1]+L[0]
        F1=(U[2]+U[1]-L[2]+L[1])//2
        F2=(2*(U[3]-L[3])+3*(U[2]+L[2])+U[1]-L[1])//6
        out.append([M,F1,F2])
        oldL,oldU=L,U;L=[];U=[]
        for p in range(4):
            L.append(sum(sum(comb(p,j)*b**j*l**(p-j)*(oldL if i<=middle else oldU)[j]
                             for j in range(p+1))for i,(l,u)in enumerate(rs)))
            U.append(sum(sum(comb(p,j)*b**j*u**(p-j)*(oldL if i<middle else oldU)[j]
                             for j in range(p+1))for i,(l,u)in enumerate(rs)))
    return out


def weighted_certificate(weights: dict[int,int],b: int):
    w=max(weights);require(w<=2*b-2,"two-carry weight bound failed")
    residues=[0]*b
    for d,n in weights.items():residues[d%b]+=n
    peak=max(weights.values());require(max(residues)==peak,"cyclic mass exceeds proposed bound")
    center=next(d for d in sorted(weights)if weights[d]==peak and d<b)
    D=set(weights)
    witness=next(r for r in range(1,b)if {r-1,r,b+r-1,b+r}<=D)
    return {"residue_masses":residues,"maximum_original_multiplicity":peak,
            "constant_output_digit":center,"all_ones_output_digit":witness}


def exact_coefficient(weights,b,m,x):
    C=max(weights)//(b-1);v=[1]+[0]*C
    for _ in range(m):
        z=x%b;x//=b
        v=[sum(v[c]*weights.get(z+b*t-c,0)for c in range(C+1))for t in range(C+1)]
    return v[x] if 0<=x<=C else 0


def delta(d):return tuple(d[i]-2*d[i+1]+d[i+2]for i in range(len(d)-2))


def real_machine(D,b,k):
    D=tuple(sorted(D));present=set(D)
    require(0 in present and max(D)<=b-2 and k>=3,"real-source hypotheses failed")
    C=2*max(D)//(b-1)
    initial=((0,)*(k-2),False);states=[initial];idx={initial:0};rows=[];parents=[None]
    for c,f in states:
        row={}
        for a in D:
            for second in D:
                def extend(ds,cs):
                    i=len(cs)
                    if i==k-2:
                        target=(tuple(cs),f or a!=second)
                        if target not in row:row[target]=tuple(ds)
                        return
                    for v in range(-C,C+1):
                        z=2*ds[-1]-ds[-2]-b*c[i]+v
                        if z in present:extend(ds+[z],cs+[v])
                extend([a,second],[])
        stored=[]
        for target,d in sorted(row.items()):
            if target not in idx:
                idx[target]=len(states);states.append(target);parents.append((len(rows),d))
            stored.append([idx[target],list(d)])
        rows.append(stored)
    # Repeated removal of vertices with no successor gives the exact infinite-path kernel.
    live=set(range(len(states)))
    while True:
        new={i for i in live if any(j in live for j,_ in rows[i])}
        if new==live:break
        live=new
    witness_start=next((i for i in sorted(live)if states[i][1]),None)
    witness=None
    if witness_start is not None:
        prefix=[];cur=witness_start
        while parents[cur]is not None:
            old,d=parents[cur];prefix.append(list(d));cur=old
        prefix.reverse();extra=[];seen={};cur=witness_start
        while cur not in seen:
            seen[cur]=len(extra)
            nxt,d=next((j,d)for j,d in rows[cur]if j in live)
            extra.append(d);cur=nxt
        t=seen[cur]
        witness={"prefix":prefix+extra[:t],"period":extra[t:]}
    return {"base":b,"k":k,"carry_bound":C,
            "states":[[list(c),f]for c,f in states],"edges":rows,
            "infinite_path_states":sorted(live),"witness":witness}


def evaluate_real(prefix,period,b):
    require(bool(period),"empty real period")
    k=len(period[0]);h=len(prefix);t=len(period)
    values=[sum(Fraction(d[i],b**(j+1))for j,d in enumerate(prefix))+
            sum(Fraction(d[i]*b**(t-j-1),b**h*(b**t-1))for j,d in enumerate(period))
            for i in range(k)]
    require(not any(delta(values)) and values[1]!=values[0],"invalid real AP")
    return values
