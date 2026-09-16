#!/usr/bin/env python3
"""Exact finite certificates for the recurrence-control research note.

All arithmetic is integral or Fraction arithmetic. The all-length implications
are proved in the companion note; this file checks complete finite carry
closures and precisely bounded calibrations. It is not a Lean certificate.
"""
from __future__ import annotations
from collections import Counter, defaultdict, deque
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import json

CARRIES = ((-2, 1), (-1, 0), (0, 0), (1, 0), (2, -1))
MOTIF_COLUMNS = ((1,0,0),(0,1,0),(1,2,0),(0,0,1),(0,1,2),(1,4,4))
MOTIF_MASKS = (1,11,19,28,32,42,50)


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def pell(n: int) -> tuple[int, ...]:
    a = [1,2]
    while len(a) < n:
        a.append(2*a[-1]+a[-2])
    return tuple(a[:n])


def sign_quadratic(a: int, b: int) -> int:
    """Sign of a+b*sqrt(2), with no floating point."""
    if not b:
        return (a > 0)-(a < 0)
    if not a:
        return (b > 0)-(b < 0)
    if a*b > 0:
        return (a > 0)-(a < 0)
    d = a*a-2*b*b
    return ((d > 0)-(d < 0)) if a > 0 else ((d < 0)-(d > 0))


def bounded_pair(u: int,v: int) -> bool:
    return (sign_quadratic(u+v,v-1)<0 and sign_quadratic(-u-v,-v-1)<0
            and sign_quadratic(u+v-2,-v-1)<0
            and sign_quadratic(-u-v-2,v-1)<0)


def state_json(s: tuple) -> list:
    return [[list(p) for p in s[0]], s[1]]


def build_graph(k: int) -> dict:
    initial = (((0,0),)*(k-2),False)
    discovered = {initial}
    queue = deque([initial])
    raw = []
    while queue:
        state = queue.popleft()
        carry, flagged = state
        for digits in product((0,1),repeat=k):
            delta = tuple(digits[i]-2*digits[i+1]+digits[i+2] for i in range(k-2))
            target_c = tuple((v+d,u+2*v) for (u,v),d in zip(carry,delta))
            if any(c not in CARRIES for c in target_c):
                continue
            target = (target_c, flagged or digits[0] != digits[1])
            raw.append((state,target,digits))
            if target not in discovered:
                discovered.add(target)
                queue.append(target)
    states = sorted(discovered)
    index = {s:i for i,s in enumerate(states)}
    edges = sorted((index[s],index[t],list(d)) for s,t,d in raw)
    accepting = [index[s] for s in states if s[1] and all(u+2*v==0 for u,v in s[0])]
    counts=[]
    vector=[0]*len(states)
    vector[index[initial]]=1
    for n in range(41):
        ordered=sum(vector[i] for i in accepting)
        require(ordered%2==0,"tuple reversal failed")
        counts.append(ordered//2)
        nxt=[0]*len(states)
        for s,t,d in edges:
            nxt[t]+=vector[s]
        vector=nxt
    return {"k":k,"states":[state_json(s) for s in states],"initial":index[initial],
            "accepting":accepting,"edges":[list(e) for e in edges],
            "positive_ap_counts_n0_through40":counts}


def bit_image(a: tuple[int, ...]) -> int:
    bits=1
    for x in a:
        require(x>0,"positive generator required")
        bits |= bits<<x
    return bits


def ap_count_bits(bits: int,k: int) -> int:
    maximum=bits.bit_length()-1
    result=0
    for d in range(1,maximum//(k-1)+1):
        starts=bits
        for j in range(1,k):
            starts &= bits>>(j*d)
            if not starts:
                break
        result += starts.bit_count()
    return result


def primitive(z: tuple, a: tuple[int,...]) -> tuple:
    """Original triangular primitive after retaining the scalar section."""
    remainder=list(z)
    coefficients=[0]*max(0,len(z)-1)
    for j in range(len(z)-1,0,-1):
        c=remainder[j]
        coefficients[j-1]=c
        remainder[j]=0
        remainder[j-1]+=2*c
        if j>=2:
            remainder[j-2]+=c
    require(remainder[0]==sum(x*y for x,y in zip(z,a)),"scalar section changed")
    return tuple(coefficients)


def boundary(c: tuple) -> tuple:
    n=len(c)+1
    out=[0]*n
    for j,t in enumerate(c,1):
        out[j]+=t
        out[j-1]-=2*t
        if j>=2:
            out[j-2]-=t
    return tuple(out)


def relation_checks() -> dict:
    digest=sha256();count=0;sections=0
    for n in range(1,81):
        a=pell(n+1);W=sum(x*x for x in a[:n])
        require(2*W==a[n-1]*a[n],"Pell square sum identity")
        for j in range(n):
            z=tuple(int(i==j) for i in range(n))
            c=primitive(z,a[:n]);dz=boundary(c)
            require(tuple(dz[i]+(a[j] if i==0 else 0) for i in range(n))==z,
                    "integral contraction identity")
            count+=1
        for seed in range(7):
            c=tuple(((j+3)*(seed+2)%9)-4 for j in range(n-1))
            dz=boundary(c)
            require(sum(x*y for x,y in zip(dz,a))==0,"boundary not arithmetic zero")
            require(primitive(dz,a[:n])==c,"primitive inverse")
            ext=(0,)+c+(0,0)
            rhs=4*sum(t*t for t in c)+sum((ext[j+2]-ext[j])**2 for j in range(n))
            require(sum(t*t for t in dz)==rhs,"exact coercivity identity")
            digest.update((repr((n,seed,c,dz,rhs))+"\n").encode())
        section=tuple(Fraction(x,W) for x in a[:n])
        require(sum(x*y for x,y in zip(section,a))==1,"section evaluation")
        require(sum(x*x for x in section)==Fraction(1,W),"quotient Gram")
        if n>=2:
            older=pell(n-1);oldW=sum(x*x for x in older)
            old=tuple(Fraction(x,oldW) for x in older)+(Fraction(0),)
            diff=tuple(x-y for x,y in zip(old,section))
            dc=primitive(diff,a[:n])
            require(boundary(dc)==diff,"section correction has no old primitive")
            require(sum(x*x for x in diff)==Fraction(1,oldW)-Fraction(1,W),"secant metric")
            sections+=1
    return {"max_n":80,"basis_identities":count,"coercivity_vectors":80*7,
            "section_secants":sections,"transcript_sha256":digest.hexdigest()}


def gap(a: tuple[int,...],r: int=2) -> bool:
    if not a or any(x<=0 for x in a):
        return False
    for j in range(1,len(a)):
        earlier=sum(a[:j])
        if j<r:
            if a[j]<=earlier:
                return False
        elif a[j]<=earlier+sum(a[:j-r+1]):
            return False
    return True


def gap_checks() -> dict:
    digest=sha256();total=0
    for n in range(1,8):
        for first in (1,2):
            for gs in product((1,2,3),repeat=max(0,n-1)):
                a=[first]
                if n>=2:
                    a.append(first+gs[0])
                for j in range(2,n):
                    a.append(a[-1]+2*sum(a[:-1])+gs[j-1])
                a=tuple(a)
                require(gap(a),"generated gap data invalid")
                bits=bit_image(a)
                require(bits.bit_count()==2**n,"binary representation collision")
                require(ap_count_bits(bits,5)==0,"gap theorem finite failure")
                require(all(x>=y for x,y in zip(a,pell(n))),"gap minimality failed")
                total+=1;digest.update((repr(a)+"\n").encode())
    dyadic=[]
    for r in range(2,7):
        a=[2**j for j in range(r)]
        while len(a)<min(r+4,11):
            a.append(2*a[-1]+a[-r])
        for n in range(r,len(a)+1):
            prefix=tuple(a[:n]);bits=bit_image(prefix)
            require(gap(prefix,r),"dyadic gap failed")
            require(ap_count_bits(bits,2**r+1)==0,"dyadic maximal progression failed")
            require(all((bits>>x)&1 for x in range(2**r)),"initial dyadic progression lost")
            dyadic.append({"r":r,"n":n,"weights":list(prefix),"longest":2**r})
    return {"literal_gap_domain":"n=1..7; first in {1,2}; each positive gap in {1,2,3}",
            "gap_cases":total,"transcript_sha256":digest.hexdigest(),"dyadic_cases":dyadic}


def motif_checks() -> dict:
    values=[tuple(sum(MOTIF_COLUMNS[j][i] for j in range(6) if m>>j&1)
                  for i in range(3)) for m in MOTIF_MASKS]
    require(values==[(1,j,j) for j in range(7)],"universal motif identity")
    rels=((-1,-2,1,0,0,0),(0,-1,0,-2,1,0),(0,0,-1,0,-2,1))
    ds=[]
    for i in range(5):
        v=[((MOTIF_MASKS[i]>>j)&1)-2*((MOTIF_MASKS[i+1]>>j)&1)
           +((MOTIF_MASKS[i+2]>>j)&1) for j in range(6)]
        c3=v[5];c1=v[2]+c3;c2=v[4]+2*c3
        reconstructed=[sum(c*r[j] for c,r in zip((c1,c2,c3),rels)) for j in range(6)]
        require(reconstructed==v,"original relation primitive for motif")
        ds.append([c1,c2,c3])
    applications=[]
    for delay in range(3,33):
        for seed_id in range(3):
            a=[(seed_id+1)*2**j+seed_id for j in range(delay)]
            while len(a)<=2*delay:
                a.append(2*a[-1]+a[-delay])
            indices=(0,delay-1,delay,2*delay-2,2*delay-1,2*delay)
            require(len(set(indices))==6,"motif aliases were discarded")
            weights=[a[j] for j in indices]
            require(len(set(weights))==6,"repeated numerical generator")
            ys=[sum(weights[j] for j in range(6) if m>>j&1) for m in MOTIF_MASKS]
            step=a[delay-1]+a[2*delay-2]
            require(ys==[a[0]+j*step for j in range(7)],"delayed recurrence witness")
            applications.append({"delay":delay,"initial":a[:delay],"indices":list(indices),
                                 "weights":weights,"step":step,"points":ys})
    alias=(0,1,2,2,3,4)
    alias_words=[[sum(int(alias[j]==i and (mask>>j&1)) for j in range(6))
                  for i in range(5)] for mask in MOTIF_MASKS]
    a=pell(5);ys=[sum(x*y for x,y in zip(w,a)) for w in alias_words]
    require(alias_words[3][2]==2,"alias regression failed")
    require(ys==[1+7*j for j in range(7)],"alias numerical pattern changed")
    require(not (bit_image(a)>>ys[3]&1),"unsupported central value unexpectedly present")
    return {"columns":[list(v) for v in MOTIF_COLUMNS],"masks":list(MOTIF_MASKS),
            "vector_values":[list(v) for v in values],"relation_rows":[list(r) for r in rels],
            "second_difference_primitives":ds,"applications":applications,
            "delay_two_alias":{"coordinate_map":list(alias),"pushed_words":alias_words,
                               "scalar_values":ys,"missing_value":ys[3]}}


def gf_checks(g: dict) -> dict:
    # The fixed denominator is verified as an identity of the reachable machine,
    # not merely guessed from a finite prefix of coefficients.
    N=len(g["states"]);initial=g["initial"];edges=g["edges"];accept=g["accepting"]
    v=[0]*N;v[initial]=1
    rows=[v]
    for j in range(3):
        nxt=[0]*N
        for s,t,d in edges:nxt[t]+=rows[-1][s]
        rows.append(nxt)
    residual=[rows[3][i]-3*rows[2][i]-2*rows[1][i]+8*rows[0][i] for i in range(N)]
    # A residual row is observationally zero iff its first N outputs vanish,
    # by the characteristic polynomial of the N by N integer matrix.
    outputs=[]
    for j in range(N):
        outputs.append(sum(residual[i] for i in accept))
        nxt=[0]*N
        for s,t,d in edges:nxt[t]+=residual[s]
        residual=nxt
    require(not any(outputs),"rational generating identity failed")
    c=g["positive_ap_counts_n0_through40"]
    require(c[:3]==[0,0,1],"initial four-AP count")
    return {"numerator":[0,0,1],"denominator":[1,-3,-2,8],
            "machine_dimension":N,"residual_outputs":outputs,
            "method":"N zero outputs of the exact recurrence residual, then Cayley-Hamilton"}


def general_operator_checks() -> dict:
    digest=sha256();cases=0
    for delay in range(2,25):
        m=delay-1
        for n in (1,2,3,7,17,41):
            for seed in range(5):
                x=[((j+1)*(seed+3)+delay)%11-5 for j in range(n)]
                D=[-2*x[j]+(x[j-1] if j else 0)-(x[j+m] if j+m<n else 0)
                   for j in range(n)]+[x[-1]]
                ip=-sum(D[j]*x[j] for j in range(n))
                xx=x+[0]*(m+1)
                one=[xx[j]-(xx[j-1] if j else 0) for j in range(n+m+1)]
                other=[xx[j]+(xx[j-m] if j>=m else 0) for j in range(n+m+1)]
                require(2*ip==sum(y*y for y in one)+sum(y*y for y in other),
                        "full unilateral-shift energy identity")
                require(m*m*ip>=2*sum(y*y for y in x),"delay-uniform accretivity")
                require(m**4*sum(y*y for y in D)>=4*sum(y*y for y in x),
                        "delay-uniform inverse norm bound")
                cases+=1;digest.update((repr((delay,n,seed,D,ip))+"\n").encode())
    return {"delay_range":[2,24],"lengths":[1,2,3,7,17,41],"vectors_per_pair":5,
            "cases":cases,"transcript_sha256":digest.hexdigest()}


def algebraic_carrier_checks() -> list[dict]:
    records=[]
    for delay in range(2,7):
        delta=Fraction(2,(delay-1)**2*(3*delay-2))
        bound=Fraction(2*(delay-1)*(delay+2)*2**(delay-1)*3**(delay-2),delay)/delta**3
        C=(bound.numerator+bound.denominator-1)//bound.denominator
        a=[2**j for j in range(delay)]
        while len(a)<7:a.append(2*a[-1]+a[-delay])
        total=zero=prefixes=0;digest=sha256()
        for n in range(7):
            for word in product(range(-2,3),repeat=n):
                total+=1
                state=[0]*delay;history=[]
                for c in reversed(word):
                    old=state[-1]
                    state=[old+c]+state[:-1]
                    state[-1]+=2*old
                    history.append(tuple(state))
                require(sum(state[i]*2**i for i in range(delay))==sum(c*t for c,t in zip(word,a)),
                        "original quotient/scalar square")
                if sum(c*t for c,t in zip(word,a)):
                    continue
                zero+=1;prefixes+=len(history)
                require(all(abs(v)<=C for row in history for v in row),"coarse all-delay carrier")
                if delay==2:
                    require(all(tuple(row) in CARRIES for row in history),"sharp Pell carrier refinement")
                digest.update((repr((word,history))+"\n").encode())
        records.append({"delay":delay,"coefficient_bound":2,"max_word_length":6,
                        "delta":str(delta),"coefficient_cutoff":C,"words":total,
                        "scalar_zero_words":zero,"zero_word_prefixes":prefixes,
                        "transcript_sha256":digest.hexdigest()})
    return records


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    actual=tuple((u,v) for u in range(-5,6) for v in range(-2,3) if bounded_pair(u,v))
    require(actual==CARRIES,"five scalar carry states")
    graphs=[build_graph(k) for k in (3,4,5,6)]
    require(not graphs[2]["accepting"],"five-AP machine accepts")
    direct=[]
    for n in range(1,14):
        a=pell(n);bits=bit_image(a)
        require(bits.bit_count()==2**n,"Pell binary injection")
        counts={str(k):ap_count_bits(bits,k) for k in (3,4,5)}
        for i,k in enumerate((3,4,5)):
            require(counts[str(k)]==graphs[i]["positive_ap_counts_n0_through40"][n],
                    "direct arithmetic and algebraic carry counts differ")
        direct.append({"n":n,"maximum":a[-1],"image_size":2**n,"positive_ap_counts":counts})
    report={"schema":"ep817-recurrence-control-v1","status":"PASS","lean_checked":False,
            "scope":"Exact finite graphs and bounded replays; infinite proofs in the accompanying notes.",
            "scalar_carries":[list(x) for x in CARRIES],"graphs":graphs,
            "direct_pell_checks":direct,"four_ap_generating_function":gf_checks(graphs[1]),
            "relations_and_metrics":relation_checks(),"gap_and_dyadic_checks":gap_checks(),
            "general_recurrence_operators":general_operator_checks(),
            "all_delay_algebraic_carrier":algebraic_carrier_checks(),
            "seven_ap_motif":motif_checks(),
            "validator_sha256":sha256(Path(__file__).read_bytes()).hexdigest()}
    rendered=json.dumps(report,indent=2,sort_keys=True)+"\n"
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(rendered,encoding="utf-8")
    print(json.dumps({"status":"PASS","receipt":str(args.output),
                      "graphs":[[g['k'],len(g['states']),len(g['edges'])] for g in graphs],
                      "gap_cases":report['gap_and_dyadic_checks']['gap_cases']},sort_keys=True))

if __name__=="__main__":
    main()
