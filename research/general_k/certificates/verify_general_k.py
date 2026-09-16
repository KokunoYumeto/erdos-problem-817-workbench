#!/usr/bin/env python3
"""Reproduce exact, bounded checks for the general-k EP817 contribution.

All universal results are proved in the companion note. This checker verifies
finite inputs, witness maps, full/canonical graph closure, and regressions.
No external packages, floating point comparisons, or disabled assertions.
Run: python certificates/verify_general_k.py --output certificates/general_k_receipt.json
"""
from __future__ import annotations
import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
from carry_tools import (require, subset_sums, bit_sums, int_ap_bits,
                         modular_witness, carry_certificate, full_carry_certificate,
                         verify_closed_certificate, verify_full_closed, power_alias)

BASE = '23c0110c95b5a2036bdc04a1f352b6e5e27742c8'
ASTAR = (1,4,5,17,21,22)
PRIMARY = [(4,19,(1,7,8)),(5,23,(1,3,4,7)),
           (6,47,(1,2,6,7,14)),(5,97,ASTAR),(6,93,ASTAR)]


def direct_sums(a: tuple[int,...], alphabet: int=2) -> Counter[int]:
    return Counter(sum(c*x for c,x in zip(row,a))
                   for row in product(range(alphabet),repeat=len(a)))


def values_to_bits(values: set[int]) -> int:
    return sum(1 << x for x in values)


def progression_tuples(values: set[int], k: int) -> set[tuple[int,...]]:
    return {tuple(x+i*(y-x) for i in range(k)) for x in values for y in values
            if all(x+i*(y-x) in values for i in range(k))}


def direct_modular(d: set[int], b: int, k: int) -> tuple[list, int]:
    bad=[]
    for x in range(b):
        for step in range(1,b):
            row=tuple((x+i*step)%b for i in range(k))
            if set(row)<=d: bad.append((x,step,row))
    return bad,b*(b-1)


def language(d: set[int], b: int, m: int) -> set[int]:
    out={0}
    for j in range(m): out={x+y*b**j for x in out for y in d}
    return out


def validate_negative(d: set[int], b: int, k: int, c: dict) -> None:
    require(c['safe'] is False,'negative certificate expected')
    cols=c['columns'];m=len(cols)
    require(m==c['length'] and m>0,'invalid witness length')
    require(all(len(col)==k and set(col)<=d for col in cols),'invalid digit column')
    ys=[sum(col[i]*b**j for j,col in enumerate(cols)) for i in range(k)]
    require(ys==c['witness'],'witness decoding mismatch')
    require(ys[1]!=ys[0] and all(ys[i]==ys[0]+i*(ys[1]-ys[0]) for i in range(k)),
            'witness does not form a nonconstant AP')


def primary_checks() -> list[dict]:
    out=[]
    for k,b,a in PRIMARY:
        d=subset_sums(a)
        require(d==set(direct_sums(a)), 'binary subset map mismatch')
        require(sum(a)<b and power_alias(a,b) is None,'invalid canonical generator input')
        bad,parameters=direct_modular(d,b,k)
        require(not bad,'primary modular witness found')
        require(modular_witness(d,b,k) is None,'modular routines disagree')
        cert=carry_certificate(d,b,k)
        require(cert['safe'] and cert['states_seen']==1 and cert['edges_examined']==len(d),
                'incorrect singleton closed-state certificate')
        run_max=[]
        for step in range(1,b):
            longest=0
            for x in range(b):
                length=0
                while length<=b and (x+length*step)%b in d:length+=1
                require(length<=b,'entire residue cycle lies in digit set')
                longest=max(longest,length)
            require(longest<k,'long progression in run certificate')
            run_max.append(longest)
        lift=tuple(sorted(b**j*x for j in range(2) for x in a))
        require(len(lift)==len(set(lift))==2*len(a),'generator cardinality loss')
        hh=subset_sums(lift)
        require(hh==language(d,b,2) and len(hh)==len(d)**2,'lifted value bijection failed')
        require(int_ap_bits(values_to_bits(hh),k) is None,'two-level progression')
        # Compare complete representation multiplicities, including intentional collisions.
        mu=direct_sums(a);lift_mu=direct_sums(lift)
        expected=Counter({x+b*y:cx*cy for x,cx in mu.items() for y,cy in mu.items()})
        require(lift_mu==expected,'lifted fiber product mismatch')
        for n in range(1,2*len(a)+1):
            q,r=divmod(n,len(a))
            retained=tuple(b**j*x for j in range(q) for x in a)+tuple(b**q*x for x in a[:r])
            bound=a[r-1]*b**q if r else a[-1]*b**(q-1)
            require(len(set(retained))==n and max(retained)==bound,'residue-sensitive retention failed')
            h=subset_sums(retained)
            require(h<=hh and int_ap_bits(values_to_bits(h),k) is None,'deletion heredity failed')
        out.append({'k':k,'base':b,'generators':list(a),'generator_sum':sum(a),
                    'distinct_digit_count':len(d),'digits':sorted(d),
                    'modular_start_step_pairs':parameters,'max_runs_by_nonzero_step':run_max,
                    'canonical_certificate':cert,'two_level_generator_count':len(lift),
                    'two_level_subset_sum_count':len(hh),'deletions_tested':2*len(a)})
    require(97<5**3 and 93**5<7**12,'comparison with retrieved upper bounds failed')
    return out


def canonical_graph_checks() -> dict:
    cases=positive=negative=edges=finite=0;digest=sha256()
    for b in range(2,9):
        for mask in range(1<<(b-1)):
            d={0}|{i+1 for i in range(b-1) if mask>>i&1}
            for k in range(3,7):
                cert=carry_certificate(d,b,k);cases+=1
                if cert['safe']:
                    positive+=1;edges+=verify_closed_certificate(d,b,k,cert)
                else:
                    negative+=1;validate_negative(d,b,k,cert)
                    require(cert['length']<=3**(k-2),'canonical shortest witness bound failed')
                for m in range(1,4):
                    direct=int_ap_bits(values_to_bits(language(d,b,m)),k) is not None
                    expected=(not cert['safe'] and cert['length']<=m)
                    require(direct==expected,'bounded language check disagrees with graph')
                    finite+=1
                # The larger graph retains true differences rather than relying on unique words.
                if b<=6 and k<=5:
                    full=full_carry_certificate(d,b,k)
                    require(full['safe']==cert['safe'],'full and canonical graphs disagree')
                    if not full['safe']:validate_negative(d,b,k,full)
                digest.update((json.dumps({'b':b,'k':k,'D':sorted(d),'certificate':cert},sort_keys=True)+'\n').encode())
    return {'bases':[2,8],'k_range':[3,6],'digit_domain':'every subset of [0,b) containing zero',
            'cases':cases,'positive':positive,'negative':negative,'direct_closed_edges':edges,
            'direct_languages_checked':finite,'canonical_full_comparison_bases':[2,6],
            'canonical_full_comparison_k':[3,5],'transcript_sha256':digest.hexdigest()}


def full_graph_checks() -> dict:
    cases=safe=unsafe=edges=finite=0;digest=sha256()
    for b in range(2,5):
        for mask in range(1<<6):
            d={0}|{i+1 for i in range(6) if mask>>i&1}
            for k in (3,4):
                cert=full_carry_certificate(d,b,k);cases+=1
                if cert['safe']:
                    safe+=1;edges+=verify_full_closed(d,b,k,cert)
                else:
                    unsafe+=1;validate_negative(d,b,k,cert)
                    C,H=cert['carry_bound'],cert['slope_bound']
                    require(cert['length']<=2*(2*C+1)**(k-2)*(2*H+1)-1,'full witness bound failed')
                for m in range(1,4):
                    direct=int_ap_bits(values_to_bits(language(d,b,m)),k) is not None
                    require(direct==(not cert['safe'] and cert['length']<=m),'full graph/direct language mismatch')
                    finite+=1
                digest.update((json.dumps({'b':b,'k':k,'D':sorted(d),'certificate':cert},sort_keys=True)+'\n').encode())
    a=(7,8,19);b=19;k=4;d=subset_sums(a)
    cert=full_carry_certificate(d,b,k)
    require(power_alias(a,b) is None and cert['safe'],'noncanonical positive example failed')
    checked=verify_full_closed(d,b,k,cert)
    require(cert['states_seen']==15 and checked==288,'noncanonical closure record changed')
    for m in (1,2,3):
        lift=tuple(sorted(b**j*x for j in range(m) for x in a))
        enclosing={b**j*x for j in range(m+1) for x in (1,7,8)}
        require(len(set(lift))==3*m and set(lift)<=enclosing,'exact original-construction embedding failed')
        require(subset_sums(lift)==language(d,b,m),'noncanonical subset/language image mismatch')
        require(int_ap_bits(values_to_bits(subset_sums(lift)),4) is None,'noncanonical lifted AP')
    alias=(1,7,8,19)
    require(power_alias(alias,19)==(1,19,1),'power alias detection failed')
    counts=[]
    for m in (1,2,3,4):
        actual={19**j*x for j in range(m) for x in alias}
        require(len(actual)==3*m+1,'alias cardinality formula failed')
        counts.append(len(actual))
    return {'bases':[2,4],'k_range':[3,4],'digit_domain':'every subset of [0,6] containing zero',
            'cases':cases,'positive':safe,'negative':unsafe,'direct_closed_edges':edges,
            'direct_languages_checked':finite,'transcript_sha256':digest.hexdigest(),
            'noncanonical_positive':{'k':4,'base':19,'generators':list(a),'digits':sorted(d),
                                       'certificate':cert,'independent_closed_edges':checked},
            'power_alias_regression':{'generators':list(alias),'base':19,'actual_counts_m1_to_m4':counts}}


def composition_checks() -> dict:
    sets=[tuple(a) for size in range(3) for a in combinations(range(1,6),size)]
    pairs=aps=triples=0
    def star(a,b):return tuple(sorted(set(a)|{(2*sum(a)+1)*x for x in b}))
    for a,b in product(sets,repeat=2):
        R=2*sum(a)+1;c=star(a,b);pairs+=1
        require(len(c)==len(a)+len(b),'star cardinality failed')
        require(2*sum(c)+1==(2*sum(a)+1)*(2*sum(b)+1),'multiplicative observable failed')
        ma,mb,mc=direct_sums(a),direct_sums(b),direct_sums(c)
        expected=Counter({x+R*y:cx*cy for x,cx in ma.items() for y,cy in mb.items()})
        require(expected==mc,'star binary multiplicities failed')
        for z in mc:
            y,x=divmod(z,R)
            require(x in ma and y in mb and mc[z]==ma[x]*mb[y],'division inverse failed')
        ta,tb,tc=map(lambda x:set(direct_sums(x,3)),(a,b,c))
        require(tc=={x+R*y for x in ta for y in tb} and len(tc)==len(ta)*len(tb),'ternary product failed')
        for k in range(3,7):
            pa,pb,pc=progression_tuples(set(ma),k),progression_tuples(set(mb),k),progression_tuples(set(mc),k)
            image={tuple(x+R*y for x,y in zip(u,v)) for u in pa for v in pb}
            require(image==pc and len(pc)==len(pa)*len(pb),'AP tuple equivalence failed')
            for row in pc:
                left=tuple(x%R for x in row);right=tuple(x//R for x in row)
                require(left in pa and right in pb,'AP inverse failed')
                require((row[0]!=row[1])==((left[0]!=left[1]) or (right[0]!=right[1])),
                        'nonconstant witness factorization failed')
            aps+=1
    for a,b,c in product(sets,repeat=3):
        require(star(star(a,b),c)==star(a,star(b,c)),'associativity failed');triples+=1
    return {'input_domain':'empty, singleton, and two-element subsets of [1,5]',
            'input_sets':len(sets),'pairs':pairs,'AP_comparisons_k3_to_k6':aps,'associativity_triples':triples}


def structural_checks() -> dict:
    columns=((1,0,0),(0,1,0),(1,1,0),(0,0,1),(0,1,1),(1,1,1))
    C={tuple(sum(e*v[i] for e,v in zip(row,columns)) for i in range(3)) for row in product((0,1),repeat=6)}
    L=lambda x:x[0]+4*x[1]+17*x[2]
    require(tuple(map(L,columns))==ASTAR and len(C)==len(set(map(L,C)))==38,'correlated cube projection failed')
    for x in C:
        for y in C:
            if x==y:continue
            require(any(tuple(x[i]+j*(y[i]-x[i]) for i in range(3)) not in C for j in range(2,5)),
                    'vector 5-AP found')
    CC={tuple(x[i]+y[i] for i in range(3)) for x in C for y in C}
    fibers=Counter(map(L,CC));T=set(direct_sums(ASTAR,3))
    require(len(CC)==201 and len(fibers)==139 and set(fibers)==T,'second-order fiber cardinality failed')
    paths=[]
    for r in range(2,6):
        vertices=tuple(5**i for i in range(r));es=tuple(vertices[i]+vertices[i+1] for i in range(r-1))
        a=vertices+es;h=subset_sums(a)
        require(len(set(a))==2*r-1 and all(x>0 for x in a),'path generator conditions failed')
        require(int_ap_bits(values_to_bits(h),5) is None,'path family 5-AP')
        qs=[]
        for i in range(r-1):
            q=[0]*(2*r-1);q[i]=q[i+1]=1;q[r+i]=-1;qs.append(tuple(q))
            require(sum(c*x for c,x in zip(q,a))==0,'path relation failed')
            support=[j for j,x in enumerate(q) if x]
            for coeff in product((-1,0,1),repeat=3):
                if not any(coeff) or all(coeff):continue
                require(sum(c*a[j] for c,j in zip(coeff,support))!=0,'path relation not minimal')
        for i in range(r-2):
            support1={j for j,x in enumerate(qs[i]) if x};support2={j for j,x in enumerate(qs[i+1]) if x}
            require(support1&support2=={i+1},'path overlap incorrect')
            vi,vj,vk=vertices[i:i+3]
            row=(vi+vk,vi+vj+vk,es[i]+es[i+1],es[i]+es[i+1]+vj)
            require(set(row)<=h and all(row[j]==row[0]+j*vj for j in range(4)),'explicit 4-AP witness failed')
        paths.append({'r':r,'generators':list(a),'subset_sum_count':len(h),'minimal_relations':qs})
    return {'correlated_cube':{'columns':columns,'image_count':len(C),'second_image_count':len(CC),
                               'projected_second_image_count':len(T),
                               'second_image_fiber_sizes':{str(x):fibers[x] for x in sorted(fibers)}},
            'path_family':paths}


def regressions() -> dict:
    positive=[]
    for b,d,k in ((4,{0,2},3),(8,{0,1,3,4},5)):
        c=carry_certificate(d,b,k)
        require(c['safe'] and modular_witness(d,b,k) is not None,'modular/carry bridge regression failed')
        verify_closed_certificate(d,b,k,c)
        positive.append({'base':b,'digits':sorted(d),'k':k,'certificate':c})
    negative=[]
    for b,a,k in ((16,(1,3,4,7),5),(18,(1,7,8),4),(60,ASTAR,5),(93,ASTAR,5),(97,ASTAR,4)):
        d=subset_sums(a);c=full_carry_certificate(d,b,k)
        validate_negative(d,b,k,c)
        negative.append({'base':b,'generators':list(a),'k':k,'certificate':c})
    bad=deepcopy(positive[0]['certificate']);bad['closed_states']=bad['closed_states'][:1]
    actions=[lambda:carry_certificate({0},1,3),lambda:carry_certificate({0},3,2),
             lambda:carry_certificate(set(),3,3),lambda:carry_certificate({-1,0},3,3),
             lambda:carry_certificate({0,3},3,3),lambda:full_carry_certificate({-1,0},3,3),
             lambda:power_alias((0,1),3),lambda:power_alias((1,1),3),
             lambda:verify_closed_certificate({0,2},4,3,bad)]
    rejected=0
    for action in actions:
        try:action()
        except (AssertionError,ValueError):rejected+=1
        else:raise AssertionError('invalid input or mutation accepted')
    return {'positive_bridges':positive,'explicit_negative_witnesses':negative,
            'invalid_inputs_and_mutations_rejected':rejected}


def search_records(root: Path) -> dict:
    names=('search_carry_5_6_80.json','search_carry_5_6_160.json','search_modular_7_12_80.json')
    records=[];hashes={};summary={}
    for name in names:
        p=root/'logs'/name
        require(p.exists(), f'missing search record: {name}')
        raw=p.read_bytes();hashes[name]=sha256(raw).hexdigest();records+=json.loads(raw)
    expected_pairs={(k,b) for k in (5,6) for b in range(3,161)} | {(k,b) for k in range(7,13) for b in range(3,81)}
    require(len(records)==784 and {(r['k'],r['base']) for r in records}==expected_pairs, 'search domain mismatch')
    for r in records:
        k,b,a=r['k'],r['base'],tuple(r['generators'])
        if not a:continue
        require(sum(a)<b and len(set(a))==len(a) and min(a)>0,'invalid stored search witness')
        require(carry_certificate(subset_sums(a),b,k)['safe'],'stored search witness rejected')
        key=str(k)
        if key not in summary or b**len(summary[key]['generators']) < summary[key]['base']**len(a):
            summary[key]={'base':b,'generators':list(a)}
    return {'records_rechecked':len(records),'best_recorded_certificates':summary,
            'source_sha256':hashes,
            'scope':'Stored witnesses replayed. Search maximality additionally depends on search_carry.py and its complete bounded runs.'}


def noncanonical_probe_checks(root: Path) -> dict:
    p=root/'logs'/'noncanonical_fixed_block.json'
    require(p.exists(), 'missing noncanonical probe record')
    raw=p.read_bytes();records=json.loads(raw);d=subset_sums(ASTAR)
    require(len(records)==96 and {(r['k'],r['base']) for r in records}==
            {(k,b) for k in (5,6) for b in range(23,71)}, 'noncanonical probe domain mismatch')
    for r in records:
        b,k=r['base'],r['k'];ys=r['witness']
        require(r['safe'] is False and r['length']==2 and len(ys)==k, 'invalid probe classification')
        require(set(ys)<=language(d,b,2) and ys[0]!=ys[1] and
                all(ys[i]==ys[0]+i*(ys[1]-ys[0]) for i in range(k)), 'invalid probe progression')
        require(full_carry_certificate(d,b,k)['safe'] is False, 'probe replay mismatch')
    return {'cases':len(records),'bases':[23,70],'k':[5,6],'generators':list(ASTAR),
            'all_witness_lengths':2,'source_sha256':sha256(raw).hexdigest()}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path)
    args=parser.parse_args();root=Path(__file__).resolve().parents[1]
    report={'schema':'ep817-general-k-carry-capacity-v1','status':'PASS','base_commit':BASE,
            'proof_status':'Ordinary mathematical proofs in the companion note; bounded exact checks here.',
            'lean_checked':False,'primary':primary_checks(),'canonical_graph':canonical_graph_checks(),
            'full_graph':full_graph_checks(),'composition':composition_checks(),
            'structural':structural_checks(),'regressions':regressions(),'search_records':search_records(root),
            'noncanonical_probe':noncanonical_probe_checks(root)}
    report['source_sha256']={p.name:sha256(p.read_bytes()).hexdigest() for p in
                            (Path(__file__).resolve(),Path(__file__).resolve().with_name('carry_tools.py'))}
    rendered=json.dumps(report,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(rendered,encoding='utf-8')
    print(rendered,end='')

if __name__=='__main__':main()
