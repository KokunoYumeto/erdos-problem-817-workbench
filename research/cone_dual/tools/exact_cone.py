#!/usr/bin/env python3
"""Exact source-to-cone arithmetic for the EP817 fifth-arity observation.

All matrices retain the ordered seven coordinates. Rational arithmetic and the
Python standard library suffice. Numerical discoveries are not proof inputs.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd, lcm
from functools import reduce, lru_cache

SHAPES=((0,),(0,1),(0,2),(0,1,2),(0,3),(0,1,3),(0,1,2,3))
V0=(1,2,2,3,2,3,4)
PERIODS=('1000','11000','111000','001','1001','11001','10','011','1011','1')
RAYS=((1,2,2,3,2,3,4),(2,3,4,4,4,5,5),(3,4,5,5,6,6,6),
      (1,2,2,3,1,2,3),(2,3,4,4,3,4,4),(3,4,5,5,5,5,5),
      (1,2,1,2,2,2,2),(2,3,3,3,2,3,3),(3,4,4,4,4,4,4),(1,1,1,1,1,1,1))


def require(ok:bool, message:str)->None:
    if not ok: raise AssertionError(message)


def dot(a,b): return sum(x*y for x,y in zip(a,b))
def mv(A,x): return [dot(row,x) for row in A]
def mm(A,B): return [[dot(row,col) for col in zip(*B)] for row in A]
def transpose(A): return list(map(list,zip(*A)))
def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]

def rref(A):
    a=[[F(x) for x in row] for row in A]
    if not a: return a,[]
    row=0;piv=[]
    for col in range(len(a[0])):
        p=next((i for i in range(row,len(a)) if a[i][col]),None)
        if p is None:continue
        a[row],a[p]=a[p],a[row];v=a[row][col];a[row]=[x/v for x in a[row]]
        for i in range(len(a)):
            if i!=row and a[i][col]:
                t=a[i][col];a[i]=[x-t*y for x,y in zip(a[i],a[row])]
        piv.append(col);row+=1
        if row==len(a):break
    return a,piv

def rank(A):return len(rref(A)[1])

def nullspace(A,n=None):
    if not A:return eye(n or 0)
    a,piv=rref(A);n=len(a[0]);out=[]
    for f in range(n):
        if f in piv:continue
        x=[F(0)]*n;x[f]=F(1)
        for i,p in enumerate(piv):x[p]=-a[i][f]
        out.append(x)
    return out

def solve_unique(A,b):
    if not A:return [] if not b else None
    n=len(A[0]);a,piv=rref([list(row)+[rhs] for row,rhs in zip(A,b)])
    if n in piv or len([p for p in piv if p<n])!=n:return None
    x=[F(0)]*n
    for i,p in enumerate(piv):
        if p<n:x[p]=a[i][-1]
    return x if mv(A,x)==list(b) else None

def inverse(A):
    n=len(A);cols=[solve_unique(A,[int(i==j) for i in range(n)]) for j in range(n)]
    require(all(x is not None for x in cols),'singular matrix')
    return transpose(cols)

def primitive(v):
    d=lcm(*[F(x).denominator for x in v]);a=[int(F(x)*d) for x in v]
    g=reduce(gcd,a);return tuple(x//abs(g) for x in a) if g else tuple(a)

def reverse(e):return int(f'{e:04b}'[::-1],2)
def shape(T):
    t=sorted(T);u=tuple(x-t[0] for x in t);return min(u,tuple(sorted(u[-1]-x for x in u)))

@lru_cache(maxsize=1)
def pattern_map():
    """Möbius derivation; row e gives the literal frequency of word e != 0000."""
    index={R:i for i,R in enumerate(SHAPES)};U=[]
    for R in SHAPES:
        row=[0]*7
        for k in range(1,len(R)+1):
            for T in combinations(R,k):row[index[shape(T)]]+=(-1)**(k+1)
        U.append(row)
    inv=inverse(U);rows=[[0]*7]
    for e in range(1,16):
        yes=[i for i in range(4) if e>>i&1];no=[i for i in range(4) if not(e>>i&1)]
        a=[0]*7
        for k in range(len(no)+1):
            for T in combinations(no,k):a[index[shape(yes+list(T))]]+=(-1)**k
        row=mm([a],inv)[0];require(all(x.denominator==1 for x in row),'nonintegral pattern section')
        rows.append([int(x) for x in row])
    return U,rows

@lru_cache(maxsize=1)
def observation_map():
    return [[int(any(e>>i&1 for i in R)) for e in range(16)] for R in SHAPES]

def incidence():
    B=[[0]*16 for _ in range(8)]
    for e in range(16):B[e>>1][e]-=1;B[e&7][e]+=1
    return B

def symmetric_equations():
    out=incidence()
    for e in range(16):
        if e<reverse(e):
            a=[0]*16;a[e]=1;a[reverse(e)]=-1;out.append(a)
    return out

@lru_cache(maxsize=1)
def facets():
    rows=pattern_map()[1]
    return [rows[e] for e in range(1,16) if e<=reverse(e)]

def observe(Y):
    Y=set(Y);return [len({y+r for y in Y for r in R}) for R in SHAPES]

def word_counts(Y,padding=0):
    """Finite admitted interval; zero-loop counts remain present."""
    Y=set(Y);require(padding>=0,'negative padding')
    lo,hi=(min(Y),max(Y)+3) if Y else (0,3)
    out=[0]*16
    for t in range(lo-padding,hi+padding+1):
        e=sum((1<<i) for i in range(4) if t-i in Y);out[e]+=1
    return out

def symmetric(Y):
    Y=set(Y);return not Y or {min(Y)+max(Y)-y for y in Y}==Y

def cycles():
    out=[]
    for root in range(8):
        def visit(v,vertices,edges):
            for bit in (0,1):
                e=2*v+bit;w=e&7
                if w==root:out.append(tuple(edges+[e]))
                elif w>root and w not in vertices:visit(w,vertices+[w],edges+[e])
        visit(root,[root],[])
    return out

def cycle_vector(c):
    z=[0]*16
    for e in c:z[e]+=1;z[reverse(e)]+=1
    return mv(observation_map(),z)

def periodic_vector(word):
    p=len(word);count=[0]*16
    for t in range(p):
        e=sum((int(word[(t-i)%p])<<i) for i in range(4));count[e]+=1
    return mv(observation_map(),count)

def conic_decomposition(v,rays=RAYS):
    for s in range(1,min(7,len(rays))+1):
        for inds in combinations(range(len(rays)),s):
            x=solve_unique(transpose([rays[i] for i in inds]),v)
            if x is not None and all(t>=0 for t in x):
                return [(i,t) for i,t in zip(inds,x) if t]
    raise AssertionError(f'no positive ray representation: {v}')

def section_vertices(extra=()):
    """Exact vertices of {x0=1, facets*x>=0, extra*x>=0}."""
    fs=facets()+list(extra);vertices=set()
    for inds in combinations(range(len(fs)),6):
        x=solve_unique([[1,0,0,0,0,0,0]]+[fs[i] for i in inds],[1]+[0]*6)
        if x is not None and all(dot(row,x)>=0 for row in fs):vertices.add(tuple(x))
    return sorted(vertices)

def image(A,q=5):
    v={0}
    for a in A:v={x+c*a for x in v for c in range(q)}
    return tuple(sorted(v))

def masses(A,q=5):
    v={0:1}
    for a in A:
        nxt={}
        for x,w in v.items():
            for c in range(q):nxt[x+c*a]=nxt.get(x+c*a,0)+w
        v=nxt
    return v

def matrix(D,b):
    D=set(D);require(D and min(D)>=0 and max(D)<=4*(b-1),'invalid fifth-arity digits')
    require(symmetric(D),'reflection requires the actual symmetric digit set')
    index={R:i for i,R in enumerate(SHAPES)};M=[];labels=[]
    for R in SHAPES:
        fibers={}
        for e in {d+r for d in D for r in R}:fibers.setdefault(e%b,set()).add(e//b)
        row=[0]*7;labs=[]
        for z,Q in sorted(fibers.items()):
            h=min(Q);T=tuple(sorted(t-h for t in Q));S=shape(T);row[index[S]]+=1
            labs.append(dict(residue=z,quotients=sorted(Q),offset=z+b*h,shape=list(S)))
        M.append(row);labels.append(labs)
    return M,labels

def modular_witness(D,b,k):
    D={x%b for x in D}
    for a in sorted(D):
        for step in range(1,b):
            vals=[(a+i*step)%b for i in range(k)]
            if all(t in D for t in vals):return vals
    return None

def ap_witness(D,k=5):
    D=sorted(set(D));s=set(D)
    if not D:return None
    for a in D:
        for d in range(1,(D[-1]-a)//(k-1)+1):
            vals=[a+i*d for i in range(k)]
            if all(t in s for t in vals):return vals
    return None

def facet_cells(rows):
    return [section_vertices([[b-a for a,b in zip(row,other)] for other in rows if other!=row]) for row in rows]

def certify_min_expansion(rows,M,threshold):
    cells=facet_cells(rows);worst=None;tests=0
    for i,vs in enumerate(cells):
        for x in vs:
            gx=dot(rows[i],x)
            require(gx>0,'potential must be positive off the origin')
            for a in rows:
                r=dot(a,mv(M,x))-threshold*gx
                require(r>=0,'polyhedral expansion failed')
                tests+=1;worst=r if worst is None else min(worst,r)
    return dict(cells=[len(x) for x in cells],inequalities=tests,minimum_slack=str(worst))

KERNEL=[[-1,-1,0],[1,0,0],[0,1,0],[1,1,0],[-1,0,-1],[0,-1,1],[0,0,0],[0,0,1],[0,0,-1],[0,0,0]]

def greedy_coordinates(x):
    """Integral positive section through the two exact flow-balance equations."""
    rows=pattern_map()[1];u,v,w,d,e,f,g,h,i=[dot(rows[j],x) for j in (1,2,3,5,6,7,9,11,15)]
    require(min(u,v,w,d,e,f,g,h,i)>=0,'input is outside the actual observation cone')
    require(u+g==v+w and w+h==e+f,'source flow balance failed')
    uv=min(u,v);gv=v-uv;up=u-uv;gp=g-gv
    he=min(h,e);hf=h-he;ep=e-he;fp=f-hf
    ue=min(up,ep);uf=up-ue;ge=ep-ue;gf=gp-ge
    out=[uv,ue,uf,gv,ge,gf,d,he,hf,i]
    require(min(out)>=0 and mv(transpose(RAYS),out)==list(x),'positive section inverse failed')
    return out

def positive_lift(M):return transpose([greedy_coordinates(mv(M,r)) for r in RAYS])

def kernel_primitive(v):
    out=[v[1],v[2],v[7]]
    require(mv(KERNEL,out)==list(v),'not an original relation of the ray presentation')
    return out

def kernel_action(Mhat):return transpose([kernel_primitive(v) for v in transpose(mm(Mhat,KERNEL))])

def subtract(A,B):return [[x-y for x,y in zip(a,b)] for a,b in zip(A,B)]

def defect(M,N):
    hM=positive_lift(M);hN=positive_lift(N);hMN=positive_lift(mm(M,N))
    E=subtract(mm(hM,hN),hMN)
    return transpose([kernel_primitive(v) for v in transpose(E)])
