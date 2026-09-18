#!/usr/bin/env python3
"""Produce the exact finite certificates used in the companion proofs.

Run from any directory. General proofs remain in the notes; bounded checks do
not replace them. Explicit checks remain active under python -O.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from math import log, floor
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parent/'tools'))
import arithmetic as ar

BASE = 'dbd0a93f2cf935103e88e5c2b2b71fe85ae7537b'


def bit_image(A,q):
    bits=1
    for a in A:
        old=bits;bits=0
        for j in range(q):bits |= old << (j*a)
    return bits


def residue_records():
    controls=[]; per_rank={}
    for n,bound in ((2,4),(3,12),(4,22)):
        number=0
        for b in range(2,bound+1):
            for A in combinations(range(1,b),n):
                if sum(A)>=b:continue
                w=ar.modular_witness(A,b,6)
                ar.require(w is not None,'finite Kneser reduction has an admissible exception')
                controls.append({'rank':n,'radix':b,'weights':list(A),'six_AP':w})
                number+=1
        per_rank[str(n)]=number
    ar.require(per_rank=={'2':1,'3':41,'4':448},'exceptional-domain count changed')
    kneser=[]
    for d,V in ((4,4),(7,12),(12,22)):
        pairs=[[h,z] for h in range(2,V+1) for z in range(h,V+1,h)
               if z>=d and 2*z-h<=V]
        kneser.append({'binary_count_lower':d,'ternary_count_upper':V,'all_stabilizer_pairs':pairs})
    anchors=((3,(1,)),(5,(1,2)),(13,(1,3,4)),(23,(1,3,4,7)))
    sharp=[]
    for n,(b,A) in enumerate(anchors,1):
        D=ar.image(A,3)
        ar.require(len({x%b for x in D})==b,'sharp residue count')
        ar.require(ar.modular_witness(A,b,5) is None,'sharp anchor has a modular five-AP')
        representatives=[]
        words=[(sum(a*c for a,c in zip(A,ds)),ds) for ds in product(range(3),repeat=n)]
        mu=Counter(x for x,ds in words)
        weighted=[]
        for r in range(b):
            x,digits=min((x,ds) for x,ds in words if x%b==r)
            representatives.append({'residue':r,'actual_value':x,'ternary_digits':list(digits)})
            fiber={z:c for z,c in mu.items() if z%b==r};mass=sum(fiber.values())
            energy=sum(Fraction(c,mass)**2/c for c in fiber.values())
            boundary=sum((Fraction(int(z==x))-Fraction(c,mass))**2/c for z,c in fiber.items())
            ar.require(energy==Fraction(1,mass) and energy+boundary==Fraction(1,mu[x]),'weighted residue Pythagoras')
            weighted.append({'residue':r,'values_and_word_masses':[[z,c] for z,c in sorted(fiber.items())],
                             'total_word_mass':mass,'section_energy':str(energy),'integral_section_boundary_energy':str(boundary)})
        scaled=[]
        for g in (2,7,19,101):
            C=tuple(g*a for a in A);q=g*b
            ar.require(ar.modular_witness(C,q,5) is None,'scaled anchor lost modular freeness')
            ar.require(len({x%q for x in ar.image(C,3)})==b,'subgroup inverse lost a residue')
            scaled.append({'scale':g,'radix':q,'weights':list(C)})
        sharp.append({'rank':n,'radix':b,'weights':list(A),'ternary_representatives':representatives,'weighted_fibers':weighted,'scaled_cases':scaled})
    scan=Counter(); digest=sha256()
    targets={1:3,2:5,3:13,4:23}
    for b in range(2,41):
        for n in range(1,5):
            for A in combinations(range(1,b),n):
                if sum(A)>=b:continue
                scan['candidate_blocks']+=1
                D=ar.image(A,2);V={x%b for x in ar.image(A,3)}
                for k in (5,6):
                    if ar.modular_witness(A,b,k) is None:
                        scan[f'safe_k{k}_rank{n}']+=1
                        ar.require(len(V)>=targets[n],'rank-residue bound failed in scan')
                        if n==4:ar.require(len(D)>=12,'binary rank-four lower bound')
                        digest.update((repr((b,A,k,len(D),len(V)))+'\n').encode())
    equality=[]
    for A in combinations(range(1,25),4):
        if len(ar.image(A,2))==11:
            ar.require(A==tuple(A[0]*i for i in (1,2,3,4)),'rank-four equality classification')
            equality.append(list(A))
    joins=[]
    for length in (1,2,3):
        for word in product(range(4),repeat=length):
            A,P=ar.generators(anchors,word)
            n3=bit_image(A,3).bit_count();n5=bit_image(A,5).bit_count()
            bound=1
            for i in word:bound*=anchors[i][0]
            ar.require(bound<=n3<=n5,'uniform mixed-rank injection failed')
            joins.append({'word':list(word),'reward':len(A),'ternary':n3,'fifth':n5,'lower_product':bound})
    tail=[]
    c=ar.scale(Fraction(1,4),ar.logint(23))
    for k,b,n in ((5,97,6),(6,1651,10)):
        u=ar.scale(Fraction(1,n),ar.logint(b))
        g=ar.add(ar.logint(k-1),ar.scale(-1,ar.logint(k-2)))
        approximate=(log(23)/4-log(b)/n)/(log(23)/4-log((k-1)/(k-2)))
        lo=Fraction(floor(10000*approximate),10000);hi=lo+Fraction(1,10000)
        # beta >= t iff (1-t)c + t log(gamma) >= log u.
        ar.require(ar.compare(ar.add(ar.scale(1-lo,c),ar.scale(lo,g)),u)>0,'tail lower enclosure')
        ar.require(ar.compare(ar.add(ar.scale(1-hi,c),ar.scale(hi,g)),u)<0,'tail upper enclosure')
        tail.append({'k':k,'comparison_rate_base':b,'comparison_rate_root':n,
                     'required_large_rank_fraction_interval':[str(lo),str(hi)]})
    return {'exceptional_canonical_domains':controls,'exceptional_counts':per_rank,
            'stabilizer_reductions':kneser,'sharp_anchors':sharp,
            'additional_scan':{'max_radix':40,**dict(scan),'transcript_sha256':digest.hexdigest()},
            'rank_four_equality_cases_through_max24':equality,
            'mixed_rank_joins':joins,'rank_tail_bounds':tail}


def composition_records():
    Ms=[ar.matrix(A,b,5) for b,A in ar.AB];terminal=tuple(len(r) for r in ar.shapes(5))
    u=(17,18,19,19,20,20,20);v=(0,2,0,3,0,0,0)
    ar.require(ar.mm(Ms[0],Ms[1])==tuple(tuple(x*y for y in v) for x in u),'original rank-one product')
    states={((1,0,0,0,0,0,0),0):((),1)}
    records=[];digest=sha256()
    for m in range(1,19):
        nxt={}
        for (row,s),(word,mass) in states.items():
            for i,M in enumerate(Ms):
                key=(ar.rm(row,M),s+(i==0));w=word+(i,)
                if key in nxt:
                    old,num=nxt[key];nxt[key]=(min(old,w),num+mass)
                else:nxt[key]=(w,mass)
        states=nxt
        ar.require(sum(x[1] for x in states.values())==2**m,'literal AB word mass')
        mins={}
        for (row,s),(word,mass) in states.items():
            F=sum(x*y for x,y in zip(row,terminal))
            if s not in mins or (F,word)<mins[s]:mins[s]=(F,word)
        per=[]
        for s,(F,w) in sorted(mins.items()):
            t=m-s
            ar.require(F==ar.minimum(s,t),'fixed-composition minimum disagreement')
            per.append({'A_count':s,'B_count':t,'minimum':F,'first_minimizer':list(w)})
        rec={'length':m,'literal_words':2**m,'row_count_states':len(states),'compositions':per}
        records.append(rec);digest.update((json.dumps(rec,sort_keys=True)+'\n').encode())
    def fast_count(w):
        row=(1,0,0,0,0,0,0)
        for i in w:row=ar.rm(row,Ms[i])
        return sum(x*y for x,y in zip(row,terminal))
    attain=0
    for s in range(31):
        for t in range(31):
            w=ar.attainer(s,t)
            ar.require(w.count(0)==s and w.count(1)==t,'attainer composition')
            ar.require(fast_count(w)==ar.minimum(s,t),'large attainer identity')
            attain+=1
    for a in range(1,41):
        K=[ar.crossing(a+i,1) for i in range(3)]
        J=[ar.crossing(1,a+i) for i in range(3)]
        ar.require(K[0]*K[2]-K[1]**2==2960*10**a,'strict balancing identity')
        ar.require(J[0]*J[2]-J[1]**2==-252*10**a,'strict clustering identity')
    strict=[]
    for s in range(1,16):
        for t in range(s+1,31):
            b=t-s+1
            ratio=Fraction(ar.minimum(s,t),93**s*10**(t-s))
            expected=Fraction(280,279)-Fraction(1,279*10**(b-1))
            ar.require(ratio==expected and ratio>1,'finite-period gap')
            if (s,t) in ((1,2),(1,3),(2,6),(5,15)):
                strict.append({'A_count':s,'B_count':t,'exact_excess':str(ratio)})
    phases=[]
    for p in (Fraction(3,5),Fraction(2,3),Fraction(3,4)):
        for stages in (10,20,40):
            w=ar.phase_word(p,stages);s=w.count(0);t=w.count(1)
            F=fast_count(w);upper=1
            for j in range(1,stages+1):
                a=((1-p)*j).__floor__();b=((2*p-1)*j).__floor__()
                upper*=93**a*((4*10**b-1)//3)
            ar.require(ar.minimum(s,t)<=F<=upper,'actual phase schedule bounds')
            phases.append({'target_B_frequency':str(p),'stages':stages,'A_count':s,'B_count':t,
                           'image_count':F,'stage_product_upper':upper,
                           'exact_target_log_per_level':ar.encode(ar.spectrum(p))})
    return {'matrices':[[list(r) for r in M] for M in Ms],
            'all_compositions_through_length18':records,'transcript_sha256':digest.hexdigest(),
            'explicit_attainer_grid':{'max_A':30,'max_B':30,'cases':attain},
            'balancing_identities_through40':True,'periodic_excess_examples':strict,
            'phase_separated_prefixes':phases,
            'retained_zero_position':{'retained_generators':[1,3,100,300],'contracted_generators':[1,3,10,30],
              'retained_fifth_count':bit_image((1,3,100,300),5).bit_count(),
              'contracted_fifth_count':bit_image((1,3,10,30),5).bit_count(),'additional_kernel_dimension':112}}


def lp_records():
    records=[]
    profiles=(Fraction(1,4),Fraction(1,3),Fraction(2,5),Fraction(1,2),Fraction(2,3),Fraction(3,4))
    for m in range(1,9):
        for p in profiles:
            cert=ar.composition_lp(ar.AB,5,m,(1-p,p))
            true=ar.spectrum(p)
            ar.require(ar.compare(ar.decode(cert['lower_log_per_level']),true)<=0,'LP lower missed exact spectrum')
            ar.require(ar.compare(true,ar.decode(cert['upper_log_per_level']))<=0,'LP upper missed exact spectrum')
            records.append(cert)
    dictionary=((3,(1,)),(5,(1,2)),(10,(2,4)))
    for q in (2,3,5):
        for m in range(1,5):
            for p in ((Fraction(1,2),Fraction(1,3),Fraction(1,6)),
                      (Fraction(1,3),)*3,(Fraction(1,2),Fraction(1,2),Fraction(0))):
                records.append(ar.composition_lp(dictionary,q,m,p))
    return records


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=HERE/'proof_data.json')
    args=parser.parse_args()
    report={'schema':'ep817-residue-composition-proof-v1','status':'PASS','lean_checked':False,
            'base_commit':BASE,
            'scope':'Written general proofs plus exactly specified finite input certificates and bounded replays.',
            'residue_profiles':residue_records(), 'composition_spectrum':composition_records(),
            'finite_composition_LPs':lp_records()}
    report['source_sha256']={str(p.relative_to(HERE.parent)):sha256(p.read_bytes()).hexdigest()
                             for p in (HERE.parent/'tools/arithmetic.py',Path(__file__).resolve())}
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','output':str(args.output),'sha256':sha256(args.output.read_bytes()).hexdigest(),
                      'finite_controls':len(report['residue_profiles']['exceptional_canonical_domains']),
                      'LP_certificates':len(report['finite_composition_LPs'])}))

if __name__=='__main__':main()
