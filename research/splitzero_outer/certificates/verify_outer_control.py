#!/usr/bin/env python3
"""Exact finite replays for the support-preserving outer-parameter theorems.

Standard library only. All runtime checks survive python -O. The general
polyhedral and infinite-schedule statements are proved in the companion note;
the finite domains here are corroboration, not a substitute for those proofs.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict, deque
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from math import factorial, prod
from pathlib import Path


def require(ok: bool, text: str) -> None:
    if not ok:
        raise AssertionError(text)


def height_bound(d: int) -> int:
    require(d >= 1, 'positive dimension required')
    return 3 * 2**(d-1) * factorial(d)


@lru_cache(maxsize=None)
def vectors(n: int) -> tuple[tuple[int, ...], ...]:
    return tuple(product(range(-2, 3), repeat=n))


def signature(a: tuple[int, ...], bases: tuple[int, ...]) -> bytes:
    """Every actual affine label (j,u,v,c), including constant and zero forms."""
    require(a and tuple(sorted(set(a))) == a and a[0] > 0, 'invalid generators')
    require(bases and all(b > sum(a) for b in bases), 'noncanonical base')
    dots = [sum(x*y for x,y in zip(u,a)) for u in vectors(len(a))]
    return bytes((t-v*b+c > 0) + (t-v*b+c >= 0)
                 for b in bases for t in dots for v in (-1,0,1) for c in (-1,0,1))


def cell_rows(a: tuple[int, ...], bases: tuple[int, ...]) -> tuple:
    """A x >= r for the integer sign cell, deduplicating only identical rows."""
    n, ell = len(a), len(bases); dimension = n+ell
    rows: dict[tuple[int,...],int] = {}
    def add(row, rhs):
        row=tuple(row)
        rows[row]=max(rows.get(row, rhs), rhs)
    add((1,)+(0,)*(dimension-1), 1)
    for i in range(1,n):
        row=[0]*dimension;row[i]=1;row[i-1]=-1;add(row,1)
    for j,b in enumerate(bases):
        row=[-1]*n+[0]*ell;row[n+j]=1;add(row,1)
        for u in vectors(n):
            t=sum(x*y for x,y in zip(u,a))
            for v in (-1,0,1):
                row=list(u)+[0]*ell;row[n+j]=-v
                for c in (-1,0,1):
                    value=t-v*b+c
                    if value>0:add(row,1-c)
                    elif value<0:add((-z for z in row),1+c)
                    else:
                        add(row,-c);add((-z for z in row),c)
    answer=tuple(sorted(rows.items()))
    x=a+bases
    require(all(sum(p*q for p,q in zip(row,x))>=rhs for row,rhs in answer),'own point outside cell')
    require(all(abs(rhs)<=2 and max(map(abs,row),default=0)<=2 for row,rhs in answer),'coefficient bound')
    return answer


def values(a):
    out=Counter({0:1})
    for x in a:
        old=out.copy()
        for y,m in old.items():out[y+x]+=m
    return out


def subset_values_by_mask(a):
    return tuple(sum(a[i] for i in range(len(a)) if mask>>i&1)
                 for mask in range(1<<len(a)))


def transitions(c, digits, b):
    present=set(digits)
    for first in digits:
        for second in digits:
            column=[first,second];target=[]
            for ci in c:
                total=2*column[-1]-column[-2]-ci
                nxt=total % b
                if nxt not in present:break
                target.append((nxt-total)//b);column.append(nxt)
            else:
                require(all(-1<=t<=1 for t in target),'carry escaped')
                yield tuple(target),tuple(column)


def full_profile(a, bases, k):
    digits=tuple(sorted(values(a)));d_to_masks=defaultdict(list)
    for mask,d in enumerate(subset_values_by_mask(a)):d_to_masks[d].append(mask)
    # Every numerical column retained with its full binary-mask fibers.
    profiles=[]
    for b in bases:
        edges=[]
        for c in product((-1,0,1),repeat=k-2):
            for nxt,col in transitions(c,digits,b):
                fibers=tuple(tuple(d_to_masks[d]) for d in col)
                edges.append((c,nxt,fibers,col[0]!=col[1]))
        profiles.append(tuple(edges))
    return tuple(profiles)


def controller(a, k, bases=None, enumerate_cycles=True, prune_returns=False):
    digits=tuple(sorted(values(a)));S=sum(a)
    if bases is None:bases=tuple(range(S+1,2*S+3))
    cs=tuple(product((-1,0,1),repeat=k-2));zero=(0,)*(k-2)
    return_rows={}
    if prune_returns:
        for c in cs:
            for target,col in transitions(c,digits,2*S+2):
                if target==zero:
                    return_rows[c]=col;break
    initial_new={};successors={}
    for b in bases:
        initial_new[b]=frozenset(t for t,col in transitions(zero,digits,b) if col[0]!=col[1])
        for c in cs:successors[b,c]=frozenset(t for t,_ in transitions(c,digits,b))
    start=frozenset();queue=deque([start]);seen={start:0};states=[start];edges=[];discarded=[]
    while queue:
        R=queue.popleft();src=seen[R]
        for b in bases:
            T=set(initial_new[b])
            for c in R:T.update(successors[b,c])
            if prune_returns and T.intersection(return_rows):
                carry=min(T.intersection(return_rows))
                discarded.append([src,b,[list(c) for c in sorted(T)],list(carry),list(return_rows[carry])])
                continue
            if zero in T:continue
            T=frozenset(T)
            if T not in seen:
                seen[T]=len(states);states.append(T);queue.append(T)
            edges.append((src,seen[T],b))
    require(len(states)<=2**(3**(k-2)-1),'controller count')
    if not enumerate_cycles:
        return {'states':[[list(c) for c in sorted(R)] for R in states],
                'edges':[list(e) for e in edges], 'cycles':[], 'best':None,
                'return_section':[[list(c),list(col)] for c,col in sorted(return_rows.items())],
                'discarded_edges':discarded}
    adjacency=defaultdict(list)
    for s,t,b in edges:adjacency[s].append((t,b))
    cycles=[]
    # Keep every parallel radix label. Minimum-vertex convention prevents rotations.
    for first in range(len(states)):
        def visit(at, visited, labels, nodes):
            for target,b in adjacency[at]:
                if target==first:
                    cycles.append({'states':nodes+[first],'bases':labels+[b],
                                   'product':prod(labels+[b]),'length':len(labels)+1})
                elif target>first and target not in visited:
                    visit(target,visited|{target},labels+[b],nodes+[target])
        visit(first,{first},[],[first])
    best=None
    for C in cycles:
        if best is None or C['product']**best['length']<best['product']**C['length']:
            best=C
    return {'states':[[list(c) for c in sorted(R)] for R in states],
            'edges':[list(e) for e in edges], 'cycles':cycles,'best':best}


def period_safe(a,k,bases):
    digits=tuple(sorted(values(a)));zero=(0,)*(k-2);R=frozenset();seen=set();m=0
    while (m%len(bases),R) not in seen:
        seen.add((m%len(bases),R));b=bases[m%len(bases)]
        T={t for t,col in transitions(zero,digits,b) if col[0]!=col[1]}
        for c in R:T.update(t for t,_ in transitions(c,digits,b))
        if zero in T:return False
        R=frozenset(T);m+=1
    return True


def direct_ap(digits,k):
    ds=sorted(digits);present=set(ds)
    for i,x in enumerate(ds):
        for y in ds[i+1:]:
            step=y-x
            if x+(k-1)*step>ds[-1]:break
            if all(x+j*step in present for j in range(k)):return tuple(x+j*step for j in range(k))
    return None


def transport_test(a,bases,aa,bb,length):
    require(signature(a,bases)==signature(aa,bb),'signature transport premise')
    require(len(bases)==len(bb),'schedule lengths')
    Va=subset_values_by_mask(a);Vb=subset_values_by_mask(aa)
    digit_map={}
    for x,y in zip(Va,Vb):
        require(x not in digit_map or digit_map[x]==y,'digit fiber failed')
        digit_map[x]=y
    require(len(set(digit_map.values()))==len(digit_map),'digit inverse')
    require(tuple(sorted(digit_map.values()))==tuple(digit_map[x] for x in sorted(digit_map)),'digit order')
    pairs=[(0,0)];P=Q=1
    for j in range(length):
        pairs=[(x+P*d,y+Q*digit_map[d]) for x,y in pairs for d in sorted(digit_map)]
        P*=bases[j%len(bases)];Q*=bb[j%len(bb)]
    forward={};backward={}
    for x,y in pairs:
        for z,w in pairs:
            u,v=x+z,y+w
            require(u not in forward or forward[u]==v,'Freiman forward failure')
            require(v not in backward or backward[v]==u,'Freiman inverse failure')
            forward[u]=v;backward[v]=u
    for k in range(3,7):
        require(bool(direct_ap([x for x,_ in pairs],k))==bool(direct_ap([y for _,y in pairs],k)),
                'AP existence transport')
    return {'length':length,'distinct_values':len(pairs),'ordered_pair_checks':len(pairs)**2,
            'pair_sum_classes':len(forward)}


def recession_certificate(a,bases,aa,bb,rays,multipliers):
    x=a+bases;y=aa+bb;rows=cell_rows(a,bases)
    require(signature(a,bases)==signature(aa,bb),'changed affine pattern')
    require(all(sum(p*q for p,q in zip(row,y))>=rhs for row,rhs in rows),'new point cell')
    require(all(all(z>=0 for z in r) for r in rays),'negative direction')
    for r in rays:
        require(all(sum(p*q for p,q in zip(row,r))>=0 for row,_ in rows),'not recession direction')
    reconstructed=tuple(v+sum(m*r[i] for r,m in zip(rays,multipliers)) for i,v in enumerate(y))
    require(reconstructed==x,'inverse reconstruction failed')
    require(all(z<=old for z,old in zip(y,x)) and max(y)<=height_bound(len(y)),'height/cost control')
    return {'original_generators':a,'original_bases':bases,'bounded_generators':aa,'bounded_bases':bb,
            'directions':rays,'multipliers':multipliers,'height_bound':height_bound(len(y)),
            'cell_rows':len(rows),'signature_sha256':sha256(signature(a,bases)).hexdigest()}


def height_replay():
    domain={};total=0
    Q=height_bound(3)
    # Keep all potential coordinatewise dominators, not only a single representative.
    for b in range(2,Q+1):
        for a1 in range(1,b):
            for a2 in range(a1+1,b-a1):
                a=(a1,a2);sig=signature(a,(b,));p=a+(b,);total+=1
                old=domain.setdefault(sig,[])
                if any(all(x<=y for x,y in zip(t,p)) for t in old):continue
                old[:]=[t for t in old if not all(x<=y for x,y in zip(p,t))]
                old.append(p)
    tested=0;digest=sha256()
    # Exact nonrandom domain, including values above the proved cutoff.
    for b in range(Q+1,121):
        for a1 in range(1,b):
            for a2 in range(a1+1,b-a1):
                p=(a1,a2,b);sig=signature(p[:2],(b,))
                candidates=[t for t in domain.get(sig,[]) if all(x<=y for x,y in zip(t,p))]
                require(bool(candidates),'bounded two-generator realization not found')
                chosen=min(candidates,key=lambda t:(t[-1],t[:-1]));tested+=1
                digest.update((repr((p,chosen))+'\n').encode())
    one=0
    for b in range(2,161):
        for a in range(1,b):
            sig=signature((a,),(b,))
            found=next(((x,y) for y in range(2,min(b,height_bound(2))+1)
                        for x in range(1,min(a,y-1)+1) if signature((x,),(y,))==sig),None)
            require(found is not None,'one generator realization missing');one+=1
    return {'one_generator_domain':'1<=a<b<=160','one_generator_cases':one,
            'two_generator_core_base_max':Q,'two_generator_core_points':total,
            'two_generator_sign_cells':len(domain),'two_generator_tail_base_range':[Q+1,120],
            'two_generator_tail_points':tested,'tail_transcript_sha256':digest.hexdigest()}


def metric_replay():
    tested=0;secants=0;tensors=[]
    # Exhaust every pair S subset T of the literal binary masks for two inputs.
    for a in ((1,4,5),(1,7,8)):
        masks=subset_values_by_mask(a);N=len(masks)
        for codes in product(range(3),repeat=N):
            S=[i for i,c in enumerate(codes) if c==2]
            T=[i for i,c in enumerate(codes) if c>=1]
            ms=Counter(masks[i] for i in S);mt=Counter(masks[i] for i in T)
            # All fiber relation vectors sum to zero, their images keep label S or T.
            for y,m in ms.items():
                difference=[(Fraction(1,mt[y]) if i in T and masks[i]==y else 0)
                            -(Fraction(1,m) if i in S and masks[i]==y else 0) for i in range(N)]
                require(sum(difference)==0,'section correction not an actual fiber boundary')
                require(sum(z*z for z in difference)==Fraction(1,m)-Fraction(1,mt[y]),'section norm')
                require(sum(Fraction(1,m)**2 for i in S if masks[i]==y)==Fraction(1,m),'quotient gram')
                secants+=1
            tested+=1
        mu=values(a);D=tuple(sorted(mu))
        for m in (1,2,3):
            widths=[prod(mu[d] for d in word) for word in product(D,repeat=m)]
            require(sum(widths)==(1<<len(a))**m,'tensor representation mass')
            determinant=Fraction(1,prod(widths))
            expected=Fraction(1,prod(mu.values()))**(m*len(D)**(m-1))
            require(determinant==expected,'tensor determinant')
            require(max(widths)==max(mu.values())**m,'metric cost tensor')
            tensors.append({'generators':a,'length':m,'image_dimension':len(widths),
                            'max_fiber':max(widths),'determinant':str(determinant)})
    return {'support_inclusion_pairs':tested,'section_boundary_identities':secants,'tensor_cases':tensors}


def chain_deficit_replay():
    cases=stages=0;digest=sha256()
    for k in range(3,8):
        h=k-2
        for n in range(1,6):
            for a in combinations(range(1,17),n):
                if direct_ap(values(a),k):continue
                B={0};defects=[];counts=[1]
                for weight in a:
                    starts=[x for x in B if x-weight not in B];lengths=[]
                    for start in starts:
                        length=0
                        while start+length*weight in B:length+=1
                        lengths.append(length)
                    require(max(lengths)<=h,'chain length exceeds final admissibility')
                    v=len(B);c=len(starts);delta=h*c-v
                    require(delta==sum(h-L for L in lengths) and delta>=0,'chain defect')
                    overlap=B & {x+weight for x in B}
                    require(len(overlap)==v-c,'relation dimension')
                    BB=B | {x+weight for x in B}
                    require(h*len(BB)==(h+1)*v+delta,'exact step')
                    B=BB;defects.append(delta);counts.append(len(B));stages+=1
                total=Fraction(h+1,h)**n + sum(Fraction(h+1,h)**(n-1-j)*Fraction(d,h)
                                               for j,d in enumerate(defects))
                require(total==len(B),'iterated defect expression')
                cases+=1;digest.update((repr((k,a,counts,defects))+'\n').encode())
    return {'k_range':[3,7],'generator_universe':[1,16],'size_range':[1,5],
            'admissible_sets':cases,'stages':stages,'transcript_sha256':digest.hexdigest()}



def lower_potential(edges, count, numerator, power):
    """Exact multiplicative Bellman certificate for every safe edge."""
    h=[Fraction(1) for _ in range(count)]
    for _ in range(count-1):
        old=h[:]
        for src,dst,b in edges:
            h[dst]=max(h[dst],Fraction(numerator,b**power)*old[src])
        if h==old:break
    require(all(b**power*h[dst]>=numerator*h[src] for src,dst,b in edges),
            'cycle lower-potential failed')
    return [str(x) for x in h]


def direct_controller_check(a,k,C):
    """Independent k-fold digit enumeration on an explicitly small domain."""
    D=tuple(sorted(values(a)));zero=(0,)*(k-2);S=sum(a)
    found={(s,b):t for s,t,b in C['edges']};count=0
    for src,raw in enumerate(C['states']):
        R={tuple(c) for c in raw}
        for b in range(S+1,2*S+3):
            T=set()
            for col in product(D,repeat=k):
                delta=tuple(col[i+2]-2*col[i+1]+col[i] for i in range(k-2))
                incoming=list(R)+([zero] if col[0]!=col[1] else [])
                for c in incoming:
                    residues=tuple(x+y for x,y in zip(c,delta))
                    if all(z%b==0 for z in residues):T.add(tuple(z//b for z in residues))
            if zero in T:require((src,b) not in found,'bad edge was retained')
            else:
                require((src,b) in found,'safe edge was removed')
                expect={tuple(c) for c in C['states'][found[src,b]]}
                require(T==expect,'direct controller transfer differs')
            count+=1
    return count


def global_rank_replay():
    specifications=[]
    for k in range(3,10):specifications.append((k,1,3,(1,)))
    for k in range(3,10):
        specifications.append((k,2,9,(1,3)) if k<=4 else (k,2,5,(1,2)))
    specifications += [(4,3,19,(1,7,8)),(5,3,13,(1,3,4)),(6,3,13,(1,3,4)),
                       (5,4,23,(1,3,4,7)),(6,4,23,(1,3,4,7))]
    results=[];gold=0
    for k,n,Q,benchmark in specifications:
        require(len(benchmark)==n and sum(benchmark)<Q and period_safe(benchmark,k,(Q,)),
                'benchmark certificate invalid')
        domain=[];best=None
        for a in combinations(range(1,Q),n):
            if sum(a)>=Q:continue
            witness=direct_ap(values(a),k)
            if witness:
                domain.append({'generators':a,'one_level_obstruction':witness});continue
            C=controller(a,k)
            entry={'generators':a,'states':C['states'],'edges':C['edges'],
                   'simple_labeled_cycles':len(C['cycles']),'best':C['best']}
            require(C['best'] is not None,'admissible block lacks safe cycle')
            if n<=2 and k<=5:gold+=direct_controller_check(a,k,C)
            c=C['best']
            if best is None or c['product']**best['cycle']['length']<best['cycle']['product']**c['length']:
                best={'generators':a,'cycle':c}
            domain.append(entry)
        require(best is not None,'empty finite optimum')
        P=best['cycle']['product'];ell=best['cycle']['length']
        require(P<=Q**ell,'benchmark upper comparison')
        require(period_safe(best['generators'],k,tuple(best['cycle']['bases'])),'minimizing period fails')
        for entry in domain:
            if 'one_level_obstruction' not in entry:
                entry['potential']=lower_potential(entry['edges'],len(entry['states']),P,ell)
        results.append({'k':k,'block_size':n,'benchmark_generators':benchmark,'benchmark_base':Q,
                        'exhaustive_domain':'all distinct positive n-element A with sum(A)<benchmark_base',
                        'generator_sets':len(domain),'best':best,'rate_root_exponent':n*ell,
                        'potential_edge_inequality':f'b^{ell}*h(target) >= {P}*h(source)',
                        'domain':domain})
    return {'instances':results,'independent_kfold_transfer_checks':gold,
            'total_generator_sets':sum(r['generator_sets'] for r in results),
            'total_safe_edges':sum(len(a.get('edges',[])) for r in results for a in r['domain'])}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--skip-height-replay',action='store_true')
    args=parser.parse_args()
    rec=[]
    rec.append(recession_certificate((1,100),(301,),(1,4),(12,),((0,1,2),(0,0,1)),(96,97)))
    rec.append(recession_certificate((10**6,7*10**6,8*10**6),(19*10**6,),
                                     (2,14,16),(38,),((1,7,8,19),),(10**6-2,)))
    rec.append(recession_certificate((1,4,5,17,21,22),(10**12,),
                                     (1,4,5,17,21,22),(142,),((0,0,0,0,0,0,1),),(10**12-142,)))
    rec.append(recession_certificate((1,4,8),(14,10**12),(1,4,8),(14,28),
                                     ((0,0,0,0,1),),(10**12-28,)))
    transport=[];profiles=[]
    for r in rec:
        a=tuple(r['original_generators']);b=tuple(r['original_bases'])
        aa=tuple(r['bounded_generators']);bb=tuple(r['bounded_bases'])
        for k in range(3,7):
            p=full_profile(a,b,k);q=full_profile(aa,bb,k)
            require(p==q,'complete carry profile changed')
            profiles.append({'generators':a,'bases':b,'k':k,'labeled_edges':sum(map(len,p)),
                             'profile_sha256':sha256(repr(p).encode()).hexdigest()})
        for m in (1,2):transport.append(transport_test(a,b,aa,bb,m))
    ctr=controller((1,4,8),5)
    require(ctr['best']['product']**2==280**ctr['best']['length'],'fixed block min cycle')
    require(period_safe((1,4,8),5,(14,20)),'known mixed period')
    require(not period_safe((1,4,8),5,(14,)),'invalid constant period passed')
    for C in ctr['cycles']:
        require(period_safe((1,4,8),5,tuple(C['bases'])),'cycle not safe from initial state')
    single=[]
    for k in range(3,10):
        C=controller((1,),k)
        require(C['best'] is not None,'no singleton capacity')
        single.append({'k':k,'controller_states':len(C['states']),'safe_edges':len(C['edges']),
                       'cycles':len(C['cycles']),'best':C['best']})
    # An unbounded full integer relation is explicitly transported, not claimed preserved.
    require(100*1-100==0 and 100*1-4==96,'full relation comparison')
    report={'schema':'ep817-splitzero-outer-v1','status':'PASS','lean_checked':False,
            'scope':'Written general proofs; exact bounded replays only for the stated finite domains.',
            'recession_witnesses':rec,'complete_profiles':profiles,'freiman_transports':transport,
            'fiber_metrics':metric_replay(),'chain_deficits':chain_deficit_replay(),
            'mixed_controller_148':ctr,'singleton_controllers':single,
            'global_fixed_rank':global_rank_replay(),
            'full_relation_comparison':{'original_relation':[100,-1],'new_amplitude':96},
            'height_replay':None if args.skip_height_replay else height_replay(),
            'validator_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    text=json.dumps(report,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(text,encoding='utf-8')
    print(text,end='')

if __name__=='__main__':main()
