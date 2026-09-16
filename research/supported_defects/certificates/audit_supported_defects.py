#!/usr/bin/env python3
"""Separate exact auditor; does not import or execute the producer.

Rebuilds original binary source fibres, numerical progression tuples,
orientation-score images and all original graph cuts.  Reads the complete
compressed proof records rather than accepting their summary counts.
"""
from __future__ import annotations
import argparse,copy,gzip,json
from collections import Counter,defaultdict
from fractions import Fraction
from math import gcd
from functools import reduce
from hashlib import sha256
from itertools import combinations,product
from pathlib import Path


def must(test,msg):
    if not test:raise AssertionError(msg)


def hash_obj(obj):return sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def binary_table(a):
    table=defaultdict(list)
    for x in product((0,1),repeat=len(a)):
        table[sum(u*v for u,v in zip(x,a))].append(x)
    return dict(table)


def progressions(a,k):
    """Independent enumeration by the FIRST AND LAST points, not by the step."""
    a=sorted(a);present=set(a);out=[]
    for x,y in combinations(a,2):
        gap=y-x
        if gap%(k-1):continue
        d=gap//(k-1)
        z=tuple(x+j*d for j in range(k))
        if set(z)<=present:out.append(z)
    return out


def check_deformation(rec):
    h=tuple(rec['h']);r=len(h);L=2*sum(h)+1
    a=tuple(x for j,t in enumerate(h) for x in (L*19**j,7*L*19**j,8*L*19**j+t))
    must(list(a)==rec['generators'] and L==rec['L'],'generator source changed')
    original=binary_table(a);defects=binary_table(h)
    must(len(original)==rec['distinct_values'],'wrong distinct-image count')
    hist=Counter(len(v) for v in original.values())
    must({str(x):y for x,y in hist.items()}==rec['multiplicity_histogram'],'wrong multiplicity profile')
    must(max(hist)==rec['max_multiplicity']==max(map(len,defects.values())),'wrong maximum fibre')
    highbase=tuple(x for j in range(r) for x in (19**j,7*19**j,8*19**j))
    highfib=binary_table(highbase)
    reconstructed={};predicted_aps={k:set() for k in (4,5,6)}
    for x,words in highfib.items():
        low=defaultdict(list)
        for w in words:low[sum(w[3*j+2]*h[j] for j in range(r))].append(w)
        for y,ww in low.items():
            val=L*x+y
            must(val not in reconstructed,'original fibres overlap')
            reconstructed[val]=set(ww)
        for k in predicted_aps:
            predicted_aps[k].update(tuple(L*x+y for y in row) for row in progressions(low,k))
    must(reconstructed=={x:set(w) for x,w in original.items()},'original source fibre equality failed')
    for k,pred in predicted_aps.items():
        actual=set(progressions(original,k))
        must(actual==pred and len(actual)==rec['ap_counts'][str(k)],'complete progression fibre check failed')
        must(bool(actual)==bool(progressions(defects,k)),'arithmetic witness existence changed')
    if all(h):
        must(bool(progressions(original,3))==bool(progressions(defects,3)),'three-term positive-defect check failed')
    return len(original),sum(rec['ap_counts'].values())


def connected_parts(n,edges):
    adj=[set() for _ in range(n)]
    for x,y in edges:adj[x].add(y);adj[y].add(x)
    unseen=set(range(n));parts=[]
    while unseen:
        root=min(unseen);seen={root};front=[root]
        while front:
            x=front.pop()
            for y in adj[x]-seen:seen.add(y);front.append(y)
        unseen-=seen;parts.append(sorted(seen))
    return parts


def cut(edges,U):return sum((x in U)!=(y in U) for x,y in edges)


def pair_cuts(n,edges):
    answer={}
    for x,y in combinations(range(n),2):
        others=[z for z in range(n) if z not in (x,y)]
        options=[]
        for choices in product((0,1),repeat=len(others)):
            U={x}|{z for z,b in zip(others,choices) if b}
            options.append(cut(edges,U))
        answer[x,y]=min(options)
    return answer


def check_graph(rec):
    n=rec['v'];edges=[tuple(e) for e in rec['edges']]
    must(len(edges)==len(set(edges)) and all(0<=x<y<n for x,y in edges),'invalid simple original graph')
    S=set()
    for orient in product((0,1),repeat=len(edges)):
        score=[0]*n
        for b,e in zip(orient,edges):score[e[b]]+=1
        S.add(tuple(score))
    must(len(S)==rec['score_values'],'wrong orientation-score source')
    mins=pair_cuts(n,edges);lam=max(mins.values(),default=0)
    must(lam==rec['lambda_max'] and rec['longest']==lam+1,'wrong pair-cut endpoint')
    if lam:
        x,d,length=rec['witness']
        must(length==lam+1 and any(d),'zero or wrong source witness')
        must(all(tuple(x[i]+j*d[i] for i in range(n)) in S for j in range(length)),'witness leaves original source')
    else:must(len(S)==1 and rec['witness'] is None,'edgeless witness wrong')
    components=connected_parts(n,edges);nontrivial=[C for C in components if len(C)>1]
    must(len(nontrivial)==len(rec['cut_trees']),'missing cut-tree component')
    path_mass=0
    for C,cert in zip(nontrivial,rec['cut_trees']):
        loc={u:i for i,u in enumerate(C)}
        ce=[(loc[x],loc[y]) for x,y in edges if x in loc and y in loc]
        cm=pair_cuts(len(C),ce);tree=[tuple(t[0]) for t in cert]
        must(len(tree)==len(C)-1 and len(connected_parts(len(C),tree))==1,'cut certificate is not a tree')
        for edge,U,capacity in cert:
            U=set(U)
            deleted=list(tree);deleted.remove(tuple(edge))
            comps=connected_parts(len(C),deleted)
            must(U==set(comps[0]) or U==set(comps[1]),'not a fundamental tree cut')
            must(cut(ce,U)==capacity==cm[tuple(sorted(edge))],'incorrect original min-cut capacity')
            observed={sum(s[C[j]] for j in U) for s in S}
            must(max(observed)-min(observed)==capacity,'cut does not retain source range')
        for u,v in combinations(range(len(C)),2):
            observed=min(q for _,U,q in cert if (u in U)!=(v in U))
            must(observed==cm[u,v],'cut tree lost a pair minimum')
        lengths=[sum((x in U)!=(y in U) for _,U,_ in cert) for x,y in ce]
        must(sum(lengths)==sum(t[2] for t in cert),'cut/path count not equal')
        path_mass+=sum(lengths)
    directions={}
    for x,y in combinations(sorted(S),2):
        vec=tuple(b-a for a,b in zip(x,y));g=reduce(gcd,(abs(a) for a in vec))
        d=tuple(a//g for a in vec)
        directions[d]=max(directions.get(d,0),g)
    expected_filtration=[]
    for q in range(1,lam+2):
        high=[edge for edge,c in mins.items() if c>=q]
        classes=connected_parts(n,high)
        expected_filtration.append([q,classes,n-len(classes)])
        for C in classes:
            for u,v in combinations(C,2):
                d=tuple(int(i==v)-int(i==u) for i in range(n))
                must(any(all(tuple(x[i]+j*d[i] for i in range(n)) in S for j in range(q+1)) for x in S),
                     'missing root-direction progression lift')
        for d,g in directions.items():
            if g>=q:must(all(sum(d[i] for i in C)==0 for C in classes),'actual direction not in reported module')
    must(rec['filtration']==expected_filtration,'wrong supported direction filtration')
    potentials=list(product(range(3),repeat=n)) if n<=4 else [tuple([0]*n),tuple(range(n)),tuple([0,0]+list(range(1,n-1)))]
    must([tuple(x[0]) for x in rec['visibility']]==potentials,'missing observation support')
    for row in rec['visibility']:
        t,visible,ideals=row
        source_max=max((g for d,g in directions.items() if sum(a*b for a,b in zip(t,d))),default=0)
        cut_max=max((c for (u,v),c in mins.items() if t[u]!=t[v]),default=0)
        must(source_max==visible==cut_max,'observed progression maximum wrong')
        expected=[]
        for q,classes,_ in expected_filtration:
            module_image=reduce(gcd,(abs(t[u]-t[v]) for C in classes for u,v in combinations(C,2)),0)
            source_image=reduce(gcd,(abs(sum(a*b for a,b in zip(t,d))) for d,g in directions.items() if g>=q),0)
            must(module_image==source_image,'observation image ideal missing a source direction')
            expected.append(module_image)
        must(ideals==expected,'image ideal data altered')
    rank=n-len(components)
    must(path_mass==rec['tree_path_mass'] and 2*len(edges)<=(lam+1)*rank,'source density budget wrong')
    return len(S),len(nontrivial)


def audit_signed_moduli():
    cases=maps=apmaps=0;rows=[]
    for r in (1,2):
        high=tuple(x for j in range(r) for x in (19**j,7*19**j,8*19**j))
        highfib=binary_table(high)
        for eta in product((-1,0,1),repeat=3*r):
            d=tuple(eta[3*j]+eta[3*j+1]-eta[3*j+2] for j in range(r))
            eta2=tuple(x for t in d for x in (0,0,-t))
            # Recover the internal vertex potential from the actual boundary cochain.
            difference=tuple(x-y for x,y in zip(eta,eta2))
            for j in range(r):
                a,b,c=difference[3*j:3*j+3]
                must(b==c-a,'retained representative difference is not a relative coboundary')
                must(d[j]-d[0]==(eta[3*j]+eta[3*j+1]-eta[3*j+2])-
                     (eta[0]+eta[1]-eta[2]),'absolute restriction lost a terminal component')
            L=2*sum(map(abs,eta))+1;L2=2*sum(map(abs,eta2))+1
            A=tuple(L*x+y for x,y in zip(high,eta));B=tuple(L2*x+y for x,y in zip(high,eta2))
            F=binary_table(A);G=binary_table(B);transport={}
            for x,words in highfib.items():
                shifts=set()
                for w in words:
                    y=sum(a*b for a,b in zip(w,A));z=sum(a*b for a,b in zip(w,B))
                    shifts.add(z-y)
                    if y in transport:must(transport[y]==z,'same-defect word map is ambiguous')
                    transport[y]=z
                must(len(shifts)==1,'tangent change has a nonconstant original fibre action')
            must(set(transport)==set(F) and set(transport.values())==set(G),'same-defect source map not onto')
            must(all(len(F[x])==len(G[y]) for x,y in transport.items()),'word masses changed')
            counts={}
            for k in (4,5,6):
                actual=set(progressions(F,k));other=set(progressions(G,k))
                must({tuple(transport[x] for x in row) for row in actual}==other,'perturbation AP transport failed')
                must(bool(actual)==bool(progressions(binary_table(d),k)),'signed defects gave wrong freeness')
                counts[str(k)]=len(actual);apmaps+=len(actual)
            ternary={sum(t*x for t,x in zip(word,d)) for word in product((0,1,2),repeat=r)}
            must((len(ternary)==3**r)==(not progressions(F,3)),'signed ternary criterion failed')
            rows.append([eta,d,L,L2,len(F),counts]);cases+=1;maps+=len(F)
    return {'scope':'all signed perturbations in {-1,0,1}^{3r}, r=1,2','cases':cases,
            'exact_value_transports':maps,'positive_AP_transports':apmaps,'transcript_sha256':hash_obj(rows)}

def specialization_audit():
    rows=[]
    for r in range(1,13):
        # Full original edge incidence, not an abstract sum operator.
        n=2*r+2
        E=[]
        for j in range(r):
            a,b=2*j+2,2*j+3
            E.extend(((0,a),(a,b),(1,b)))
        columns=[]
        for j in range(r):
            c=[0]*(3*r);c[3*j:3*j+3]=[1,1,-1]
            boundary=[0]*n
            for v,(a,b) in zip(c,E):boundary[a]-=v;boundary[b]+=v
            must(boundary==[-1,1]+[0]*(n-2),'null terminal boundary altered')
            columns.append(c)
        # Before identifying the terminals, the circuit differences have zero boundary.
        for j in range(1,r):
            c=[columns[j][i]-columns[0][i] for i in range(3*r)]
            boundary=[0]*n
            for v,(a,b) in zip(c,E):boundary[a]-=v;boundary[b]+=v
            must(not any(boundary),'retained theta cycle is not a cycle')
        must(Fraction(3,r)==sum(3*Fraction(1,r)**2 for _ in range(r)),'sum-coordinate metric incorrect')
        # The principal-ideal resolution gives multiplication by -t before specialization,
        # zero at t=0, and negative augmentation as its first-order connecting map.
        for coeffs in product((-1,0,1),repeat=min(r,4)):
            c=list(coeffs)+[0]*(r-len(coeffs));mass=sum(c)
            cycle=c[:];cycle[0]-=mass
            must(sum(cycle)==0 and c==[x+(mass if j==0 else 0) for j,x in enumerate(cycle)],'Bockstein decomposition failed')
        rows.append([r,r-1,r,str(Fraction(3,r))])
    return {'full_incidence_cases':12,'transcript_sha256':hash_obj(rows)}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--proof-data',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    raw=gzip.decompress(args.proof_data.read_bytes());obj=json.loads(raw)
    cases=obj['universal_cases'];expected=[list(h) for r in range(1,4) for h in product(range(3),repeat=r)]
    expected += [list(h) for h in ((1,3,4),(1,3,9),(0,1,3),(1,2,3))]
    must([x['h'] for x in cases]==expected,'deformation domain incomplete')
    uv=ua=0
    for rec in cases:
        v,a=check_deformation(rec);uv+=v;ua+=a
    graphs=obj['graphs'];expected_graphs=[]
    for n in range(1,6):
        E=list(combinations(range(n),2))
        expected_graphs.extend((n,tuple(e for j,e in enumerate(E) if bits>>j&1)) for bits in range(1<<len(E)))
    must([(r['v'],tuple(tuple(e) for e in r['edges'])) for r in graphs]==expected_graphs,'graph domain incomplete')
    sv=trees=0
    for rec in graphs:
        v,t=check_graph(rec);sv+=v;trees+=t
    rejected=[]
    def fail(name,fn):
        try:fn()
        except (AssertionError,KeyError,ValueError,IndexError):rejected.append(name)
        else:raise AssertionError('corrupt certificate accepted: '+name)
    a=copy.deepcopy(cases[-1]);a['distinct_values']+=1
    fail('false numerical image count',lambda:check_deformation(a))
    b=copy.deepcopy(cases[0]);b['max_multiplicity']=1
    fail('erased present-zero representation',lambda:check_deformation(b))
    c=copy.deepcopy(cases[-1]);c['generators'][-1]+=1
    fail('changed arithmetic generator',lambda:check_deformation(c))
    d=copy.deepcopy(cases[-1]);d['ap_counts']['4']+=1
    fail('false progression count',lambda:check_deformation(d))
    g=copy.deepcopy(graphs[-1]);g['lambda_max']-=1
    fail('false pair connectivity',lambda:check_graph(g))
    q=copy.deepcopy(graphs[-1]);q['cut_trees'][0][0][2]+=1
    fail('altered supported cut capacity',lambda:check_graph(q))
    w=copy.deepcopy(graphs[-1]);w['witness'][1]=[0]*w['v']
    fail('zeroed source witness',lambda:check_graph(w))
    fail('missing original graph support',lambda:must(len(graphs)-1==len(expected_graphs),'missing graph'))
    report={'schema':'ep817-supported-defect-independent-audit-v1','status':'PASS','lean_checked':False,
            'deformations':len(cases),'distinct_deformation_values':uv,'positive_step_APs_checked':ua,
            'graphs':len(graphs),'source_score_values':sv,'cut_trees':trees,
            'visibility_cases':sum(len(x['visibility']) for x in graphs),
            'image_ideal_checks':sum(len(v[2]) for x in graphs for v in x['visibility']),
            'signed_defect_moduli':audit_signed_moduli(),
            'specialization':specialization_audit(),'corrupt_records_rejected':rejected,
            'input_sha256':sha256(raw).hexdigest(),'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
