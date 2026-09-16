#!/usr/bin/env python3
"""Literal score sources, integral orientation allocation, and exact closures.

Every reported source point retains an original edge-head mask. Rational
elimination is used only to express relations in a displayed basis.
Standard-library only; checks remain enabled under Python -O.
"""
from __future__ import annotations
from collections import deque
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import lcm

def require(ok, message):
    if not ok: raise AssertionError(message)

def add(x,y): return tuple(a+b for a,b in zip(x,y))
def sub(x,y): return tuple(a-b for a,b in zip(x,y))
def dot(x,y): return sum(a*b for a,b in zip(x,y))

def score(mask, n, edges):
    s=[0]*n
    for j,(a,b) in enumerate(edges): s[b if (mask>>j)&1 else a]+=1
    return tuple(s)

def score_source(n,edges):
    S={}
    for mask in range(1<<len(edges)):
        S.setdefault(score(mask,n,edges),[]).append(mask)
    return S

def graph_aut(n,edges):
    E={tuple(sorted(e)) for e in edges}
    return [p for p in permutations(range(n))
            if {tuple(sorted((p[a],p[b]))) for a,b in E}==E]

def orbits(S,n,edges):
    D={sub(a,b) for a in S for b in S};D.discard((0,)*n)
    ps=graph_aut(n,edges);remaining=set(D);out=[]
    while remaining:
        r=min(remaining)
        orb={tuple(t*r[p[i]] for i in range(n)) for p in ps for t in(-1,1)}
        require(orb<=D,'automorphism escaped original differences')
        remaining-=orb;out.append((r,len(orb)))
    return D,ps,out

def rref(rows,columns):
    a=[list(map(F,r)) for r in rows];p=[];j=0
    for c in range(columns):
        v=next((i for i in range(j,len(a)) if a[i][c]),None)
        if v is None:continue
        a[j],a[v]=a[v],a[j];scale=a[j][c];a[j]=[x/scale for x in a[j]]
        for i in range(len(a)):
            if i!=j and a[i][c]:
                t=a[i][c];a[i]=[x-t*y for x,y in zip(a[i],a[j])]
        p.append(c);j+=1
        if j==len(a):break
    return a,p

def coeff(basis,v):
    if not basis:return [] if not any(v) else None
    d=len(basis);rows,p=rref([[b[i] for b in basis]+[v[i]] for i in range(len(v))],d)
    if any(not any(r[:d]) and r[d] for r in rows):return None
    ans=[F(0)]*d
    for row,i in zip(rows,p):ans[i]=row[d]
    require(all(sum(c*b[i] for c,b in zip(ans,basis))==v[i] for i in range(len(v))), 'coefficient replay failed')
    return ans

def annihilator(basis,n):
    rows,p=rref(basis,n);out=[]
    for j in range(n):
        if j in p:continue
        v=[F(0)]*n;v[j]=1
        for row,i in zip(rows,p):v[i]=-row[j]
        den=lcm(*(x.denominator for x in v));out.append(tuple(int(den*x) for x in v))
    return out

def independent(rows):
    B=[]
    for r in rows:
        if coeff(B,r) is None:B.append(tuple(r))
    return B

def union_closure(S,r,k):
    """Progression closure in the SAME S union (S+r); retain every source lift."""
    U=set(S)|{add(s,r) for s in S};n=len(r);W=[];rounds=[]
    while True:
        old=list(W);Q=annihilator(old,n);fib={}
        for x in sorted(U):fib.setdefault(tuple(dot(q,x) for q in Q),x)
        pts=sorted(fib);steps=[]
        for aindex,a in enumerate(pts):
            for b in pts[aindex+1:]:
                v=sub(b,a);path=[tuple(x+i*y for x,y in zip(a,v)) for i in range(k)]
                if not all(x in fib for x in path):continue
                xs=[fib[x] for x in path];w=sub(xs[1],xs[0])
                if coeff(W,w) is not None:continue
                defects=[tuple(xs[i][h]-2*xs[i+1][h]+xs[i+2][h] for h in range(n)) for i in range(k-2)]
                cs=[coeff(old,d) for d in defects]
                require(all(c is not None for c in cs),'missing old-boundary primitive')
                reps=[]
                for x in xs:
                    shift=0 if x in S else 1;s=x if not shift else sub(x,r)
                    require(s in S,'source union lift missing')
                    reps.append({'mask':S[s][0], 'shift':shift})
                steps.append({'representatives':reps,'step':w,'defects':defects,
                              'coefficients':[[str(c) for c in row] for row in cs]})
                W.append(w)
        if not steps:break
        rounds.append({'old_basis':old,'steps':steps})
    return W,rounds

def collision_closure(S,r,k):
    """Original-source closure under a specified scalar collision r."""
    n=len(r);W=[tuple(r)];rounds=[]
    while True:
        old=list(W);Q=annihilator(old,n);fib={}
        for x in sorted(S):fib.setdefault(tuple(dot(q,x) for q in Q),x)
        points=sorted(fib);steps=[]
        for aindex,a in enumerate(points):
            for b in points[aindex+1:]:
                v=sub(b,a);path=[tuple(x+i*y for x,y in zip(a,v)) for i in range(k)]
                if not all(x in fib for x in path):continue
                xs=[fib[x] for x in path];w=sub(xs[1],xs[0])
                if coeff(W,w) is not None:continue
                defects=[tuple(xs[i][h]-2*xs[i+1][h]+xs[i+2][h] for h in range(n)) for i in range(k-2)]
                cs=[coeff(old,d) for d in defects]
                require(all(c is not None for c in cs),'original-source closure lost a primitive')
                steps.append({'representatives':[{'mask':S[x][0],'shift':0} for x in xs],
                              'step':w,'defects':defects,'coefficients':[[str(x) for x in row] for row in cs]})
                W.append(w)
        if steps:rounds.append({'old_basis':old,'steps':steps})
        for i,j in combinations(range(n),2):
            root=tuple(int(h==j)-int(h==i) for h in range(n));c=coeff(W,root)
            if c is not None:
                return {'initial_basis':[r],'rounds':rounds,'final_basis':W,'root':root,'coefficients':list(map(str,c))}
        require(bool(steps),'local collision has no root consequence')

def packet(S,r,a,v,sigma):
    rows=[tuple(a[h]+i*v[h]+sigma[i]*r[h] for h in range(len(r))) for i in range(len(sigma))]
    require(all(row in S for row in rows),'packet left original score source')
    return {'anchor':a,'step':v,'switch':sigma,'masks':[S[s][0] for s in rows]}

def packets_cubic(S,r):
    """All possible nonzero first-round directions for a degree-three source.

At endpoints in opposite translated copies, each coordinate of v is 0 or
-opposite_sign(r). Every possible v is tested; actual intermediate masks stay.
"""
    n=len(r);out={}
    options=[(0,-1 if x>0 else 1) if x else (0,) for x in r]
    for v in product(*options):
        if not any(v) or sum(v):continue
        tail=tuple(4*x+y for x,y in zip(v,r))
        if any(abs(x)>3 for x in tail):continue
        for a in sorted(S):
            if add(a,tail) not in S:continue
            sigma=[0]
            for j in (1,2,3):
                row=tuple(x+j*y for x,y in zip(a,v))
                if row in S:sigma.append(0)
                elif add(row,r) in S:sigma.append(1)
                else:break
            else:
                out[v]=packet(S,r,a,v,sigma+[1]);break
    return out

def cone_packets(S,r,ps):
    vectors=list(ps);target=tuple(abs(x) for x in r);z=(0,)*len(r)
    queue=deque([z]);parent={z:None}
    while queue and target not in parent:
        x=queue.popleft()
        for i,v in enumerate(vectors):
            y=tuple(a+abs(b) for a,b in zip(x,v))
            if all(a<=b for a,b in zip(y,target)) and y not in parent:
                parent[y]=(x,i);queue.append(y)
    if target not in parent:return None
    seq=[];cur=target
    while parent[cur] is not None:
        cur,i=parent[cur];seq.append(ps[vectors[i]])
    require(all(r[j]+sum(p['step'][j] for p in seq)==0 for j in range(len(r))), 'conformal identity failed')
    return seq

class IntegralFlow:
    def __init__(self,n):self.adj=[[] for _ in range(n)]
    def edge(self,u,v,c):
        i=len(self.adj[u]);j=len(self.adj[v]);self.adj[u].append([v,j,c,c]);self.adj[v].append([u,i,0,0]);return (u,i)
    def flow(self,s,t):
        total=0
        while True:
            p=[None]*len(self.adj);p[s]=(-1,-1);q=deque([s])
            while q and p[t] is None:
                u=q.popleft()
                for j,(v,rev,c,orig) in enumerate(self.adj[u]):
                    if c and p[v] is None:p[v]=(u,j);q.append(v)
            if p[t] is None:return total
            amount=10**20;v=t
            while v!=s:u,j=p[v];amount=min(amount,self.adj[u][j][2]);v=u
            v=t
            while v!=s:
                u,j=p[v];e=self.adj[u][j];e[2]-=amount;self.adj[v][e[1]][2]+=amount;v=u
            total+=amount

def orient(n,edges,target):
    require(len(target)==n and min(target)>=0 and sum(target)==len(edges),'invalid degree request')
    m=len(edges);source=m+n;sink=source+1;net=IntegralFlow(sink+1);choices=[]
    for i,(a,b) in enumerate(edges):
        net.edge(source,i,1);left=net.edge(i,m+a,1);right=net.edge(i,m+b,1);choices.append((left,right))
    for v in range(n):net.edge(m+v,sink,target[v])
    require(net.flow(source,sink)==m,'orientation cut condition failed')
    mask=0
    for i,(_,right) in enumerate(choices):
        u,j=right
        if net.adj[u][j][2]==0:mask|=1<<i
    require(score(mask,n,edges)==tuple(target),'orientation output mismatch')
    return mask

def clique_tail(m,r):
    E=list(combinations(range(m),2));i=max(range(m),key=lambda h:r[h]);j=min(range(m),key=lambda h:r[h])
    require(r[i]>0 and r[j]<0,'not a nonzero zero-sum difference')
    alpha=tuple(int(h==j)-int(h==i) for h in range(m));I=[h for h in range(m) if h not in(i,j)];extra=list(combinations(I,2))
    b=tuple(0 if h==i else m-1 if h==j else m-2 for h in range(m))
    mask=orient(m,E+extra,tuple(r[h]+alpha[h]+b[h] for h in range(m)))
    tmask=mask&((1<<len(E))-1);sheads={}
    for eindex,(u,v) in enumerate(extra):
        head=v if (mask>>(len(E)+eindex))&1 else u;sheads[(u,v)]=u if head==v else v
    for u,v in E:
        if j in(u,v):sheads[(u,v)]=j
        elif i in(u,v):sheads[(u,v)]=v if u==i else u
    smask=sum((1<<h) for h,(u,v) in enumerate(E) if sheads[(u,v)]==v)
    index={e:h for h,e in enumerate(E)};flips=[1<<index[tuple(sorted((i,j)))]]
    flips += [(1<<index[tuple(sorted((i,h)))])|(1<<index[tuple(sorted((j,h)))]) for h in I]
    current=smask
    for f in flips:current^=f
    rows=[current]
    for f in flips:current^=f;rows.append(current)
    require(current==smask and len(rows)==m,'root string reconstruction failed')
    rows.append(tmask);xs=[score(x,m,E) for x in rows]
    require(sub(xs[1],xs[0])==alpha,'root step lost')
    require(all(tuple(xs[h][a]-2*xs[h+1][a]+xs[h+2][a] for a in range(m))==((0,)*m if h<m-2 else tuple(r)) for h in range(m-1)), 'clique tail defect failed')
    return {'i':i,'j':j,'alpha':alpha,'masks':rows}

def clique_derivation(m,r):
    initial=tuple(r);current=initial;stages=[]
    while any(current):
        p=clique_tail(m,current);p['current']=current;stages.append(p);next_r=add(current,p['alpha'])
        require(sum(max(0,x) for x in next_r)==sum(max(0,x) for x in current)-1,'integral budget failed')
        current=next_r
    require(len(stages)<=m*m//4,'clique implication bound failed')
    return {'difference':initial,'stages':stages}

def digit_image(A,q=2):
    vals={0}
    for a in A:vals={x+j*a for x in vals for j in range(q)}
    return vals

def ap_witness(values,k):
    s=sorted(values);P=set(s)
    for i,a in enumerate(s):
        for b in s[i+1:]:
            if a+(k-1)*(b-a)>s[-1]:break
            xs=tuple(a+j*(b-a) for j in range(k))
            if all(x in P for x in xs):return xs
    return None

def primitive_components(A,q=2):
    n=len(A);rows=[r for r in product(range(1-q,q),repeat=n) if any(r) and dot(r,A)==0]
    rows.sort(key=lambda r:(sum(map(abs,r)),r));primitives=[]
    for r in rows:
        if any(all(p[i]*r[i]>=0 and abs(p[i])<=abs(r[i]) for i in range(n)) for p in primitives):continue
        primitives.append(r)
    parent=list(range(n))
    def find(i):
        while i!=parent[i]:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for r in primitives:
        support=[i for i,x in enumerate(r) if x]
        for i in support[1:]:parent[find(i)]=find(support[0])
    classes={}
    for i in range(n):classes.setdefault(find(i),[]).append(i)
    partition=sorted(classes.values())
    require(__import__('math').prod(len(digit_image([A[i] for i in C],q)) for C in partition)==len(digit_image(A,q)), 'factor cardinality mismatch')
    return partition,primitives
