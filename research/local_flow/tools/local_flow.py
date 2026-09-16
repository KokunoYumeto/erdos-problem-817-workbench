#!/usr/bin/env python3
"""Literal finite-set observations, graph substitutions, and integral flow cones.

Standard-library only. All matrices count original finite labels. No spectral
floating-point calculation or enumeration over an unspecified infinite domain.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from math import gcd
from functools import reduce
from typing import Iterable

SHAPES=((0,),(0,1),(0,2),(0,1,2),(0,3),(0,1,3),(0,1,2,3))
ORBITS=(1,2,3,5,6,7,9,11,15)  # ordinary 4-bit integers; reversing preserves the orbit
# z=A*f: counts of each displayed word, not combined counts of a reversal pair.
A=[
 [0,0,0,-1,0,0,1],
 [0,0,0,0,0,-1,1],
 [0,-1,0,1,0,1,-1],
 [0,0,-1,1,0,1,-1],
 [0,0,0,0,-1,2,-1],
 [-1,1,1,-1,1,-2,1],
 [0,-1,0,2,0,0,-1],
 [-1,2,1,-2,0,-1,1],
 [4,-3,-2,2,-1,2,-1],
]
B=[
 [1,0,1,1,0,1,1,2,1],
 [1,1,1,2,1,2,1,2,1],
 [1,1,2,1,1,2,1,2,1],
 [1,2,2,2,1,2,1,2,1],
 [2,0,2,2,0,2,1,2,1],
 [2,1,2,2,1,2,1,2,1],
 [2,2,2,2,1,2,1,2,1],
]
CONSERVATION=[
 [1,-1,-1,0,0,0,1,0,0],
 [0,0,1,0,-1,-1,0,1,0],
]
RAY_SUPPORTS=((3,),(8,),(0,1),(6,1),(4,7),(5,7),
              (0,2,4),(0,2,5),(6,2,4),(6,2,5))
PERIODS=('10','1','1000','001','011','1011','11000','111000','1001','11001')


def require(ok: bool, msg: str) -> None:
    if not ok: raise AssertionError(msg)


def reverse_bits(x: int, width: int) -> int:
    y=0
    for j in range(width): y|=((x>>j)&1)<<(width-1-j)
    return y


def image(weights: Iterable[int], q: int) -> tuple[int,...]:
    require(q>=2,'arity at least two')
    vals={0}
    for a in weights: vals={x+c*a for x in vals for c in range(q)}
    return tuple(sorted(vals))


def bit_image(weights: Iterable[int], q: int) -> int:
    bits=1
    for a in weights:
        require(a>0,'positive generators')
        out=0
        for c in range(q): out |= bits << (a*c)
        bits=out
    return bits


def observations(Y: Iterable[int]) -> list[int]:
    Y=set(Y)
    require(bool(Y),'nonempty numerical source')
    return [len({y+r for y in Y for r in R}) for R in SHAPES]


def window_counts(Y: Iterable[int], q: int=5) -> list[int]:
    Y=set(Y);require(bool(Y) and q>=2,'invalid window source')
    width=q-1
    counts=[0]*(1<<width)
    for t in range(min(Y),max(Y)+width):
        word=sum(int(t-r in Y)<<r for r in range(width))
        counts[word]+=1
    return counts


def symmetric(Y: Iterable[int]) -> bool:
    Y=set(Y)
    return bool(Y) and {min(Y)+max(Y)-y for y in Y}==Y


def mv(M, v): return [sum(a*b for a,b in zip(row,v)) for row in M]
def mm(M,N): return [[sum(a*b for a,b in zip(row,col)) for col in zip(*N)] for row in M]
def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def transpose(M): return [list(x) for x in zip(*M)]
def add(M,N): return [[x+y for x,y in zip(a,b)] for a,b in zip(M,N)]
def scale(c,M): return [[c*x for x in row] for row in M]


def power(M,n):
    require(n>=0,'negative exponent');out=eye(len(M))
    while n:
        if n&1:out=mm(out,M)
        n//=2
        if n:M=mm(M,M)
    return out


def rref(M):
    out=[[Fraction(x) for x in row] for row in M]
    if not out:return out,[]
    i=0;piv=[]
    for j in range(len(out[0])):
        k=next((k for k in range(i,len(out)) if out[k][j]),None)
        if k is None:continue
        out[i],out[k]=out[k],out[i]
        v=out[i][j];out[i]=[x/v for x in out[i]]
        for k in range(len(out)):
            if k!=i and out[k][j]:
                v=out[k][j];out[k]=[x-v*y for x,y in zip(out[k],out[i])]
        piv.append(j);i+=1
        if i==len(out):break
    return out,piv


def rank(M):return len(rref(M)[1])

def nullspace(M):
    R,p=rref(M);n=len(M[0]);out=[]
    for j in range(n):
        if j in p:continue
        v=[Fraction(0)]*n;v[j]=1
        for i,k in enumerate(p):v[k]=-R[i][j]
        out.append(v)
    return out


def primitive(v):
    den=1
    for x in v:
        den=den*x.denominator//gcd(den,x.denominator)
    v=[int(x*den) for x in v];g=reduce(gcd,v)
    return [x//abs(g) for x in v]


def charpoly(M):
    """Integral Faddeev--LeVerrier coefficients, highest degree first."""
    n=len(M);P=eye(n);coeff=[1]
    for k in range(1,n+1):
        P=mm(M,P);tr=sum(P[i][i] for i in range(n))
        require(tr%k==0,'characteristic divisibility')
        c=-tr//k;coeff.append(c)
        for i in range(n):P[i][i]+=c
    require(not any(x for row in P for x in row),'Cayley--Hamilton residual')
    return coeff


def poly_matrix(coeff,M):
    out=scale(0,M)
    for c in coeff:out=add(mm(out,M),scale(c,eye(len(M))))
    return out


def incidence(q: int):
    width=q-2;n=1<<width;E=2*n
    d=[[0]*E for _ in range(n)]
    for e in range(E):d[e&(n-1)][e]+=1;d[e>>1][e]-=1
    return d


def raw_shapes(q):
    return tuple(sorted(((0,)+tuple(j for j in range(1,q-1) if bits>>(j-1)&1)
                         for bits in range(1<<(q-2))),key=lambda R:(R[-1],len(R),R)))


def count_carrier(D,b):
    D=tuple(sorted(set(D)))
    require(D and D[0]==0 and D[-1]<=4*(b-1) and b>=2,'outside fifth-arity bound')
    require(symmetric(D),'reflection requires symmetric digit source')
    indices={R:i for i,R in enumerate(SHAPES)}
    M=[]
    for R in SHAPES:
        fibers=defaultdict(set)
        for e in {d+r for d in D for r in R}:fibers[e%b].add(e//b)
        row=[0]*7
        for fiber in fibers.values():
            h=min(fiber);F=tuple(sorted(x-h for x in fiber))
            rev=tuple(sorted(F[-1]-x for x in F));F=min(F,rev)
            row[indices[F]]+=1
        M.append(row)
    return M


def substitution(D,b,q=5):
    """Each actual input edge is sent to its full b-edge output path."""
    D=tuple(sorted(set(D)));width=q-2;size=1<<(width+1);nv=size//2
    require(D and D[0]==0 and b>=2 and D[-1]<=(q-1)*(b-1),'invalid digit range')
    masks=[[0]*(width+1) for _ in range(b)]
    for d in D:
        for r in range(width+1):
            h,z=divmod(d+r,b)
            require(0<=h<=width,'lost input coordinate')
            masks[z][r]|=1<<h
    vertex=[]
    for s in range(nv):
        v=0
        for r in range(width):
            for d in D:
                h,z=divmod(d+1+r,b)
                if z==0 and 1<=h<=width and (s>>(h-1)&1):v|=1<<r;break
        vertex.append(v)
    L=[[0]*size for _ in range(size)];paths=[]
    for e in range(size):
        path=[];previous=vertex[e>>1]
        for z in range(b):
            out=sum(int(bool(e&m))<<r for r,m in enumerate(masks[z]))
            require(out>>1==previous,'path source mismatch')
            previous=out&(nv-1);path.append(out);L[out][e]+=1
        require(previous==vertex[e&(nv-1)],'path target mismatch')
        paths.append(path)
    V=[[int(vertex[j]==i) for j in range(nv)] for i in range(nv)]
    require(mm(incidence(q),L)==mm(V,incidence(q)),'chain square failed')
    result={'edges':L,'vertices':V,'vertex_function':vertex,'paths':paths,
            'zero_padding':(q-1)*(b-1)-D[-1]}
    if q==5 and symmetric(D):
        emb=[[int(e!=0 and min(e,reverse_bits(e,4))==o) for o in ORBITS] for e in range(16)]
        K=mm([L[e] for e in ORBITS],emb)
        M=count_carrier(D,b)
        require(mm(K,A)==mm(A,M),'nine-pattern/seven-count square')
        require(mm(B,A)==eye(7) and not any(x for row in mm(CONSERVATION,A) for x in row),'coordinate identities')
        result.update({'patterns':K,'counts':M})
    return result


def cone_rays():
    """All positive circuits of a 2-row integer matrix: complete support <=3."""
    rays=[]
    for count in range(1,4):
        for supp in combinations(range(9),count):
            Q=[[row[j] for j in supp] for row in CONSERVATION]
            ns=nullspace(Q)
            if len(ns)!=1:continue
            v=ns[0]
            if all(x<0 for x in v):v=[-x for x in v]
            if not all(x>0 for x in v):continue
            p=primitive(v);z=[0]*9
            for j,x in zip(supp,p):z[j]=x
            rays.append(z)
    require(len(rays)==10,'unexpected positive-circuit list')
    return rays


def decompose(z):
    """Exact nonnegative integral/rational circuit decomposition, with no rescaling."""
    require(len(z)==9 and min(z)>=0 and mv(CONSERVATION,z)==[0,0],'outside circulation cone')
    x=list(z);coeff=[0]*10
    coeff[0]=x[3];coeff[1]=x[8];x[3]=x[8]=0
    source=[min(x[0],x[2]),0];source[1]=x[2]-source[0]
    target=[min(x[4],x[2]),0];target[1]=x[2]-target[0]
    for i in range(2):
        for j in range(2):
            c=min(source[i],target[j]);coeff[6+2*i+j]+=c
            source[i]-=c;target[j]-=c
    # subtract the four triple circuits literally
    for t in range(6,10):
        for j in RAY_SUPPORTS[t]:x[j]-=coeff[t]
    require(x[2]==0 and min(x)>=0,'transport decomposition failed')
    coeff[2]=x[0];coeff[3]=x[6];coeff[4]=x[4];coeff[5]=x[5]
    out=[sum(coeff[i]*int(j in RAY_SUPPORTS[i]) for i in range(10)) for j in range(9)]
    require(out==list(z),'circuit reconstruction failed')
    return coeff


def simple_cycles(q=5):
    nv=1<<(q-2);out=[]
    for start in range(nv):
        def visit(nodes,edges):
            v=nodes[-1]
            for digit in (0,1):
                e=(v<<1)|digit;w=e&(nv-1)
                if w==start:out.append((tuple(nodes),tuple(edges+[e])))
                elif w>start and w not in nodes:visit(nodes+[w],edges+[e])
        visit([start],[])
    return out


def symmetric_period(word: str,N: int):
    require(N>=1 and word and '1' in word,'invalid original period')
    p=len(word);Y={j*p+i for j in range(N) for i,d in enumerate(word) if d=='1'}
    center=2*N*p+4
    return tuple(sorted(Y|{center-y for y in Y}))


def modular_safe(A,b,k=5):
    D=image(A,2);require(D[-1]<b,'canonical input')
    present=set(D)
    return not any(all((a+i*d)%b in present for i in range(k))
                   for a in D for d in range(1,b))


def integer_ap(Y,k):
    Y=tuple(sorted(Y));present=set(Y)
    for i,x in enumerate(Y):
        for y in Y[i+1:]:
            d=y-x
            if x+(k-1)*d>Y[-1]:break
            if all(x+j*d in present for j in range(2,k)):return tuple(x+j*d for j in range(k))
    return None


def dual_certificate(w):
    """Exact certificate for a row on the entire closed observable cone.

The two potential values alter the coefficient row only by the two retained
conservation rows. A negative result includes an actual symmetric finite tail.
"""
    require(len(w)==7,'seven original observation coefficients required')
    rays=[[int(j in s) for j in range(9)] for s in RAY_SUPPORTS]
    values=[sum(a*b for a,b in zip(w,mv(B,z))) for z in rays]
    bad=next((i for i,v in enumerate(values) if v<0),None)
    if bad is not None:
        f=mv(B,rays[bad]);word=PERIODS[bad];h=word.count('1')
        required=Fraction(6*f[0]*sum(abs(x) for x in w),h*(-values[bad]))
        N=max(4,required.numerator//required.denominator+2)
        Y=symmetric_period(word,N);obs=observations(Y)
        require(sum(a*b for a,b in zip(w,obs))<0,'finite periodic violation failed')
        return {'nonnegative':False,'ray':bad,'period':word,'repetitions':N,
                'size':len(Y),'observations':obs}
    r=mv(transpose(B),w)
    potential=[min(r[0],r[6]),-min(r[4],r[5])]
    alpha=[r[j]-sum(potential[i]*CONSERVATION[i][j] for i in range(2)) for j in range(9)]
    require(min(alpha)>=0,'positive local remainder failed')
    require(mv(transpose(A),alpha)==list(w),'dual original-row reconstruction')
    return {'nonnegative':True,'potential':potential,'pattern_coefficients':alpha}
