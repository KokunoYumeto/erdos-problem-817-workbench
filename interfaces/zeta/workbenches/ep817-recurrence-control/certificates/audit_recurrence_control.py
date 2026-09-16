#!/usr/bin/env python3
"""Separately implemented exact audit. Does not import the producer module."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from collections import defaultdict, deque
from fractions import Fraction
from itertools import product
from pathlib import Path


def check(ok, message):
    if not ok:
        raise AssertionError(message)


def weights(n):
    result=[]
    p,q=0,1
    for _ in range(n):
        result.append(q)
        p,q=q,2*q+p
    return result


def sums(a):
    out={0}
    for x in a:
        out.update({y+x for y in out})
    return out


def count_progressions(values,k):
    ordered=sorted(values);answer=0
    for i,x in enumerate(ordered):
        for y in ordered[i+1:]:
            d=y-x
            if x+(k-1)*d>ordered[-1]:
                break
            if all(x+j*d in values for j in range(2,k)):
                answer+=1
    return answer


def as_state(raw):
    return tuple(tuple(p) for p in raw[0]),bool(raw[1])


def check_graphs(report):
    carriers={(-2,1),(-1,0),(0,0),(1,0),(2,-1)}
    check({tuple(c) for c in report['scalar_carries']}==carriers,'wrong scalar carrier')
    sizes=[]
    for item in report['graphs']:
        k=item['k'];states=[as_state(s) for s in item['states']]
        check(len(set(states))==len(states),'duplicate state')
        check(all(len(s[0])==k-2 and all(p in carriers for p in s[0]) for s in states),
              'unsupported state coordinate')
        ids={s:i for i,s in enumerate(states)}
        initial=(((0,0),)*(k-2),False)
        check(initial in ids and item['initial']==ids[initial],'initial support erased')
        expected=[]
        for si,(old,flag) in enumerate(states):
            for col in product((0,1),repeat=k):
                nxt=[]
                for j,(u,v) in enumerate(old):
                    # Work in 1,sqrt(2), multiplying by 1+sqrt(2),
                    # then return to the original 1,alpha coordinates.
                    a,b=u+v,v
                    A,B=a+2*b,a+b
                    A+=col[j]+col[j+2]-2*col[j+1]
                    nxt.append((A-B,B))
                if not all(p in carriers for p in nxt):
                    continue
                target=(tuple(nxt),flag or col[0]!=col[1])
                check(target in ids,'missing supported target')
                expected.append((si,ids[target],tuple(col)))
        actual=[(e[0],e[1],tuple(e[2])) for e in item['edges']]
        check(sorted(actual)==sorted(expected),'complete labeled edges mismatch')
        reached={ids[initial]}
        while True:
            more=reached|{t for s,t,c in actual if s in reached}
            if more==reached:
                break
            reached=more
        check(reached==set(range(len(states))),'unreachable support asserted reachable')
        accepting=[i for i,(row,f) in enumerate(states) if f and all(u+2*v==0 for u,v in row)]
        check(accepting==item['accepting'],'supported scalar-zero target erased')
        counts=[];paths={ids[initial]:1}
        for n in range(41):
            oriented=sum(paths.get(i,0) for i in accepting)
            check(oriented%2==0,'reversal count')
            counts.append(oriented//2)
            out=defaultdict(int)
            for s,t,c in actual:out[t]+=paths.get(s,0)
            paths=out
        check(counts==item['positive_ap_counts_n0_through40'],'path count mismatch')
        if k>=5:
            check(not accepting,'forbidden progression accepted')
        sizes.append([k,len(states),len(actual)])
    check(sizes==[[3,8,26],[4,22,46],[5,27,28],[6,49,50]],'full graph inventory')


def check_motif(report):
    data=report['seven_ap_motif']
    columns=data['columns'];masks=data['masks']
    check(len(columns)==6 and len(masks)==7,'missing motif support')
    vectors=[[sum(columns[i][j] for i in range(6) if mask&(1<<i)) for j in range(3)]
             for mask in masks]
    check(vectors==[[1,j,j] for j in range(7)],'motif does not evaluate to seven AP')
    check(vectors==data['vector_values'],'retained motif image')
    rel=data['relation_rows']
    for j in range(5):
        dd=[int(bool(masks[j]&(1<<i)))-2*int(bool(masks[j+1]&(1<<i)))
            +int(bool(masks[j+2]&(1<<i))) for i in range(6)]
        coeff=data['second_difference_primitives'][j]
        check(dd==[sum(coeff[t]*rel[t][i] for t in range(3)) for i in range(6)],'relation primitive')
    for case in data['applications']:
        delay=case['delay'];a=list(case['initial'])
        while len(a)<=2*delay:a.append(a[len(a)-delay]+2*a[-1])
        inds=[0,delay-1,delay,2*delay-2,2*delay-1,2*delay]
        check(inds==case['indices'] and len(set(inds))==6,'delay support alias')
        w=[a[i] for i in inds]
        check(w==case['weights'],'original recurrent weights changed')
        v=[sum(w[j] for j in range(6) if mask>>j&1) for mask in masks]
        d=a[delay-1]+a[2*delay-2]
        check(v==[a[0]+j*d for j in range(7)]==case['points'],'actual seven AP failure')
    check(len(data['applications'])==90,'missing delayed parameter instance')
    alias=data['delay_two_alias'];mapping=[0,1,2,2,3,4]
    push=[[sum(int(mapping[j]==i and mask>>j&1) for j in range(6)) for i in range(5)]
          for mask in masks]
    check(alias['coordinate_map']==mapping and alias['pushed_words']==push,'support-changing map altered')
    w=weights(5);y=[sum(x*t for x,t in zip(row,w)) for row in push]
    check(y==alias['scalar_values'] and alias['missing_value']==22,'alias value ledger')
    check(push[3][2]==2 and 22 not in sums(w),'unsupported repeated generator not detected')


def check_gf(report):
    gf=report['four_ap_generating_function']
    check(gf['numerator']==[0,0,1] and gf['denominator']==[1,-3,-2,8],'wrong rational function')
    g=next(x for x in report['graphs'] if x['k']==4);N=len(g['states'])
    matrix=[[0]*N for _ in range(N)]
    for s,t,d in g['edges']:matrix[s][t]+=1
    # Transpose viewpoint: propagate the accepting observation backwards.
    obs=[int(i in g['accepting']) for i in range(N)]
    initial=g['initial'];sequence=[]
    for _ in range(N+3):
        sequence.append(obs[initial])
        obs=[sum(matrix[i][j]*obs[j] for j in range(N)) for i in range(N)]
    residual=[sequence[j+3]-3*sequence[j+2]-2*sequence[j+1]+8*sequence[j] for j in range(N)]
    check(not any(residual) and residual==gf['residual_outputs'],'full matrix recurrence residual')
    check(sequence[:3]==[0,0,2],'rational numerator')


def core(report):
    check(report['status']=='PASS' and report['lean_checked'] is False,'evidence scope')
    check_graphs(report);check_motif(report);check_gf(report)


def independent_arithmetic(report):
    direct=0
    for entry in report['direct_pell_checks']:
        n=entry['n']
        if n>11:continue
        a=weights(n);H=sums(a)
        check(len(H)==entry['image_size']==2**n,'word/value fibre')
        for k in (3,4,5):
            check(count_progressions(H,k)==entry['positive_ap_counts'][str(k)],'direct tuple count')
            direct+=1
    gap_count=0
    def descend(a,depth):
        nonlocal gap_count
        H=sums(a)
        check(len(H)==2**len(a),'gap binary collision')
        check(count_progressions(H,5)==0,'gap arithmetic obstruction')
        check(all(x>=y for x,y in zip(a,weights(len(a)))),'gap minimality')
        gap_count+=1
        if depth==7:return
        for g in (1,2,3):
            nxt=a[0]+g if len(a)==1 else a[-1]+2*sum(a[:-1])+g
            descend(a+[nxt],depth+1)
    for start in (1,2):descend([start],1)
    check(gap_count==report['gap_and_dyadic_checks']['gap_cases']==2186,'gap domain coverage')
    return {'direct_integer_ap_counts':direct,'direct_pell_max_n':11,'gap_cases':gap_count}


def matrix_checks():
    cases=0
    for r in range(2,9):
        for n in range(1,26):
            a=[2**i for i in range(r)]
            while len(a)<n:a.append(2*a[-1]+a[-r])
            a=a[:n]
            D=[[int(i==j)-2*int(i==j-1)-int(j>=r and i==j-r)
                for j in range(1,n)] for i in range(n)]
            check(all(sum(a[i]*D[i][j] for i in range(n))==0 for j in range(n-1)),
                  'full incidence row not in arithmetic kernel')
            # Lower-row minor is upper triangular with literal unit diagonal.
            minor=D[1:]
            check(all(minor[i][i]==1 for i in range(n-1)), 'unimodular minor diagonal')
            check(all(minor[i][j]==0 for i in range(n-1) for j in range(i)),
                  'unimodular minor triangularity')
            if r==2:
                W=sum(x*x for x in a)
                sec=[Fraction(x,W) for x in a]
                check(sum(x*y for x,y in zip(sec,a))==1,'metric section')
                gram=[[sum(D[i][j]*D[i][l] for i in range(n))
                       for l in range(n-1)] for j in range(n-1)]
                expected=[[(5 if j==0 else 6) if j==l else (-1 if abs(j-l)==2 else 0)
                           for l in range(n-1)] for j in range(n-1)]
                check(gram==expected,'complete boundary Gram')
            cases+=1
    return {'delays':[2,8],'max_length':25,'full_relation_matrix_cases':cases}


def mutations(report):
    funcs=[]
    def missing_edge(r):r['graphs'][2]['edges'].pop()
    def zero_terminal(r):r['graphs'][1]['accepting']=[]
    def bad_carrier(r):r['scalar_carries'][0]=[0,1]
    def repeated_motif(r):r['seven_ap_motif']['masks'][3]=24
    def erase_alias(r):r['seven_ap_motif']['delay_two_alias']['pushed_words'][3][2]=1
    def bad_gf(r):r['four_ap_generating_function']['denominator'][3]=0
    def bad_count(r):r['graphs'][1]['positive_ap_counts_n0_through40'][2]=0
    def bad_primitive(r):r['seven_ap_motif']['second_difference_primitives'][0][0]+=1
    funcs=[missing_edge,zero_terminal,bad_carrier,repeated_motif,erase_alias,bad_gf,bad_count,bad_primitive]
    rejected=[]
    for f in funcs:
        corrupted=copy.deepcopy(report);f(corrupted)
        try:core(corrupted)
        except (AssertionError,KeyError,IndexError):rejected.append(f.__name__)
        else:raise AssertionError('corruption not rejected: '+f.__name__)
    return rejected


def algebraic_prefix_audit(report):
    records=[]
    for r in range(2,7):
        delta=Fraction(2,(r-1)*(r-1)*(3*r-2))
        B=Fraction((r-1)*(r+2),r*delta*delta)
        cutoff=B*2**r*3**(r-2)/delta
        C=-(-cutoff.numerator//cutoff.denominator)
        weights_r=[1]
        for j in range(1,7):weights_r.append(2*weights_r[-1]+(weights_r[j-r] if j>=r else 0))
        total=zero=prefixes=0;digest=hashlib.sha256()
        for n in range(7):
            for word in product(range(-2,3),repeat=n):
                total+=1
                if sum(word[j]*weights_r[j] for j in range(n))!=0:continue
                zero+=1;history=[]
                for h in range(1,n+1):
                    # Long divide the original high-prefix polynomial, not Horner multiplication.
                    coefficients=list(word[n-h:])+[0]*max(0,r-h)
                    for j in range(len(coefficients)-1,r-1,-1):
                        c=coefficients[j];coefficients[j]=0
                        coefficients[j-1]+=2*c;coefficients[j-r]+=c
                    remainder=tuple(coefficients[:r])
                    check(all(abs(v)<=C for v in remainder),'general coefficient carrier')
                    history.append(remainder)
                prefixes+=len(history)
                digest.update((repr((word,history))+"\n").encode())
        records.append({"delay":r,"coefficient_bound":2,"max_word_length":6,
                        "delta":str(delta),"coefficient_cutoff":C,"words":total,
                        "scalar_zero_words":zero,"zero_word_prefixes":prefixes,
                        "transcript_sha256":digest.hexdigest()})
    check(records==report['all_delay_algebraic_carrier'],'all-delay independent polynomial audit')
    return {"delays":[2,6],"max_word_length":6,"coefficient_alphabet":[-2,2],
            "words_screened":sum(d['words'] for d in records),
            "scalar_zero_words":sum(d['scalar_zero_words'] for d in records),
            "prefix_remainders":sum(d['zero_word_prefixes'] for d in records)}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--receipt',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();raw=args.receipt.read_bytes();report=json.loads(raw)
    producer=Path(__file__).with_name('verify_recurrence_control.py')
    check(hashlib.sha256(producer.read_bytes()).hexdigest()==report['validator_sha256'],'producer source hash')
    core(report)
    result={'schema':'ep817-recurrence-independent-audit-v1','status':'PASS','lean_checked':False,
            'method':'Separate program; complete edge re-enumeration, exact observation, direct pair counts and matrix checks.',
            'arithmetic':independent_arithmetic(report),'matrices':matrix_checks(),
            'all_delay_algebraic_carrier':algebraic_prefix_audit(report),
            'mutations_rejected':mutations(report),'receipt_sha256':hashlib.sha256(raw).hexdigest(),
            'auditor_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','output':str(args.output),'mutations':len(result['mutations_rejected'])}))

if __name__=='__main__':main()
