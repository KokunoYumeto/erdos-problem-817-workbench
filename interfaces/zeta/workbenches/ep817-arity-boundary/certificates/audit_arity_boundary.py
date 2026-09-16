#!/usr/bin/env python3
"""Independent exact audit; imports no producer module.

Recomputes digit polynomials, carry targets by quotient enumeration, and direct
image moments by bitwise Boolean polynomial products of the ORIGINAL generators.
Real-limit graphs are checked by destination enumeration and independent SCCs.
"""
from __future__ import annotations
import argparse
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import comb
from pathlib import Path
import json


def need(ok,msg):
    if not ok:raise AssertionError(msg)


def polynomial(A,q):
    v=[1]
    for a in A:
        w=[0]*(len(v)+(q-1)*a)
        for j in range(q):
            for i,c in enumerate(v):w[i+j*a]+=c
        v=w
    return {i:c for i,c in enumerate(v)if c}


def action_audit(item,b):
    D=dict(item['digit_weights']);m=item['machine'];C=max(D)//(b-1)
    need(m['carry_bound']==C and m['base']==b,'carry bound altered')
    states=m['states'];need(states[0]==1 and len(set(states))==len(states),'state identity altered')
    lookup={v:i for i,v in enumerate(states)};matrix=[];reachable={0}
    for i,R in enumerate(states):
        need(0<=R<1<<(C+1),'state outside carry box');row=[]
        for z in range(b):
            out={t for c in range(C+1)if (R>>c)&1 for t in range(C+1)
                 if z+b*t-c in D}
            label=sum(1<<t for t in out)
            need(label in lookup,'missing supported destination')
            row.append(lookup[label])
        need(row==m['transitions'][i],'altered original digit action')
        counts=[0]*len(states)
        for j in row:counts[j]+=1
        matrix.append(counts)
    need(matrix==m['matrix'],'matrix is not full residue aggregation')
    while True:
        new=reachable|{j for i in reachable for j in m['transitions'][i]}
        if new==reachable:break
        reachable=new
    need(reachable==set(range(len(states))),'unreached or missing state')
    need(m['terminal']==[sum(1 for c in range(C+1)if (R>>c)&1)for R in states],
         'terminal value count changed')
    return b*len(states)


_BYTE=[]
for v in range(256):
    pos=[i for i in range(8)if (v>>i)&1]
    _BYTE.append((len(pos),sum(pos),sum(i*i for i in pos)))


def direct_image(A,b,q,m):
    bits=1
    for j in range(m):
        for a in A:
            w=a*b**j;old=bits;bits=0
            for t in range(q):bits |=old<<(t*w)
    N=S1=S2=0
    for block,v in enumerate(bits.to_bytes((bits.bit_length()+7)//8,'little')):
        n,s,t=_BYTE[v];x=8*block;N+=n;S1+=n*x+s;S2+=n*x*x+2*x*s+t
    need(N==bits.bit_count(),'bit moment count inconsistent')
    return [N,S1,S2]


def mv(M,v):return [sum(a*b for a,b in zip(row,v))for row in M]


def power_observation(M,f,out,poly,shift):
    for _ in range(shift):f=mv(M,f)
    v=f[:];w=[0]*len(f)
    for a in poly:
        w=[x+a*y for x,y in zip(w,v)];v=mv(M,v)
    seen=[]
    for _ in range(len(M)):
        seen.append(w[out]);w=mv(M,w)
    need(not any(seen),'false recurrence admitted')
    return seen


def moment_audit(item,b):
    m=item['machine'];n=len(m['states']);C=m['carry_bound'];P=2
    F=[[sum(c**p for c in range(C+1)if (R>>c)&1)for R in m['states']]for p in range(3)]
    seq=[]
    for t in range(9):
        seq.append([F[p][0]for p in range(3)])
        G=[[0]*n for _ in range(3)]
        for s,row in enumerate(m['transitions']):
            for z,target in enumerate(row):
                for p in range(3):
                    for j in range(p+1):G[p][s]+=comb(p,j)*z**(p-j)*b**j*F[j][target]
        F=G
    need(seq==item['moments_through_m20'][:9],'moment transport altered')
    form=item['series'];poly=form['recurrence_polynomial']
    power_observation(m['matrix'],m['terminal'],0,poly,form['recurrence_shift'])
    den=form['denominator'];num=form['numerator'];allseq=[x[0]for x in item['moments_through_m20']]
    for j in range(len(allseq)):
        t=sum(a*allseq[j-i]for i,a in enumerate(den)if i<=j)
        need(t==(num[j]if j<len(num)else 0),'series coefficient mismatch')
    return len(seq)


def recurrence_weight(weights,b,m,x,cache=None):
    if cache is None:cache={}
    key=(m,x)
    if key in cache:return cache[key]
    if m==0:return int(x==0)
    n=sum(w*recurrence_weight(weights,b,m-1,(x-d)//b,cache)
          for d,w in weights.items()if x>=d and (x-d)%b==0)
    cache[key]=n;return n


def delta(x):return tuple(x[i]-2*x[i+1]+x[i+2]for i in range(len(x)-2))


def strongly_live(rows):
    n=len(rows);adj=[[j for j,_ in row]for row in rows];rev=[[]for _ in rows]
    for i,ds in enumerate(adj):
        for j in ds:rev[j].append(i)
    seen=set();order=[]
    for root in range(n):
        if root in seen:continue
        seen.add(root);stack=[(root,0)]
        while stack:
            u,j=stack[-1]
            if j<len(adj[u]):
                v=adj[u][j];stack[-1]=(u,j+1)
                if v not in seen:seen.add(v);stack.append((v,0))
            else:order.append(u);stack.pop()
    seen=set();cycles=set()
    for root in reversed(order):
        if root in seen:continue
        block=set([root]);seen.add(root);stack=[root]
        while stack:
            u=stack.pop()
            for v in rev[u]:
                if v not in seen:seen.add(v);block.add(v);stack.append(v)
        if len(block)>1 or root in adj[root]:cycles |=block
    live=set(cycles);stack=list(cycles)
    while stack:
        u=stack.pop()
        for v in rev[u]:
            if v not in live:live.add(v);stack.append(v)
    return live


def audit_real_graph(g,D):
    b=g['base'];k=g['k'];C=2*max(D)//(b-1)
    states=[(tuple(c),f)for c,f in g['states']];lookup={s:i for i,s in enumerate(states)}
    need(C==g['carry_bound'] and len(lookup)==len(states),'real state bound altered')
    for i,(c,f)in enumerate(states):
        actual={}
        # Destination carries fixed first; a column is then uniquely determined by its first two digits.
        for dest in product(range(-C,C+1),repeat=k-2):
            flags=set()
            for a in D:
                for e in D:
                    ds=[a,e]
                    for h,v in enumerate(dest):
                        t=2*ds[-1]-ds[-2]-b*c[h]+v
                        if t not in D:break
                        ds.append(t)
                    if len(ds)==k:flags.add(f or a!=e)
                    if f and flags:break
                    if not f and len(flags)==2:break
                if f and flags:break
                if not f and len(flags)==2:break
            for flag in flags:
                need((dest,flag)in lookup,'missing real-limit state')
                actual[lookup[(dest,flag)]]=True
        stored={j for j,d in g['edges'][i]}
        need(stored==set(actual),'missing/extra real-limit transition')
        for j,d in g['edges'][i]:
            need(all(x in D for x in d),'real graph label outside binary source')
            need(tuple(b*x+y for x,y in zip(c,delta(d)))==states[j][0],
                 'wrong persistent second-difference carry')
            need(states[j][1]==(f or d[0]!=d[1]),'nonconstancy flag altered')
    live=strongly_live(g['edges']);need(sorted(live)==g['infinite_path_states'],'wrong infinite-path kernel')
    exists=any(states[i][1]for i in live)
    need(exists==(g['witness']is not None),'wrong real AP decision')
    return sum(len(row)for row in g['edges'])


def brute_small_real(D,b,k):
    C=2*max(D)//(b-1);init=((0,)*(k-2),False);states=[init];idx={init:0};rows=[]
    cols=[(d,delta(d),d[0]!=d[1])for d in product(sorted(D),repeat=k)]
    for c,f in states:
        targets={}
        for ds,v,t in cols:
            z=tuple(b*x+y for x,y in zip(c,v))
            if any(abs(x)>C for x in z):continue
            st=(z,f or t)
            if st not in idx:idx[st]=len(states);states.append(st)
            targets[idx[st]]=list(ds)
        rows.append([[j,d]for j,d in sorted(targets.items())])
    live=strongly_live(rows)
    return any(states[j][1]for j in live)


def audit(data, full=True):
    need(data['schema']=='ep817-arity-boundary-v1' and data['status']=='PASS','record status invalid')
    actions=direct=mom=weights=0;digests=sha256()
    for rec in data['records']:
        A=rec['generators'];b=rec['base'];k=rec['forbidden_length'];D2=polynomial(A,2)
        for x in D2:
            for step in range(1,b):
                need(not all((x+i*step)%b in D2 for i in range(k)), 'binary modular failure')
        for item in rec['arities']:
            q=item['arity'];w=polynomial(A,q)
            need(item['digit_weights']==[[d,v]for d,v in w.items()], 'local polynomial altered')
            actions+=action_audit(item,b);mom+=moment_audit(item,b)
            if full:
                for m in range(4 if b<100 else 3):
                    result=direct_image(A,b,q,m)
                    need(result==item['moments_through_m20'][m],'original generators disagree with quotient moments')
                    digests.update((repr((A,b,q,m,result))+'\n').encode());direct+=1
        tern=rec['arities'][1];w=dict(tern['digit_weights']);h=rec['ternary_holes'];D=set(w);W=max(D);H=set(h['holes'])
        need(D==set(range(W+1))-H-{W-x for x in H},'hole source incomplete')
        need(D|{b+x for x in D}==set(range(b+W+1))-H-{b+W-x for x in H},'two-translate fill false')
        wr=rec['weighted_metric_certificate'];s=[sum(c for d,c in w.items()if d%b==r)for r in range(b)]
        need(s==wr['residue_masses'] and max(s)==max(w.values())==wr['maximum_original_multiplicity'],'weighted residue budget false')
        for m in range(1,9):
            rep=(b**m-1)//(b-1)
            need(recurrence_weight(w,b,m,wr['constant_output_digit']*rep)==max(w.values())**m,'original multiplicity witness failed')
            need(recurrence_weight({d:1 for d in D},b,m,wr['all_ones_output_digit']*rep)==2**(m-1),'image-word multiplicity witness failed')
            weights+=2
        rel=rec['cross_level_relation']
        need(all(-2<=c<=2 for c in rel['lower']+rel['upper']) and
             sum(a*c for a,c in zip(A,rel['lower']))==b*sum(a*c for a,c in zip(A,rel['upper']))!=0,'missing cross-level relation')
        raw=rec['raw_second_moment'];roots=raw['roots'];cs=[Fraction(x)for x in raw['coefficients']]
        tm=tern['machine']; nn=len(tm['states']); CC=tm['carry_bound']
        BB=[[0]*(3*nn)for _ in range(3*nn)]
        for pp in range(3):
            for rr,row in enumerate(tm['transitions']):
                for zz,tt in enumerate(row):
                    for jj in range(pp+1):
                        BB[pp*nn+rr][jj*nn+tt]+=comb(pp,jj)*zz**(pp-jj)*b**jj
        ff=[sum(cc**pp for cc in range(CC+1)if (RR>>cc)&1)for pp in range(3)for RR in tm['states']]
        power_observation(BB,ff,2*nn,raw['annihilator'],0)
        need(all(sum(c*r**m for r,c in zip(roots,cs))==x[2]for m,x in enumerate(tern['moments_through_m20'])), 'second moment constants false')
        lm=rec['limit'];C0=Fraction(len(w)-h['kappa'],b-h['kappa']);span=Fraction(W,b-1)
        need(Fraction(lm['ternary_mass'])==C0 and Fraction(lm['span'])==span and
             Fraction(lm['remaining_outer_mass'])==span-C0,'limit mass transport false')
        eta=cs[-1]/C0-span*span/4
        need(Fraction(lm['scaled_uniform_variance'])==eta and
             Fraction(lm['variance_over_Q'])==eta*(b*b-1)/sum(a*a for a in A),'variance observation mixed with multiplicities')
    MM=data['records'][2]['arities'][2]['machine']['matrix']
    VV=[1,0,0,1,0]; WW=[0,-411,1,0,1]
    need(mv(MM,VV)==[3*x for x in VV], 'Jordan eigenvector failed')
    need([x-3*y for x,y in zip(mv(MM,WW),WW)]==[824*x for x in VV], 'Jordan generalized vector failed')
    seq=[x[0]for x in data['records'][2]['arities'][2]['moments_through_m20']]
    aa,bb,cc=seq[:3];dd,ee,ff=seq[1:4];gg,hh,ii=seq[2:5]
    need(aa*(ee*ii-ff*hh)-bb*(dd*ii-ff*gg)+cc*(dd*hh-ee*gg)!=0, 'observable order was reduced')
    real_edges=0
    for g in data['real_boundary']['complete_record_machines']:
        A=(1,7,8)if g['base']==19 else (1,4,5,17,21,22)
        if full:real_edges+=audit_real_graph(g,set(polynomial(A,2)))
    for x in data['real_boundary']['examples']:
        A=x['generators'];b=x['base'];a=x['prefix'];e=x['period'];c=delta(a)
        need(any(c) and delta(e)==tuple(-(b-1)*v for v in c),'boundary defect cancelled incorrectly')
        for ds,masks in ((a,x['prefix_masks']),(e,x['period_masks'])):
            for d,mask in zip(ds,masks):need(d==sum(v for j,v in enumerate(A)if (mask>>j)&1),'real source mask false')
        xs=[Fraction((b-1)*u+v,b*(b-1))for u,v in zip(a,e)]
        need([str(y)for y in xs]==x['values'] and not any(delta(xs)) and xs[1]!=xs[0],'real progression false')
        for p in x['finite_prefixes']:
            m=p['length'];Y=[u*b**(m-1)+v*(b**(m-1)-1)//(b-1)for u,v in zip(a,e)]
            need(Y==p['integer_points'] and delta(Y)==tuple(p['second_difference'])==c,'finite observation overwritten by limit')
    small=none=0
    if full:
        for b in range(3,8):
            for mask in range(1<<(b-2)):
                D={0}|{d for d in range(1,b-1)if (mask>>(d-1))&1}
                for k in range(3,6):small+=1;none+=not brute_small_real(D,b,k)
        s=data['real_boundary']['small_domain'];need(small==s['alphabets_and_lengths'] and none==s['no_real_ap'],'small real graph disagreement')
    return {"residue_actions":actions,"direct_original_moment_cases":direct,
            "moment_states_checked":mom,"exact_peak_instances":weights,
            "record_real_graph_arcs":real_edges,"brute_force_real_sources":small,
            "no_real_AP_sources":none,"direct_transcript_sha256":digests.hexdigest()}


def mutations(data):
    tests=[]
    def run(label,change):
        d=deepcopy(data);change(d)
        try:audit(d,False)
        except AssertionError:tests.append(label)
        else:raise AssertionError('mutation escaped: '+label)
    run('original digit multiplicity',lambda d:d['records'][0]['arities'][1]['digit_weights'][0].__setitem__(1,2))
    run('supported zero terminal',lambda d:d['records'][0]['arities'][0]['machine']['terminal'].__setitem__(0,0))
    run('omitted residue transition',lambda d:d['records'][2]['arities'][2]['machine']['transitions'][0].__setitem__(0,0))
    run('semisimplified repeated pole',lambda d:d['records'][2]['arities'][2]['series'].__setitem__('denominator',[1,-1654,4953]))
    run('uncorrected count',lambda d:d['records'][0]['arities'][1]['moments_through_m20'][2].__setitem__(0,139**2))
    run('false uniform weight budget',lambda d:d['records'][2]['weighted_metric_certificate'].__setitem__('maximum_original_multiplicity',218))
    run('erased terminal defect',lambda d:d['real_boundary']['examples'][1]['finite_prefixes'][0].__setitem__('second_difference',[0,0,0]))
    run('altered least-norm variance',lambda d:d['records'][0]['limit'].__setitem__('scaled_uniform_variance','1/4'))
    return tests


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();data=json.loads(args.input.read_text());result=audit(data)
    result.update({"schema":"ep817-arity-boundary-independent-audit-v1","status":"PASS","lean_checked":False,
                   "mutations_rejected":mutations(data),"receipt_sha256":sha256(args.input.read_bytes()).hexdigest(),
                   "auditor_sha256":sha256(Path(__file__).read_bytes()).hexdigest()})
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
