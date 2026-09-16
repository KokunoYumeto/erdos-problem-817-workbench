#!/usr/bin/env python3
"""Independent arithmetic audit of the delivered graphical proof data.

This file imports no producer module. It reconstructs masks, source scores,
modular exclusions, all lower-radix witnesses, the entire finite extension
classification, and all complete root-budget witness domains.
"""
from __future__ import annotations
import argparse,copy,gzip,hashlib,json
from collections import Counter,defaultdict
from fractions import Fraction
from itertools import combinations,product
from pathlib import Path


def need(ok:bool,message:str)->None:
    if not ok:raise AssertionError(message)


def mask_value(A,mask):
    need(isinstance(mask,int) and 0<=mask<(1<<len(A)), 'mask outside original source')
    return sum(a for i,a in enumerate(A) if mask & (1<<i))


def all_fibres(A):
    out=defaultdict(list)
    for mask in range(1<<len(A)):out[mask_value(A,mask)].append(mask)
    return dict(out)


def score(m,mask):
    out=[0]*m
    for e,(i,j) in enumerate(combinations(range(m),2)):
        out[i if mask & (1<<e) else j]+=1
    return tuple(out)


def progression(values,k):
    D=set(values);order=sorted(D)
    for a in order:
        for b in order:
            if b<=a:continue
            if a+(k-1)*(b-a)>order[-1]:break
            row=tuple(a+i*(b-a) for i in range(k))
            if all(x in D for x in row):return row
    return None


def delta(row):return tuple(row[i]+row[i+2]-2*row[i+1] for i in range(len(row)-2))


def check_return(row,D):
    c=tuple(row['carry']);r=tuple(row['digits'])
    need(len(c)==4 and len(r)==6 and all(x in D for x in r),'return-domain defect')
    need(delta(r)==tuple(-x for x in c),'incorrect returning source column')


def check_bad_base(rec,A,D):
    q=rec['base'];low=rec['low'];high=rec['high'];c=rec['carry'];ys=rec['points']
    need(all(x in D for x in low+high),'non-source digit in obstruction')
    need(low[0]!=low[1] and all(t%q==0 for t in delta(low)), 'invalid modular obstruction')
    need(tuple(t//q for t in delta(low))==tuple(c),'wrong carry observation')
    need(delta(high)==tuple(-x for x in c),'wrong second-level primitive')
    need(ys==[x+q*y for x,y in zip(low,high)],'incorrect numerical evaluation')
    need(ys[1]!=ys[0] and not any(delta(ys)),'zero or nonarithmetic witness')
    source=A+tuple(q*x for x in A)
    need(all(mask_value(source,m)==y for m,y in zip(rec['subset_masks'],ys)),'incorrect original subset witness')


def check_rigidity_row(row):
    m=row['vertices'];r=tuple(row['relation']);i,j=row['root'];masks=row['subset_masks']
    need(len(r)==m and any(r) and sum(r)==0 and 0<=i<m and 0<=j<m and i!=j,'bad relation type')
    need(r[i]==max(r) and r[j]==min(r),'wrong retained extrema')
    need(len(masks)==m+1,'wrong packet length')
    S=[score(m,mask) for mask in masks]
    need(S==[tuple(s) for s in row['scores']],'source scores not represented by their masks')
    alpha=tuple(int(h==j)-int(h==i) for h in range(m))
    need(tuple(y-x for x,y in zip(S[0],S[1]))==alpha,'root increment changed')
    for h in range(m-1):
        dd=tuple(S[h][a]-2*S[h+1][a]+S[h+2][a] for a in range(m))
        need(dd==(r if h==m-2 else (0,)*m),'original relation not the sole final defect')
    need(tuple(row['last_second_defect'])==r,'misstated output defect')


def audit(rec,previous):
    need(rec['status']=='PASS' and rec['lean_checked'] is False,'scope/status mismatch')
    c=rec['candidate'];T=tuple(c['ruler']);E=tuple(combinations(range(len(T)),2));A=tuple(T[j]-T[i] for i,j in E)
    need(T==(0,4,7,41,257) and A==tuple(c['generators_in_edge_order']),'candidate source changed')
    need(len(set(A))==10 and min(A)>0 and sum(A)==1102,'generator-set defect')
    F=all_fibres(A);D=set(F);q=c['base']
    need(q==1651 and c['k']==6 and len(D)==291 and c['digits']==sorted(D),'candidate statement mismatch')
    need({y:sorted(ms) for y,ms in c['all_binary_fibres']}=={y:sorted(ms) for y,ms in F.items()},'original fibers changed')
    # All starts outside D are immediately excluded by their first term.
    pairs=0
    for start in sorted(D):
        for step in range(1,q):
            pairs+=1
            need(any((start+j*step)%q not in D for j in range(1,6)),'nonzero-step modular AP found')
    need(c['modular_parameter_pairs']==q*(q-1) and c['modular_AP_count']==0,'modular scope mismatch')
    section=c['return_section'];need({tuple(r['carry']) for r in section}==set(product((-1,0,1),repeat=4)) and len(section)==81,'incomplete returning domain')
    for row in section:check_return(row,D)
    bad=c['excluded_smaller_canonical_bases'];need([r['base'] for r in bad]==list(range(1103,1651)),'smaller-radix coverage gap')
    for row in bad:check_bad_base(row,A,D)
    for y,ms in F.items():need(Fraction(c['source_gram'][str(y)])==Fraction(1,len(ms)),'quotient metric changed')
    need(c['strict_improvement']['new_cubed']==1651**3<93**5==c['strict_improvement']['old_fifth'],'rate comparison failed')
    SF={score(5,mask) for mask in range(1024)};C=sum(i*t for i,t in enumerate(T))
    need(len(SF)==291 and len({C-sum(t*x for t,x in zip(T,s)) for s in SF})==291,'claimed score injection failed')
    need(len({tuple(x+y for x,y in zip(a,b)) for a in SF for b in SF})==c['vector_double_image_count']==3081,'double source changed')
    need(len({a+b for a in D for b in D})==c['integer_ternary_image_count']==2103,'double observation changed')
    ext=rec['extensions'];prefix=(0,4,7,41);old=tuple(y-x for x,y in combinations(prefix,2));oldF=all_fibres(old)
    layers=[]
    for rank in range(5):
        layer={y-sum(prefix[i] for i in I) for y in oldF for I in combinations(range(4),rank)}
        need(progression(layer,6) is None,'infinite-family fiber obstruction found')
        layers.append({'new_edges_selected':rank,'count':len(layer),'min':min(layer),'max':max(layer)})
    need(ext['finite_fibres']==layers and ext['width_budget']==178 and ext['all_z_greater_than_safe_bound']==356,'tail theorem inputs changed')
    params=ext['complete_lower_parameter_classification'];need([r['z'] for r in params]==list(range(42,357)),'parameter domain gap')
    cc=Counter()
    for row in params:
        U=prefix+(row['z'],);B=tuple(y-x for x,y in combinations(U,2));status=row['status'];cc[status]+=1
        if status=='repeated_generator':need(len(set(B))<len(B),'fake duplicate');continue
        need(len(set(B))==10,'duplicate generator in admitted family')
        FF=all_fibres(B)
        if status=='safe_integer':need(progression(FF,6) is None,'false small-parameter safety')
        elif status=='integer_obstruction':
            ys=row['witness'];need(len(ys)==6 and ys[1]!=ys[0] and not any(delta(ys)),'invalid finite obstruction')
            need(all(mask_value(B,m)==y for m,y in zip(row['masks'],ys)),'finite obstruction outside source')
        else:raise AssertionError('unknown status')
    need(dict(cc)==ext['counts'],'wrong classification count')
    # Literal symbolic coefficient verification of the two-parameter hyperplane.
    P=(0,1,5,22);B=tuple(y-x for x,y in combinations(P,2));sym=ext['universal_obstruction']
    need(sym['intercepts']==[-22+17*j for j in range(6)] and sym['slope']==1,'symbolic row altered')
    for intercept,(oldmask,newmask) in zip(sym['intercepts'],sym['old_and_new_masks']):
        need(newmask.bit_count()==1 and mask_value(B,oldmask)-mask_value(P,newmask)==intercept,'symbolic source coefficients wrong')
    rigidity=rec['collision_rigidity'];rows=rigidity['complete_witnesses'];lookup=defaultdict(list)
    for row in rows:check_rigidity_row(row);lookup[row['vertices']].append(tuple(row['relation']))
    for m in range(2,6):
        N=m*(m-1)//2;S={score(m,mask) for mask in range(1<<N)}
        directions={tuple(y-x for x,y in zip(s,t)) for s in S for t in S if s!=t}
        need(len(lookup[m])==len(directions) and set(lookup[m])==directions,'complete root-budget witness domain changed')
    need(len(rows)==3300==rigidity['complete_witness_count'],'wrong complete collision count')
    bcount=0
    if previous is not None:
        for entry in rec['bellman_future']['records']:
            k,r=entry['k'],entry['rank'];p=previous/f'variable_k{k}_r{r}.json.gz';raw=p.read_bytes()
            need(hashlib.sha256(raw).hexdigest()==entry['predecessor_sha256'],'predecessor changed')
            oldrec=json.loads(gzip.decompress(raw));f=list(map(Fraction,entry['future_cost_power']));B,power=entry['target']['base'],entry['target']['root'];states=oldrec['states'];EE=oldrec['representative_edges']
            need(len(f)==len(states) and all(Fraction(1,2**power)<=x<=1 for x in f),'future metric range failed')
            for i in range(len(states)):
                expected=min([Fraction(1)]+[Fraction(rad**power,B**n)*f[v] for u,v,rad,n,li in EE if u==i])
                need(f[i]==expected,'Bellman fixed-point equality failed')
            need(all(f[i]<=f[j] for i,x in enumerate(states) for j,y in enumerate(states) if x&y==x),'support monotonicity failed');bcount+=1
    # Mutations are tested against the exact validators, not a status bit.
    mutations=[]
    def reject(name,fn):
        try:fn()
        except (AssertionError,KeyError,ValueError,IndexError):mutations.append(name)
        else:raise AssertionError('false mutation admitted: '+name)
    rr=copy.deepcopy(section[0]);rr['digits'][0]+=1;reject('changed_return_primitive',lambda:check_return(rr,D))
    bb=copy.deepcopy(bad[0]);bb['subset_masks'][0]^=1;reject('changed_subset_mask',lambda:check_bad_base(bb,A,D))
    bb2=copy.deepcopy(bad[-1]);bb2['points'][0]+=1;reject('changed_numerical_point',lambda:check_bad_base(bb2,A,D))
    cr=copy.deepcopy(rows[-1]);cr['subset_masks'][-1]^=1;reject('changed_root_packet_mask',lambda:check_rigidity_row(cr))
    cr2=copy.deepcopy(rows[-1]);cr2['relation'][0]+=1;reject('changed_original_relation',lambda:check_rigidity_row(cr2))
    reject('omitted_radix',lambda:need([r['base'] for r in bad[:-1]]==list(range(1103,1651)),'coverage'))
    reject('omitted_collision_class',lambda:need(len(rows[:-1])==3300,'collision coverage'))
    reject('unit_quotient_metric',lambda:need(all(len(ms)==1 for ms in F.values()),'metric'))
    return {'status':'PASS','producer_imported':False,'candidate_actual_start_step_pairs':pairs,
            'outside_start_pairs_excluded_by_first_digit':(q-len(D))*(q-1),'returning_columns':len(section),
            'lower_canonical_radix_witnesses':len(bad),'finite_extension_parameters':len(params),
            'complete_collision_packets':len(rows),'predecessor_Bellman_records':bcount,
            'rejected_mutations':mutations}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--receipt',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--predecessor-certificates',type=Path,default=Path(__file__).resolve().parent/'predecessor_inputs')
    a=ap.parse_args();raw=a.receipt.read_bytes();rec=json.loads(gzip.decompress(raw) if a.receipt.suffix=='.gz' else raw)
    out=audit(rec,a.predecessor_certificates);out['receipt_file_sha256']=hashlib.sha256(raw).hexdigest();out['auditor_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    text=json.dumps(out,sort_keys=True,indent=2)+'\n';a.output.write_text(text,encoding='utf-8');print(text,end='')
if __name__=='__main__':main()
