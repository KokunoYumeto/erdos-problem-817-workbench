"""Literal finite image operations. No coordinate rescaling or external dependencies."""
from __future__ import annotations
from collections import Counter
from itertools import product
from math import isqrt

def require(test: bool, message: str) -> None:
    if not test:
        raise AssertionError(message)

def values(A: tuple[int, ...], q: int) -> set[int]:
    require(q >= 1, 'positive alphabet size required')
    out = {0}
    for a in A:
        out = {x + j*a for x in out for j in range(q)}
    return out

def masses(A: tuple[int, ...], q: int) -> Counter:
    out = Counter({0: 1})
    for a in A:
        nxt = Counter()
        for x, mass in out.items():
            for j in range(q):
                nxt[x+j*a] += mass
        out = nxt
    return out

def runs(D: set[int]) -> int:
    return sum(x-1 not in D for x in D)

def statistics(D: set[int], b: int) -> dict:
    require(b >= 2 and D and min(D) >= 0 and max(D) <= 2*b-2,
            'digit range must be contained in [0,2b-2]')
    U = {d % b for d in D}
    t, kap, v = len(D), runs(D), len(U)
    eta = len(U | {(u+1) % b for u in U})-v
    beta = t-v
    T = ((v, beta), (eta, kap-eta))
    require(all(x >= 0 for row in T for x in row), 'negative transfer entry')
    tr = v+kap-eta
    det = v*(kap-eta)-beta*eta
    return dict(digits=sorted(D), base=b, size=t, runs=kap, residues=v,
                cyclic_boundary=eta, overlap=beta, matrix=[list(row) for row in T],
                trace=tr, determinant=det,
                two_level_kernel=beta*(t-kap),
                no_cross_level_collisions=beta*(t-kap)==0,
                full_base_growth=(v == b or len(D | {d+1 for d in D}) == 2*b))

def matmul(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

def image_chain(levels):
    """Levels are least significant first; recursion retains literal radices."""
    Y = {0}
    for b,D in reversed(levels):
        Y = {d+b*y for d in D for y in Y}
    return Y

def count_chain(levels):
    M = [[1,0],[0,1]]
    for b,D in levels:
        M=matmul(M, statistics(D,b)['matrix'])
    return M[0][0]+M[0][1], M[1][0]+M[1][1]

def ap_witness(D: set[int], k: int):
    require(k >= 3, 'k >= 3 required')
    L = sorted(D)
    if not L: return None
    for i,x in enumerate(L):
        for y in L[i+1:]:
            d=y-x
            if x+(k-1)*d > L[-1]: break
            if all(x+j*d in D for j in range(2,k)):
                return [x+j*d for j in range(k)]
    return None

def modular_ap(D: set[int], p: int, k: int):
    U = {x%p for x in D}
    for x in sorted(U):
        for y in sorted(U):
            d=(y-x)%p
            if d and all((x+j*d)%p in U for j in range(2,k)):
                return [int((x+j*d)%p) for j in range(k)]
    return None

def is_prime(p: int) -> bool:
    return p >= 2 and all(p%d for d in range(2,isqrt(p)+1))

def good_prime(A: tuple[int,...], h: int = 2) -> dict:
    require(A and min(A)>0 and len(set(A))==len(A), 'positive distinct generators required')
    require(h >= 1, 'h >= 1 required')
    S=sum(A)
    signed={x-h*S for x in values(A,2*h+1)}
    positives=sorted(x for x in signed if x>0)
    bits=(h*S).bit_length() # strict upper bound on natural logarithm
    bound=256+4*len(positives)*bits
    excluded=[]
    for p in range(2,bound+1):
        if not is_prime(p): continue
        bad=next((x for x in positives if x%p==0),None)
        if bad is None:
            E=values(A,h+1)
            require(len({x%p for x in E})==len(E),'prime failed observation injection')
            return dict(weights=list(A),coefficient_radius=h,prime=p,
                        exact_positive_difference_count=len(positives),max_difference=h*S,
                        bit_budget=bits,bound=bound,excluded_primes=excluded,
                        observed_image_size=len(E),actual_generator_max=max(A),
                        binary_digit_max=S,noncanonical=(S>=p))
        excluded.append([p,bad])
    raise AssertionError('proved prime budget exhausted')

def amplify(A: tuple[int,...], r: int, h: int = 2):
    R=2*h*sum(A)+1
    B=tuple(R**j*a for j in range(r) for a in A)
    require(len(set(B))==r*len(A),'amplification generator collision')
    return R,B

def quotient_basis(D: set[int], Y: set[int], b: int):
    require(max(D)<=2*b-2 and min(D)>=0,'range required')
    return [((d+b,y),(d,y+1)) for d in sorted(D) if d+b in D
            for y in sorted(Y) if y+1 in Y]

def collision_path(A: tuple[int,...], b: int, q: int) -> dict:
    """A shortest collision of words of distinct local values, or full carry closure."""
    from collections import deque
    require(q >= 2 and A and min(A)>0 and sum(A)<b,'canonical generator block required')
    D=sorted(values(A,q))
    diffs={}
    for x in D:
        for y in D:diffs.setdefault(x-y,(x,y))
    queue=deque([0]);parents={0:None};terminal=None
    while queue and terminal is None:
        c=queue.popleft()
        for delta,(x,y) in sorted(diffs.items()):
            if (c+delta)%b:continue
            nxt=(c+delta)//b
            require(abs(nxt)<=q-2,'universal difference carry bound')
            if c==0 and nxt==0:continue
            if nxt==0:
                terminal=(c,delta,x,y);break
            if nxt not in parents:
                parents[nxt]=(c,delta,x,y);queue.append(nxt)
    result={'weights':list(A),'base':b,'arity':q,'independent':terminal is None,
            'reachable_nonzero_carries':sorted(c for c in parents if c)}
    if terminal:
        labels=[terminal[1:]];c=terminal[0]
        while c:
            prev,delta,x,y=parents[c];labels.append((delta,x,y));c=prev
        labels.reverse()
        xs=[x for delta,x,y in labels];ys=[y for delta,x,y in labels]
        vx=sum(x*b**j for j,x in enumerate(xs));vy=sum(y*b**j for j,y in enumerate(ys))
        require(vx==vy and xs!=ys,'collision reconstruction')
        require(len(labels)<=q-1,'absolute-carry witness bound')
        result['witness']={'left':xs,'right':ys,'value':vx,'levels':len(labels),
                           'differences':[delta for delta,x,y in labels]}
    return result
