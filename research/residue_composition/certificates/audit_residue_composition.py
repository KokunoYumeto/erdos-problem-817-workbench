#!/usr/bin/env python3
"""Independent finite audit; imports no producer or arithmetic helper.

Numerical images are computed by bit polynomials. The AB matrices are recovered
by interpolation on actual finite sets. All LP comparisons use integer powers.
"""
from __future__ import annotations
import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path

HERE=Path(__file__).resolve().parent
R=((0,),(0,1),(0,2),(0,1,2),(0,3),(0,1,3),(0,1,2,3))
AB=((10,(1,3)),(10,(2,4)))


def check(ok,msg):
    if not ok:raise AssertionError(msg)


def bits_image(A,q):
    p=1
    for a in A:
        p=sumset_digit(p,a,q)
    return p


def sumset_digit(p,a,q):
    out=0
    for i in range(q):out |= p << (i*a)
    return out


def bit_values(p):
    out=[]
    while p:
        x=(p & -p).bit_length()-1
        out.append(x);p &= p-1
    return out


def cyclic_bad(D,b,k):
    mask=(1<<b)-1
    p=sum(1<<x for x in D)
    for d in range(1,b):
        starts=p
        for i in range(1,k):
            h=(i*d)%b
            rotated=p if h==0 else ((p>>h)|(p<<(b-h)))&mask
            starts &= rotated
            if not starts:break
        if starts:return True
    return False


def bounded_tuples(n,b,first=1,prefix=()):
    if n==0:
        yield prefix;return
    for a in range(first,b):
        if sum(prefix)+n*a+n*(n-1)//2>=b:break
        yield from bounded_tuples(n-1,b,a+1,prefix+(a,))


def verify_control(row):
    A=tuple(row['weights']);b=row['radix'];n=row['rank'];w=row['six_AP']
    check(len(A)==n and tuple(sorted(set(A)))==A and A[0]>0 and sum(A)<b,'invalid original control source')
    check(0<w['step']<b and 0<=w['start']<b,'invalid nonzero modular step')
    points=[(w['start']+i*w['step'])%b for i in range(6)]
    check(points==w['points'] and len(w['subset_masks'])==6,'corrupt AP tuple')
    for x,mask in zip(points,w['subset_masks']):
        check(0<=mask<(1<<n),'mask outside original binary source')
        check(sum(a for i,a in enumerate(A) if mask>>i&1)==x,'wrong original subset witness')


def audit_residues(rec):
    expected=[]
    for n,bound in ((2,4),(3,12),(4,22)):
        for b in range(2,bound+1):
            for A in bounded_tuples(n,b):expected.append((n,b,A))
    actual=[(x['rank'],x['radix'],tuple(x['weights'])) for x in rec['exceptional_canonical_domains']]
    check(actual==expected and len(actual)==490,'incomplete exceptional canonical domain')
    for row in rec['exceptional_canonical_domains']:verify_control(row)
    check(rec['exceptional_counts']=={'2':1,'3':41,'4':448},'wrong exceptional count')
    for row in rec['stabilizer_reductions']:
        d,V=row['binary_count_lower'],row['ternary_count_upper']
        expected=[[h,z] for h in range(2,V+1) for z in range(h,V+1,h)
                  if z>=d and 2*z-h<=V]
        check(row['all_stabilizer_pairs']==expected,'a Kneser stabilizer case was omitted')
    anchors=[]
    for row in rec['sharp_anchors']:
        A=tuple(row['weights']);b=row['radix'];n=row['rank'];D=bit_values(bits_image(A,2))
        check(not cyclic_bad(D,b,5),'sharp block is not modular-five-free')
        T={x%b for x in bit_values(bits_image(A,3))}
        check(len(T)==(3,5,13,23)[n-1]==b,'sharp ternary residue count')
        reps=row['ternary_representatives']
        check([x['residue'] for x in reps]==list(range(b)),'residue section omitted a supported value')
        for x in reps:
            cs=x['ternary_digits']
            check(len(cs)==n and all(0<=c<=2 for c in cs),'invalid ternary representative')
            check(sum(a*c for a,c in zip(A,cs))==x['actual_value'],'wrong actual digit value')
            check(x['actual_value']%b==x['residue'],'wrong residue section')
        mu={0:1}
        for a in A:
            nxt={}
            for x,c in mu.items():
                for j in range(3):nxt[x+j*a]=nxt.get(x+j*a,0)+c
            mu=nxt
        check(sum(mu.values())==3**n,'original ternary word mass')
        check(len(row['weighted_fibers'])==b,'weighted receiving support incomplete')
        for x,fiber in zip(reps,row['weighted_fibers']):
            r=x['residue'];original={z:c for z,c in mu.items() if z%b==r};total=sum(original.values())
            check(x['actual_value']==min(original),'integral residue section does not use specified least value')
            check(fiber['values_and_word_masses']==[[z,c] for z,c in sorted(original.items())],'receiving mass changed')
            check(fiber['total_word_mass']==total and Fraction(fiber['section_energy'])==Fraction(1,total),'wrong least-norm energy')
            defect=sum((Fraction(int(z==x['actual_value']))-Fraction(c,total))**2/c for z,c in original.items())
            check(defect==Fraction(fiber['integral_section_boundary_energy']),'lost residue-boundary Gram')
            check(defect+Fraction(1,total)==Fraction(1,original[x['actual_value']]),'weighted Pythagoras')
        for sc in row['scaled_cases']:
            g=sc['scale'];C=tuple(sc['weights']);q=sc['radix']
            check(C==tuple(g*a for a in A) and q==g*b,'wrong subgroup inverse data')
            check(not cyclic_bad(bit_values(bits_image(C,2)),q,5),'scaled source has forbidden AP')
            check(len({x%q for x in bit_values(bits_image(C,3))})==b,'lost scaled residue')
        anchors.append((b,A))
    counts=Counter();digest=sha256();kneser_checks=0
    for b in range(2,41):
        for n in range(1,5):
            for A in bounded_tuples(n,b):
                counts['candidate_blocks']+=1
                D=bit_values(bits_image(A,2));V={x%b for x in bit_values(bits_image(A,3))}
                for k in (5,6):
                    if not cyclic_bad(D,b,k):
                        counts[f'safe_k{k}_rank{n}']+=1
                        check(len(V)>=(3,5,13,23)[n-1],'residue lower bound failed')
                        if n==4:check(len(D)>=12,'binary rank-four lower bound')
                        H=[h for h in range(b) if {(x+h)%b for x in V}==V]
                        z=len({(x+h)%b for x in D for h in H})
                        check(len(V)>=2*z-len(H),'finite Kneser arithmetic failed')
                        kneser_checks+=1
                        digest.update((repr((b,A,k,len(D),len(V)))+'\n').encode())
    scan=rec['additional_scan']
    check(all(scan[k]==v for k,v in counts.items()),'additional scan counts differ')
    check(scan['transcript_sha256']==digest.hexdigest(),'additional scan transcript differs')
    equality=[]
    for A in combinations(range(1,25),4):
        if bits_image(A,2).bit_count()==11:
            check(A==tuple(A[0]*i for i in (1,2,3,4)),'equality theorem regression')
            equality.append(list(A))
    check(equality==rec['rank_four_equality_cases_through_max24'],'missing equality case')
    for row in rec['mixed_rank_joins']:
        weights=[];P=1;lower=1
        for i in row['word']:
            b,A=anchors[i];weights.extend(P*x for x in A);P*=b;lower*=b
        n3=bits_image(weights,3).bit_count();n5=bits_image(weights,5).bit_count()
        check((n3,n5,lower)==(row['ternary'],row['fifth'],row['lower_product']),'direct mixed image differs')
        check(lower<=n3<=n5 and len(weights)==row['reward'],'mixed rank budget failed')
    for row in rec['rank_tail_bounds']:
        k=row['k'];base=row['comparison_rate_base'];root=row['comparison_rate_root']
        lo,hi=map(Fraction,row['required_large_rank_fraction_interval'])
        for x,sign in ((lo,1),(hi,-1)):
            expr={23:(1-x)/4,k-1:x,k-2:-x,base:-Fraction(1,root)}
            check(log_sign(expr)==sign,'rank-tail rational enclosure failed')
    return {'complete_obstruction_blocks':490,'complete_additional_blocks':counts['candidate_blocks'],
            'finite_Kneser_checks':kneser_checks,'mixed_original_image_checks':len(rec['mixed_rank_joins'])}


def observation(Y):
    return [len({y+r for y in Y for r in rs}) for rs in R]


def invert(M):
    n=len(M);Q=[[Fraction(x) for x in row]+[Fraction(i==j) for j in range(n)] for i,row in enumerate(M)]
    for j in range(n):
        p=next(i for i in range(j,n) if Q[i][j])
        Q[j],Q[p]=Q[p],Q[j];a=Q[j][j];Q[j]=[x/a for x in Q[j]]
        for i in range(n):
            if i!=j:
                a=Q[i][j];Q[i]=[x-a*y for x,y in zip(Q[i],Q[j])]
    return [x[n:] for x in Q]


def matmul(A,B):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)] for row in A]
def matvec(M,v):return tuple(sum(x*y for x,y in zip(row,v)) for row in M)


def recover_matrices():
    tails=[bit_values(bits_image(A,5)) for A in ((4,),(1,),(2,),(3,),(1,2),(1,6),(2,9))]
    O=list(map(list,zip(*(observation(Y) for Y in tails))))
    inv=invert(O);out=[]
    for _,A in AB:
        D=bit_values(bits_image(A,5))
        Q=list(map(list,zip(*(observation({d+10*y for d in D for y in Y}) for Y in tails))))
        M=matmul(Q,inv)
        check(all(x.denominator==1 and x>=0 for row in M for x in row),'interpolated matrix is not a count matrix')
        out.append(tuple(tuple(int(x) for x in row) for row in M))
    return tuple(out)


def independent_count(Ms,w):
    v=(1,2,2,3,2,3,4)
    for i in reversed(w):v=matvec(Ms[i],v)
    return v[0]


def original_generators(dictionary,w):
    P=1;A=[]
    for i in w:
        b,B=dictionary[i];A.extend(P*x for x in B);P*=b
    check(len(A)==len(set(A)),'cross-level generators not distinct')
    return A


def expected_min(s,t):
    if not s+t:return 1
    if not t:return (16*10**s-7)//9
    if not s:return (4*10**t-1)//3
    if s>=t:
        a,r=divmod(s,t)
        K=lambda j:(80*10**j+37)//9
        return K(a)**(t-r)*K(a+1)**r
    return 93**(s-1)*((28*10**(t-s+1)-1)//3)


def prescribed_word(s,t):
    if not s:return (1,)*t
    if not t:return (0,)*s
    if s>=t:
        a,r=divmod(s,t)
        return ((1,)+(0,)*a)*(t-r)+((1,)+(0,)*(a+1))*r
    return (1,)*(t-s+1)+(0,)+(1,0)*(s-1)


def audit_composition(rec):
    Ms=recover_matrices()
    check([[list(r) for r in M] for M in Ms]==rec['matrices'],'matrix interpolation disagrees')
    states={((1,2,2,3,2,3,4),0):((),1)};cases=0;max_states=0
    for row in rec['all_compositions_through_length18']:
        m=row['length'];nxt={}
        for (v,s),(w,mass) in states.items():
            for i,M in enumerate(Ms):
                key=(matvec(M,v),s+(i==0));word=(i,)+w
                if key in nxt:
                    old,num=nxt[key];nxt[key]=(min(old,word),num+mass)
                else:nxt[key]=(word,mass)
        states=nxt;max_states=max(max_states,len(states))
        check(sum(x[1] for x in states.values())==2**m,'column audit lost a literal word')
        mins={}
        for (v,s),(w,mass) in states.items():
            if s not in mins or (v[0],w)<mins[s]:mins[s]=(v[0],w)
        check(len(row['compositions'])==m+1,'missing fixed-composition class')
        for x in row['compositions']:
            s,t=x['A_count'],x['B_count'];F,w=mins[s]
            check(s+t==m and F==x['minimum']==expected_min(s,t),'minimum count mismatch')
            check(list(w)==x['first_minimizer'],'lexicographic witness mismatch')
            cases+=1
    direct=0
    for m in range(1,7):
        for w in product((0,1),repeat=m):
            direct_value=bits_image(original_generators(AB,w),5).bit_count()
            check(direct_value==independent_count(Ms,w),'direct original q=5 image mismatch')
            direct+=1
    for s in range(31):
        for t in range(31):
            check(independent_count(Ms,prescribed_word(s,t))==expected_min(s,t),'attainer grid failed')
    for x in rec['periodic_excess_examples']:
        s,t=x['A_count'],x['B_count'];b=t-s+1
        ratio=Fraction(expected_min(s,t),93**s*10**(t-s))
        check(ratio==Fraction(x['exact_excess'])==Fraction(280,279)-Fraction(1,279*10**(b-1)) and ratio>1,
              'false finite-period gap')
    for x in rec['phase_separated_prefixes']:
        p=Fraction(x['target_B_frequency']);word=[];upper=1
        for j in range(1,x['stages']+1):
            a=((1-p)*j).__floor__();b=((2*p-1)*j).__floor__()
            word.extend((1,0)*a);word.extend((1,)*b)
            upper*=93**a*((4*10**b-1)//3)
        s,t=word.count(0),word.count(1);F=independent_count(Ms,word)
        check((s,t,F,upper)==(x['A_count'],x['B_count'],x['image_count'],x['stage_product_upper']),
              'phase-source prefix mismatch')
        check(expected_min(s,t)<=F<=upper,'phase-source enclosure')
    zero=rec['retained_zero_position']
    old=bits_image(zero['retained_generators'],5).bit_count()
    new=bits_image(zero['contracted_generators'],5).bit_count()
    check((old,new)==(289,177)==(zero['retained_fifth_count'],zero['contracted_fifth_count']), 'active zero-position map')
    check(old-new==zero['additional_kernel_dimension']==112,'lost active-position kernel')
    # Exact all-length crossing certificate: separate order-two recurrences.
    U=(17,18,19,19,20,20,20);V=(0,2,0,3,0,0,0)
    check(matmul(Ms[0],Ms[1])==[[x*y for y in V] for x in U],'rank-one factor mismatch')
    Au=matvec(Ms[0],U);A2u=matvec(Ms[0],Au)
    check(all(a2-11*a+10*u==0 for a2,a,u in zip(A2u,Au,U)),'first recurrence')
    transB=tuple(zip(*Ms[1]));Bv=matvec(transB,V);B2v=matvec(transB,Bv)
    check(all(b2-11*b+10*v==0 for b2,b,v in zip(B2v,Bv,V)),'second recurrence')
    for a,b in product((1,2),repeat=2):
        u=U;v=V
        for _ in range(a-1):u=matvec(Ms[0],u)
        for _ in range(b-1):v=matvec(transB,v)
        check(sum(x*y for x,y in zip(u,v))==(8*10**(a+b)+4*10**b-3)//9,'crossing initial value')
    return Ms,{'composition_classes':cases,'literal_words_through18':2**19-2,
               'maximum_column_states':max_states,'direct_original_images':direct,'attainer_grid_cases':961}


def unpack(expr):return {int(b):Fraction(c) for b,c in expr}
def plus(*exprs):
    out={}
    for E in exprs:
        for b,c in E.items():out[b]=out.get(b,Fraction(0))+c
    return {b:c for b,c in out.items() if c and b!=1}
def times(c,E):return {b:Fraction(c)*x for b,x in E.items()}
def log_sign(E):
    E={b:Fraction(c) for b,c in E.items() if c and b!=1};den=1
    for c in E.values():den=den*c.denominator//gcd(den,c.denominator)
    a=b=1
    for x,c in E.items():
        e=int(c*den)
        if e>0:a*=x**e
        else:b*=x**(-e)
    return (a>b)-(a<b)


def verify_lp(cert,points):
    m=cert['horizon'];D=cert['dictionary'];d=len(D)
    p=tuple(Fraction(x) for x in cert['profile']);lam=tuple(Fraction(x) for x in cert['mixture'])
    basis=[tuple(x) for x in cert['basis']]
    check(len(p)==d and len(lam)==d and len(basis)==d and min(lam)>=0 and sum(lam)==1,'invalid LP probability')
    check(all(sum(lam[j]*basis[j][i] for j in range(d))==m*p[i] for i in range(d)), 'LP frequency mismatch')
    actual={tuple(x['counts']):(x['image_count'],tuple(x['word'])) for x in cert['points']}
    check(actual==points,'LP primal domain incomplete or counts wrong')
    dual=[unpack(x) for x in cert['dual_prices']]
    for c,(F,w) in points.items():
        lhs=plus(*(times(c[i],dual[i]) for i in range(d)))
        check(log_sign(plus(lhs,{F:Fraction(-1)}))<=0,'LP dual inequality failed')
    primal=plus(*({points[c][0]:lam[j]/m} for j,c in enumerate(basis)))
    dualvalue=plus(*(times(p[i],dual[i]) for i in range(d)))
    upper=unpack(cert['upper_log_per_level']);lower=unpack(cert['lower_log_per_level'])
    check(log_sign(plus(primal,times(-1,dualvalue)))==0,'primal/dual gap')
    check(log_sign(plus(upper,times(-1,primal)))==0,'wrong LP upper value')
    check(log_sign(plus(lower,times(-1,upper),{cert['q']-1:Fraction(1,m)}))==0,'lost cut-factor correction')
    check(Fraction(cert['mean_reward'])==sum(p[i]*len(D[i]['weights']) for i in range(d)), 'reward changed')


def audit_lps(records,Ms):
    cache={};direct=0;inequalities=0
    for cert in records:
        dictionary=tuple((x['radix'],tuple(x['weights'])) for x in cert['dictionary'])
        q,m=cert['q'],cert['horizon'];key=(dictionary,q,m)
        if key not in cache:
            points={}
            for w in product(range(len(dictionary)),repeat=m):
                if dictionary==AB and q==5:
                    F=independent_count(Ms,w)
                else:
                    F=bits_image(original_generators(dictionary,w),q).bit_count();direct+=1
                c=tuple(w.count(i) for i in range(len(dictionary)))
                if c not in points or (F,w)<points[c]:points[c]=(F,w)
            cache[key]=points
        verify_lp(cert,cache[key]);inequalities+=len(cache[key])
    return cache,{'LP_certificates':len(records),'LP_dual_inequalities':inequalities,
                  'additional_direct_original_images':direct}


def corruptions(report,Ms,cache):
    failures=[]
    def rejected(name,fn):
        try:fn()
        except (AssertionError,KeyError,ValueError,IndexError):failures.append(name)
        else:raise AssertionError('corruption went undetected: '+name)
    x=deepcopy(report['residue_profiles']['exceptional_canonical_domains'][0]);x['six_AP']['subset_masks'][0]^=1
    rejected('changed original subset mask',lambda:verify_control(x))
    x=deepcopy(report['residue_profiles']['exceptional_canonical_domains'][0]);x['six_AP']['step']=0
    rejected('constant modular witness',lambda:verify_control(x))
    x=deepcopy(report['residue_profiles']);x['exceptional_canonical_domains'].pop()
    rejected('missing exceptional block',lambda:audit_residues(x))
    x=deepcopy(report['composition_spectrum']);x['matrices'][0][0][0]+=1
    rejected('incorrect arithmetic count matrix',lambda:audit_composition(x))
    x=deepcopy(report['composition_spectrum']);x['all_compositions_through_length18'][2]['compositions'][1]['minimum']+=1
    rejected('incorrect fixed-composition minimum',lambda:audit_composition(x))
    for name,change in [('negative primal coefficient',lambda c:c['mixture'].__setitem__(0,'-1')),
                        ('invalid dual price',lambda c:c['dual_prices'].__setitem__(0,[[10,'1000']])),
                        ('missing LP count class',lambda c:c['points'].pop())]:
        c=deepcopy(report['finite_composition_LPs'][0]);change(c)
        dictionary=tuple((v['radix'],tuple(v['weights'])) for v in c['dictionary'])
        rejected(name,lambda c=c,dictionary=dictionary:verify_lp(c,cache[(dictionary,c['q'],c['horizon'])]))
    return failures


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--proof',type=Path,default=HERE/'proof_data.json')
    parser.add_argument('--output',type=Path,default=HERE/'independent_audit.json')
    args=parser.parse_args();r=json.loads(args.proof.read_text())
    check(r['status']=='PASS' and r['lean_checked'] is False,'incorrect evidence boundary')
    residues=audit_residues(r['residue_profiles'])
    Ms,composition=audit_composition(r['composition_spectrum'])
    cache,lps=audit_lps(r['finite_composition_LPs'],Ms)
    bad=corruptions(r,Ms,cache)
    out={'schema':'ep817-residue-composition-independent-audit-v1','status':'PASS','lean_checked':False,
         'base_commit':r['base_commit'],'proof_sha256':sha256(args.proof.read_bytes()).hexdigest(),
         'auditor_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
         'residue_checks':residues,'composition_checks':composition,'LP_checks':lps,
         'rejected_corruptions':bad,
         'scope':'Separate arithmetic implementation; no imported producer/helper; bounded checks accompany written proofs.'}
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,sort_keys=True))

if __name__=='__main__':main()
