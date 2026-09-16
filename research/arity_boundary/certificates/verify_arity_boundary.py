#!/usr/bin/env python3
"""Reproduce exact image, moment, metric and real-boundary certificates.

All computations are bounded and use the standard library. General all-length
claims are proved in the companion notes, not inferred from finite sampling.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from arity_core import *


def rat(x):return str(Fraction(x))

def modular_safe(D,b,k):
    bits=sum(1<<d for d in D);mask=(1<<b)-1
    require(max(D)<b,"noncanonical modular digits")
    for d in range(1,b):
        starts=bits
        for i in range(1,k):
            s=(i*d)%b
            starts &= bits if s==0 else ((bits>>s)|(bits<<(b-s)))&mask
            if not starts:break
        require(not starts,f"forbidden modular progression, b={b}, k={k}, d={d}")
    return b*(b-1)


def check_formula(machine,moms,num,den):
    # den is the denominator of the length-generating series, in ascending powers.
    M=machine['matrix'];f=machine['terminal'];d=len(den)-1
    p=list(reversed(den));shift=max(0,len(num)-d)
    obs=check_observed_recurrence(M,f,0,p,shift)
    seq=[x[0]for x in moms]
    for m in range(len(seq)):
        coefficient=sum(den[j]*seq[m-j]for j in range(min(d,m)+1))
        require(coefficient==(num[m]if m<len(num)else 0),"generating-series numerator mismatch")
    return {"numerator":num,"denominator":den,"recurrence_polynomial":p,
            "recurrence_shift":shift,"finite_observations":obs}


def denominator(roots):
    p=[1]
    for r in roots:
        q=[0]*(len(p)+1)
        for j,a in enumerate(p):q[j]+=a;q[j+1]-=r*a
        p=q
    return p


def record(A,b,k):
    binary=digit_weights(A,2)
    pairs=modular_safe(binary,b,k)
    arities=[]
    for q in range(2,8):
        weights=digit_weights(A,q);D=set(weights);machine=carry_machine(D,b)
        mm=moments(machine,20,2)
        if q==2:num=[1];den=denominator([len(D)])
        elif len(A)==6 and q==3:num=[1,len(D)-b-3];den=denominator([b,3])
        elif len(A)==6:
            num=[1,(q-1)*sum(A)-b];den=denominator([b,1])
        elif q==3:num=[1,363];den=denominator([b,89])
        elif q==4:num=[1,1644,-1645];den=denominator([b,3,3])
        elif q==5:num=[1,2749,3302];den=denominator([b,3])
        else:num=[1,(q-1)*sum(A)-b-6,6*b];den=denominator([b,1])
        formula=check_formula(machine,mm,num,den)
        for m,(N,S1,S2)in enumerate(mm):
            width=(q-1)*sum(A)*(b**m-1)//(b-1)
            require(2*S1==N*width,"reflection mean failed")
            require(12*(N*S2-S1*S1)>=N*N*(N*N-1),"integer spacing variance failed")
        arities.append({"arity":q,"digit_weights":[[d,weights[d]]for d in sorted(weights)],
                        "machine":machine,"moments_through_m20":mm,"series":formula})
    ternary=arities[1];weights=dict(ternary['digit_weights']);D=set(weights)
    hole=hole_certificate(D,b);eps=endpoint_moments(hole,b,20)
    require(eps==ternary['moments_through_m20'],"two independent moment recurrences disagree")
    for m,v in enumerate(eps):require(v[0]==count_run_formula(len(D),b,hole['kappa'],m),"run count formula failed")
    weighted=weighted_certificate(weights,b)
    peak=weighted['maximum_original_multiplicity'];r=weighted['all_ones_output_digit'];c=weighted['constant_output_digit']
    for m in range(1,13):
        rep=(b**m-1)//(b-1)
        require(exact_coefficient(weights,b,m,c*rep)==peak**m,"original peak witness failed")
        require(exact_coefficient({d:1 for d in D},b,m,r*rep)==2**(m-1),"distinct-digit peak witness failed")
    B,f,out=moment_matrix(ternary['machine'],2);K=hole['kappa']
    roots=[K,b,b*K,b*b,K*b*b,b**3]
    p=poly_from_roots(roots);obs=check_observed_recurrence(B,f,out,p)
    coefficients=solve_square([[x**m for x in roots]for m in range(len(roots))],
                              [v[2]for v in eps[:len(roots)]])
    require(all(sum(c*x**m for c,x in zip(coefficients,roots))==v[2]for m,v in enumerate(eps)),"second moment closed form mismatch")
    C0=Fraction(len(D)-K,b-K);span=Fraction(max(D),b-1)
    scaled_variance=coefficients[-1]/C0-span**2/4
    original_Q=sum(a*a for a in A)
    variance_Q_ratio=scaled_variance*(b*b-1)/original_Q
    require(scaled_variance>0 and variance_Q_ratio>1,"variance constants invalid")
    nonzero=[(i,j)for i,a in enumerate(A)for j,c in enumerate(A)if c-a==1]
    require(nonzero,"no unit top-block relation")
    i,j=nonzero[0]
    # An actual ternary representation of b is the lower-block primitive.
    def representative(target):
        reps={0:()}
        for a in A:
            nxt={}
            for x,word in reps.items():
                for z in range(3):nxt.setdefault(x+z*a,word+(z,))
            reps=nxt
        require(target in reps,"missing cross-level ternary representation")
        return reps[target]
    if 1 in A:
        top=[0]*len(A);top[A.index(1)]=1
    else:
        top=[0]*len(A);top[i]=-1;top[j]=1
    low=representative(b)
    require(sum(x*a for x,a in zip(low,A))==b*sum(x*a for x,a in zip(top,A)),"cross-level kernel witness invalid")
    return {"generators":list(A),"base":b,"forbidden_length":k,"modular_pairs":pairs,
            "binary_size":len(binary),"arities":arities,"ternary_holes":hole,
            "weighted_metric_certificate":weighted,
            "raw_second_moment":{"roots":roots,"coefficients":[rat(x)for x in coefficients],
                "annihilator":p,"finite_observations":obs},
            "limit":{"ternary_mass":rat(C0),"span":rat(span),"remaining_outer_mass":rat(span-C0),
                "scaled_uniform_variance":rat(scaled_variance),"variance_over_Q":rat(variance_Q_ratio)},
            "cross_level_relation":{"lower":list(low),"upper":top}}


def toy_replays():
    n=0;comparison=0;hole_n=0;digest=sha256()
    for b in range(2,7):
        W=min(2*b-2,8)
        for bits in range(1<<W):
            D={0}|{j for j in range(1,W+1)if (bits>>(j-1))&1}
            machine=carry_machine(D,b);mm=moments(machine,3,3)
            image={0}
            for m in range(4):
                direct=[sum(x**p for x in image)for p in range(4)]
                require(direct==mm[m],"direct image/moment mismatch in exhaustive digit replay")
                comparison+=1
                image={d+b*x for d in D for x in image}
            if b<max(D,default=0)<=2*b-2:
                try:h=hole_certificate(D,b)
                except AssertionError:pass
                else:
                    ep=endpoint_moments(h,b,5)
                    machine_mm=moments(machine,5,2)
                    require(ep==machine_mm,"toy hole/moment disagreement")
                    hole_n+=1
            n+=1;digest.update((repr((b,sorted(D),mm))+'\n').encode())
    # Exact quotient norm/section identities on representative small weighted fibers.
    metric_cases=0
    for A in ((1,3),(1,4,5),(1,3,4,7)):
        for q in (2,3,4):
            w=digit_weights(A,q);b=sum(A)+1
            fibers={}
            for d,wd in w.items():
                for e,we in w.items():fibers.setdefault(d+b*e,[]).append((d,e,wd*we))
            for x,rows in fibers.items():
                mass=sum(t for _,_,t in rows)
                norm=sum(Fraction(t,mass)**2/Fraction(t) for _,_,t in rows)
                require(norm==Fraction(1,mass),"least-norm quotient section failed")
                require(sum(Fraction(t,mass)for _,_,t in rows)==1,"section right inverse failed")
                metric_cases+=1
    return {"digit_alphabets":n,"moment_comparisons":comparison,"valid_hole_cases":hole_n,
            "weighted_fibers":metric_cases,"transcript_sha256":digest.hexdigest()}


def real_boundary():
    examples=[(A3,19,4,[0,0,1,1],[0,9,0,9]),
              (A6,97,5,[4,5,5,5,6],[64,0,32,64,0]),
              (A6,93,6,[0,0,0,0,1,1],[4,26,48,70,0,22]),
              (A10,1651,6,[293,293,294,294,294,295],[548,1099,0,551,1102,3])]
    data=[]
    for A,b,k,pre,tail in examples:
        reps={}
        for mask in range(1<<len(A)):
            val=sum(a for i,a in enumerate(A)if (mask>>i)&1)
            reps.setdefault(val,mask)
        require(all(x in reps for x in pre+tail),"real witness leaves original binary image")
        require(delta(tail)==tuple(-(b-1)*c for c in delta(pre)) and any(delta(pre)),"constant-boundary identity failed")
        xs=evaluate_real([pre],[tail],b)
        prefixes=[]
        for m in range(1,13):
            Y=[a*b**(m-1)+e*(b**(m-1)-1)//(b-1)for a,e in zip(pre,tail)]
            require(delta(Y)==delta(pre),"integer terminal boundary lost")
            for x,y,e in zip(xs,Y,tail):require(x-Fraction(y,b**m)==Fraction(e,(b-1)*b**m),"real tail identity failed")
            prefixes.append({"length":m,"integer_points":Y,"second_difference":list(delta(Y))})
        data.append({"base":b,"k":k,"generators":list(A),"prefix":pre,"period":tail,
                     "prefix_masks":[reps[d]for d in pre],"period_masks":[reps[d]for d in tail],
                     "values":[rat(x)for x in xs],"difference":rat(xs[1]-xs[0]),"finite_prefixes":prefixes})
    machines=[]
    for A,b,k in ((A3,19,4),(A6,97,5),(A6,93,6)):
        D=digit_weights(A,2);g=real_machine(D,b,k)
        require(g['witness']is not None,"expected real progression missing")
        evaluate_real(g['witness']['prefix'],g['witness']['period'],b)
        machines.append(g)
    total=safe=0;digest=sha256()
    for b in range(3,8):
        for mask in range(1<<(b-2)):
            D={0}|{d for d in range(1,b-1)if (mask>>(d-1))&1}
            for k in range(3,6):
                g=real_machine(D,b,k);total+=1
                if g['witness']is None:safe+=1
                else:evaluate_real(g['witness']['prefix'],g['witness']['period'],b)
                digest.update((repr((b,sorted(D),k,len(g['states']),g['witness']))+'\n').encode())
    return {"examples":data,"complete_record_machines":machines,
            "small_domain":{"bases":[3,7],"lengths":[3,5],"alphabets_and_lengths":total,
                            "no_real_ap":safe,"real_ap":total-safe,"transcript_sha256":digest.hexdigest()}}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    records=[record(A6,97,5),record(A6,93,6),record(A10,1651,6)]
    # The retained size-two Jordan block is observable, not an inferred fit.
    q4=records[2]['arities'][2];M=q4['machine']['matrix'];n=len(M)
    N=[[M[i][j]-(3 if i==j else 0)for j in range(n)]for i in range(n)]
    N2=[[sum(N[i][h]*N[h][j]for h in range(n))for j in range(n)]for i in range(n)]
    require(rational_rank(N)==4 and rational_rank(N2)==3,"Jordan chain disappeared")
    seq=[x[0]for x in q4['moments_through_m20']]
    require(rational_rank([[seq[i+j]for j in range(5)]for i in range(5)])==3,"observable realization dimension mismatch")
    report={"schema":"ep817-arity-boundary-v1","status":"PASS","lean_checked":False,
        "records":records,"small_exact_replays":toy_replays(),"real_boundary":real_boundary(),
        "jordan_certificate":{"rank_M_minus_3I":4,"rank_square":3,"observable_hankel_rank":3},
        "source_sha256":{f:sha256(Path(__file__).with_name(f).read_bytes()).hexdigest()
                         for f in ('arity_core.py','verify_arity_boundary.py')}}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({"status":"PASS","records":len(records),"toy":report['small_exact_replays'],
                      "real":report['real_boundary']['small_domain'],
                      "source_sha256":report['source_sha256']},indent=2))

if __name__=='__main__':main()
