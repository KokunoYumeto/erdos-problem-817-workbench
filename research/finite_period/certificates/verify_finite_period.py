#!/usr/bin/env python3
"""Generate exact finite arithmetic certificates for the finite-period theorem."""
from pathlib import Path
import sys,json,hashlib,argparse
from itertools import combinations,product
from fractions import Fraction
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from finite_period import *


def cut_checks():
    count=0;max_ratio=Fraction(1);digest=sha256();cases=0
    for q in range(2,7):
        for A in [(1,),(2,),(1,2),(1,3),(2,5),(1,3,4)]:
            for b in range(sum(A)+1,sum(A)+5):
                M=matrix(A,b,q);Rs=shapes(q);D=image(A,q);cases+=1
                for Y in [(0,),(0,1),(0,2),(0,1,4,5),(0,2,7,9)]:
                    target=tuple(sorted({d+b*y for d in D for y in Y}))
                    v=[len({y+r for y in Y for r in R}) for R in Rs]
                    observed=tuple(sum(a*c for a,c in zip(row,v)) for row in M)
                    direct=tuple(len({t+r for t in target for r in R}) for R in Rs)
                    require(observed==direct,'full shift observation mismatch')
                    require(len(target)<=len(D)*len(Y)<=(q-1)*len(target),'cut fibre inequality failed')
                    fibers={}
                    for d in D:
                        for y in Y:fibers.setdefault(d+b*y,[]).append((d,y))
                    require(max(map(len,fibers.values()))<=q-1,'original fibre bound failed')
                    max_ratio=max(max_ratio,Fraction(len(D)*len(Y),len(target)))
                    digest.update((repr((q,A,b,Y,direct))+'\n').encode());count+=1
    return {'matrix_cases':cases,'full_join_cases':count,'maximum_pair_to_value_ratio':str(max_ratio),'transcript_sha256':digest.hexdigest()}


def symbolic_finite_minima():
    D=[(10,(1,3)),(10,(2,4))];out=[]
    for m in range(0,101):
        word=attaining_word(m);v,n=word_value(D,word,5)
        require(len(word)==m and n==2*m and v==radix_ten_minimum(m),'attaining block formula')
        if m>=2:
            require(radix_ten_minimum(m+3)==893*v,'length-three recurrence')
        out.append([m,word,v])
    inequalities=[]
    for L in range(4,101):
        t=(8*10**L+37)//9;old=(8*10**(L-2)+37)//9
        require(t>93*old,'run splitting inequality')
        inequalities.append([L,t-93*old])
    require(93**3>893**2,'two/three-part replacement inequality')
    C2,_=actual_generators(D,(1,0));C3,_=actual_generators(D,(1,0,0))
    require(C2==(2,4,10,30) and C3==(2,4,10,30,100,300),'original macro generators')
    require(image(C2,5)==tuple(range(0,185,2)),'BA exact digit set')
    require(image(C3,5)==tuple(range(0,1785,2)),'BAA exact digit set')
    return {'through_length':100,'attainers':out,'run_difference_checks':inequalities,'BA_generators':list(C2),'BAA_generators':list(C3),'BA_image_count':93,'BAA_image_count':893}


def pressure_checks():
    D=[(10,(1,3)),(10,(2,4))];q=5;Ms=[matrix(A,b,q) for b,A in D];v=[len(R) for R in shapes(q)];e=(1,0,0,0,0,0,0)
    counts={0:[1]};rows=[e]
    for m in range(1,8):
        rows=[row_times(x,M) for x in rows for M in Ms];counts[m]=[sum(a*b for a,b in zip(x,v)) for x in rows]
    out=[]
    for s in (1,2,3):
        Z={m:sum((Fraction(1,n**s) for n in values),Fraction()) for m,values in counts.items()}
        for m in range(1,5):
            for n in range(1,8-m):
                ratio=Z[m+n]/(Z[m]*Z[n]);require(1<=ratio<=4**s,'partition multiplication')
                out.append({'s':s,'m':m,'n':n,'ratio':str(ratio)})
    return {'partition_sum_checks':len(out),'records':out}


def graph_checks():
    D=[(10,(1,3)),(10,(2,4))]
    # Strict alternating controller and the 3-cycle ABB; these retain the starting vertex.
    graphs=[('alternation',2,[(0,1,0),(1,0,1)],(93,4)),('ABB',3,[(0,1,0),(1,2,1),(2,0,1)],(933,6))]
    result=[]
    for name,s,edges,expected in graphs:
        rec=[]
        for m in range(1,13):
            paths=[(i,i,'') for i in range(s)]
            for _ in range(m):paths=[(start,t,word+chr(65+label)) for start,end,word in paths for u,t,label in edges if u==end]
            best=min((word_value(D,w,5)[0],st,en,w) for st,en,w in paths)
            count,st,en,w=best;close='';cur=en
            while cur!=st:
                edge=next(e for e in edges if e[0]==cur);cur=edge[1];close+=chr(65+edge[2])
                require(len(close)<s,'bridge length bound')
            total,N=word_value(D,w+close,5)
            # Exact lower and explicit periodic-count upper enclosures of the known cycle rate.
            p,d=expected
            require(root_compare(count,4,2*m,p,1,d)<=0,'controller lower misses rate')
            require(root_compare(p,1,d,total,1,N)<=0,'controller upper misses rate')
            rec.append({'length':m,'start':st,'end':en,'word':w,'image_count':count,'bridge':close,'closed_count':total,'closed_reward':N})
        result.append({'name':name,'vertices':s,'edges':edges,'cycle_rate_power':[expected[0],expected[1]],'records':rec})
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=Path(__file__).with_name('finite_period_receipt.json'));a=p.parse_args()
    dictionaries=[('radix_ten',[(10,(1,3)),(10,(2,4))],20),('unequal_rewards',[(10,(1,3)),(10,(2,4)),(3,(1,))],9),('mixed_rank',[(3,(1,)),(5,(1,2)),(23,(1,3,4,7))],8)]
    tables=[]
    for name,D,depth in dictionaries:
        for b,A in D:require(modular_witness(A,b,5) is None,'binary modular certificate')
        report=finite_enclosures(D,5,depth);report['name']=name
        if name=='radix_ten':
            for rec in report['records']:
                require(rec['upper']['image_count']==radix_ten_minimum(rec['length']),'finite-word exact minimum failed')
                require(root_compare(rec['lower']['image_count'],4,rec['lower']['generator_reward'],893,1,6)<=0,'known optimum lower')
                require(root_compare(893,1,6,rec['upper']['image_count'],1,rec['upper']['generator_reward'])<=0,'known optimum upper')
        tables.append(report)
    report={'schema':'ep817-finite-period-v1','status':'PASS','lean_checked':False,'scope':'ordinary all-length proofs; exact stated finite replay','tables':tables,'cut_checks':cut_checks(),'finite_minimum_formula':symbolic_finite_minima(),'pressure':pressure_checks(),'controllers':graph_checks(), 'source_sha256':{str(Path(__file__).name):sha256(Path(__file__).read_bytes()).hexdigest(),'finite_period.py':sha256((Path(__file__).resolve().parents[1]/'tools/finite_period.py').read_bytes()).hexdigest()}}
    text=json.dumps(report,indent=2,sort_keys=True)+'\n';a.output.write_text(text);print(json.dumps({'status':'PASS','receipt':str(a.output),'bytes':len(text),'dictionary_word_counts_at_final_depth':{t['name']:t['records'][-1]['literal_words'] for t in tables},'cut_cases':report['cut_checks'],'pressure_checks':report['pressure']['partition_sum_checks']},indent=2))
if __name__=='__main__':main()
