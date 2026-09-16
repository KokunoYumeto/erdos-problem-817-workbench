"""Exact finite carry graph for k-APs in base-b digit languages."""
from __future__ import annotations
from collections import deque
from itertools import product

def require(ok: bool, message: str) -> None:
    if not ok: raise AssertionError(message)

def subset_sums(a: tuple[int, ...]) -> set[int]:
    out = {0}
    for v in a: out |= {s + v for s in tuple(out)}
    return out

def bit_sums(a: tuple[int, ...]) -> int:
    out = 1
    for v in a: out |= out << v
    return out

def int_ap_bits(bits: int, k: int) -> tuple[int, int] | None:
    for step in range(1, (bits.bit_length()-1)//(k-1)+1):
        hits = bits
        for i in range(1,k): hits &= bits >> (i*step)
        if hits: return ((hits & -hits).bit_length()-1,step)
    return None

def modular_witness(digits: set[int], b: int, k: int) -> tuple[int, int] | None:
    for start in sorted(digits):
        for step in range(1,b):
            if all((start+i*step)%b in digits for i in range(k)):
                return start,step
    return None

def successors(c: tuple[int,...], digits: tuple[int,...], b: int):
    allowed = set(digits)
    for first in digits:
        for second in digits:
            column = [first,second]; target=[]
            for ci in c:
                u,v=column[-2:]
                w=(2*v-u-ci)%b
                if w not in allowed: break
                target.append((w-2*v+u+ci)//b);column.append(w)
            else:
                yield tuple(target),tuple(column)

def carry_certificate(digits: set[int], b: int, k: int) -> dict:
    require(b>=2 and k>=3 and bool(digits), 'invalid base, length, or digits')
    require(min(digits)>=0 and max(digits)<b, 'digits must lie in [0,b)')
    zero=(0,)*(k-2); initial=(zero,False)
    queue=deque([initial]);parent={initial:None}; edges=0
    while queue:
        c,flag=state=queue.popleft()
        for cc,column in successors(c,tuple(sorted(digits)),b):
            edges+=1
            require(all(-1<=v<=1 for v in cc),'carry bound')
            ff=flag or column[0]!=column[1];nxt=(cc,ff)
            if nxt in parent:continue
            parent[nxt]=(state,column)
            if cc==zero and ff:
                cols=[];at=nxt
                while parent[at] is not None:
                    before,col=parent[at];cols.append(col);at=before
                cols.reverse()
                values=[sum(col[i]*b**j for j,col in enumerate(cols)) for i in range(k)]
                require(values[1]!=values[0], 'constant alleged witness')
                require(all(values[i+2]-2*values[i+1]+values[i]==0 for i in range(k-2)), 'invalid witness')
                return {'safe':False,'states_seen':len(parent),'edges_examined':edges,
                        'columns':cols,'witness':values,'length':len(cols)}
            queue.append(nxt)
    states=sorted((list(c),flag) for c,flag in parent)
    return {'safe':True,'states_seen':len(parent),'edges_examined':edges,'closed_states':states}

def verify_closed_certificate(digits: set[int], b: int, k: int, certificate: dict) -> int:
    """Independent edge generator: enumerate columns via arithmetic congruences."""
    require(certificate['safe'] is True,'positive certificate required')
    require(b >= 2 and k >= 3 and bool(digits) and min(digits) >= 0 and max(digits) < b, "invalid verifier domain")
    states={(tuple(c),f) for c,f in certificate['closed_states']}
    require(all(len(c) == k-2 and all(isinstance(x,int) and -1 <= x <= 1 for x in c) and isinstance(f,bool) for c,f in states), "invalid canonical state")
    zero=(0,)*(k-2);require((zero,False) in states,'missing initial state')
    require((zero,True) not in states,'accepting state present')
    checked=0
    # Direct k-fold enumeration is used only in deliberately small test domains.
    for column in product(sorted(digits), repeat=k):
        delta=tuple(column[i+2]-2*column[i+1]+column[i] for i in range(k-2))
        for c,flag in states:
            if any((x+y)%b for x,y in zip(c,delta)):continue
            cc=tuple((x+y)//b for x,y in zip(c,delta))
            require((cc,flag or column[0]!=column[1]) in states,'closure failed')
            checked+=1
    return checked

def power_alias(a: tuple[int,...], b: int) -> tuple[int,int,int] | None:
    require(b>=2, 'base must be at least two')
    require(all(isinstance(x,int) and x > 0 for x in a) and len(set(a)) == len(a), "generators must be distinct positive integers")
    allowed=set(a)
    for x in a:
        value=x*b; exponent=1
        while value<=max(a,default=0):
            if value in allowed:return x,value,exponent
            value*=b;exponent+=1
    return None

def full_successors(c: tuple[int,...], h: int, digits: tuple[int,...], b: int):
    residues={r:tuple(d for d in digits if d%b==r) for r in range(b)}
    def finish(column, target):
        i=len(target)
        if i==len(c):
            z=h+column[1]-column[0]
            yield tuple(target),z//b,z%b!=0,tuple(column)
            return
        u,v=column[-2:]
        for w in residues[(2*v-u-c[i])%b]:
            yield from finish(column+[w],target+[(w-2*v+u+c[i])//b])
    for first in digits:
        for second in digits:
            yield from finish([first,second],[])

def full_carry_certificate(digits: set[int], b: int, k: int) -> dict:
    require(b>=2 and k>=3 and bool(digits) and min(digits)>=0,'invalid full carry input')
    S=max(digits);C=(2*S+b-2)//(b-1);H=(S+b-2)//(b-1)
    zero=(0,)*(k-2);initial=(zero,0,False)
    queue=deque([initial]);parent={initial:None};edges=0
    while queue:
        c,h,flag=state=queue.popleft()
        for cc,hh,mark,column in full_successors(c,h,tuple(sorted(digits)),b):
            edges+=1;ff=flag or mark;nxt=(cc,hh,ff)
            require(all(-C<=x<=C for x in cc) and -H<=hh<=H,'full carry bound')
            if nxt in parent:continue
            parent[nxt]=(state,column)
            if cc==zero and (ff or hh!=0):
                cols=[];at=nxt
                while parent[at] is not None:
                    before,col=parent[at];cols.append(col);at=before
                cols.reverse()
                values=[sum(col[i]*b**j for j,col in enumerate(cols)) for i in range(k)]
                require(values[1]!=values[0], 'full carry constant alleged witness')
                require(all(values[i+2]-2*values[i+1]+values[i]==0 for i in range(k-2)), 'full carry invalid witness')
                return {'safe':False,'carry_bound':C,'slope_bound':H,'states_seen':len(parent),
                        'edges_examined':edges,'columns':cols,'witness':values,'length':len(cols)}
            queue.append(nxt)
    states=sorted((list(c),h,f) for c,h,f in parent)
    return {'safe':True,'carry_bound':C,'slope_bound':H,'states_seen':len(parent),
            'edges_examined':edges,'closed_states':states}

def verify_full_closed(digits: set[int], b: int, k: int, cert: dict) -> int:
    require(cert['safe'],'full positive certificate required')
    require(b >= 2 and k >= 3 and bool(digits) and min(digits) >= 0, 'invalid full verifier domain')
    S=max(digits);C=(2*S+b-2)//(b-1);H=(S+b-2)//(b-1)
    states={(tuple(c),h,f) for c,h,f in cert['closed_states']};zero=(0,)*(k-2)
    require(all(len(c)==k-2 and all(isinstance(x,int) and -C<=x<=C for x in c) and isinstance(h,int) and -H<=h<=H and isinstance(f,bool) for c,h,f in states), 'invalid full state')
    require((zero,0,False) in states,'missing full initial')
    require(all(c!=zero or (h==0 and not f) for c,h,f in states),'full accepting state present')
    count=0
    for column in product(sorted(digits),repeat=k):
        delta=tuple(column[i+2]-2*column[i+1]+column[i] for i in range(k-2))
        for c,h,flag in states:
            if any((x+y)%b for x,y in zip(c,delta)):continue
            cc=tuple((x+y)//b for x,y in zip(c,delta));z=h+column[1]-column[0]
            require((cc,z//b,flag or z%b!=0) in states,'full closure failed')
            count+=1
    return count
