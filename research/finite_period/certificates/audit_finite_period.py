#!/usr/bin/env python3
"""Independent audit: interpolate carriers from actual numerical joins.

Imports no producer or producer helper. Full word enumeration uses receiving
column vectors rather than the producer's prefix rows. Fractions are exact.
"""
from pathlib import Path
import json,sys,hashlib,copy
from fractions import Fraction
from itertools import combinations,product
from collections import defaultdict


def check(b,m):
    if not b:raise AssertionError(m)


def sums(A,q):
    out={0}
    for a in A:
        nxt=set(out)
        for j in range(1,q):nxt.update(x+j*a for x in out)
        out=nxt
    return out

SH=((0,),(0,1),(0,2),(0,1,2),(0,3),(0,1,3),(0,1,2,3))

def obs(S):return tuple(len(set().union(*(set(x+r for x in S) for r in R))) for R in SH)


def invert(M):
    n=len(M);a=[[Fraction(x) for x in row]+[Fraction(int(i==j)) for j in range(n)] for i,row in enumerate(M)]
    for i in range(n):
        p=next((p for p in range(i,n) if a[p][i]),None)
        if p is None:return None
        a[i],a[p]=a[p],a[i];d=a[i][i];a[i]=[x/d for x in a[i]]
        for j in range(n):
            if j!=i:
                d=a[j][i];a[j]=[x-d*y for x,y in zip(a[j],a[i])]
    return [r[n:] for r in a]


def basis():
    selected=[];rows=[]
    def rank(a):
        a=[[Fraction(x) for x in row] for row in a];i=0
        for j in range(7):
            p=next((p for p in range(i,len(a)) if a[p][j]),None)
            if p is None:continue
            a[i],a[p]=a[p],a[i];d=a[i][j];a[i]=[x/d for x in a[i]]
            for k in range(i+1,len(a)):
                d=a[k][j];a[k]=[x-d*y for x,y in zip(a[k],a[i])]
            i+=1
        return i
    for width in range(0,20):
        pairs=[{j,width-j} for j in range((width+2)//2)]
        for bits in range(1<<len(pairs)):
            Y=set().union(*(pairs[i] for i in range(len(pairs)) if bits>>i&1))
            if not Y:continue
            v=obs(Y)
            if rank(rows+[v])>len(rows):rows.append(v);selected.append(sorted(Y))
            if len(rows)==7:return selected,rows
    raise AssertionError('no original-set basis')


def interpolate(A,b,B,I):
    D=sums(A,5);result=[]
    O=[obs({d+b*y for d in D for y in Y}) for Y in B]
    for j in range(7):
        row=[sum(I[i][k]*O[k][j] for k in range(7)) for i in range(7)]
        check(all(x.denominator==1 and x>=0 for x in row),'nonintegral interpolated carrier')
        result.append(tuple(int(x) for x in row))
    return tuple(result)


def apply(M,x):return tuple(sum(a*b for a,b in zip(row,x)) for row in M)

def word_count(Ms,w):
    x=(1,2,2,3,2,3,4)
    for a in reversed(w):x=apply(Ms[ord(a)-65],x)
    return x[0]


def root_cmp(a,d,n,b,e,m):
    l=a**m*e**n;r=b**n*d**m
    return (l>r)-(l<r)


def test_root(r):
    a,d,n=r['image_count'],r['denominator'],r['generator_reward'];lo,hi=map(Fraction,r['root_interval'])
    check(lo**n<=Fraction(a,d)<=hi**n,'incorrect outward algebraic interval')
    check(hi-lo==Fraction(1,1<<36),'unexpected precision grid')


def audit(data,full=True):
    Bs,V=basis();I=invert(V);check(I is not None,'singular actual-set basis');scope={};direct=0
    check(len(data['tables'])==3,'missing dictionary')
    for table in data['tables']:
        check(table['q']==5,'changed arity')
        D=[(d['radix'],tuple(d['weights'])) for d in table['dictionary']]
        Ms=[interpolate(A,b,Bs,I) for b,A in D]
        check([[list(r) for r in M] for M in Ms]==table['matrices'],'carrier differs from original sets')
        for b,A in D:
            check(len(set(A))==len(A) and min(A)>0 and sum(A)<b,'canonical source corrupted')
            vals=sums(A,2)
            for x in range(b):
                for d in range(1,b):check(not all((x+j*d)%b in vals for j in range(5)),'invalid binary modular source')
        expected={'radix_ten':20,'unequal_rewards':9,'mixed_rank':8}[table['name']]
        check(len(table['records'])==expected,'incomplete finite dictionary domain')
        states={((1,2,2,3,2,3,4),0):1}
        for m,rec in enumerate(table['records'],1):
            check(rec['length']==m and rec['literal_words']==len(D)**m,'incorrect original word domain')
            for key,den in [('lower',4),('upper',1)]:
                row=rec[key];check(len(row['word'])==m,'missing literal word')
                n=sum(len(D[ord(a)-65][1]) for a in row['word'])
                check(row['generator_reward']==n and row['denominator']==den,'reward or original cut denominator changed')
                check(word_count(Ms,row['word'])==row['image_count'],'word is not a witness for its count')
                test_root(row)
            if full:
                new=defaultdict(int)
                for (x,n),mult in states.items():
                    for (_,A),M in zip(D,Ms):new[(apply(M,x),n+len(A))]+=mult
                states=new;check(sum(states.values())==len(D)**m,'column enumeration lost source words')
                for (x,n),mult in states.items():
                    for name,den in [('lower',4),('upper',1)]:
                        r=rec[name]
                        check(root_cmp(x[0],den,n,r['image_count'],den,r['generator_reward'])>=0,'record is not a complete minimum')
            if table['name']=='radix_ten':
                q,r=divmod(m,3)
                predicted=13 if m==1 else (893**q if r==0 else (93**2*893**(q-1) if r==1 else 93*893**q))
                check(rec['upper']['image_count']==predicted,'finite-length theorem mismatch')
        for m in range(1,4):
            for w in product(range(len(D)),repeat=m):
                P=1;A=[]
                for a in w:
                    b,B=D[a];A.extend(P*x for x in B);P*=b
                actual=len(sums(A,5));word=''.join(chr(65+a) for a in w)
                check(actual==word_count(Ms,word),'direct generator/carry mismatch');direct+=1
        scope[table['name']]={'maximum_length':expected,'final_word_coverage':len(D)**expected,'independent_column_states':len(states) if full else None}
    check(data['cut_checks']['matrix_cases']==120 and data['cut_checks']['full_join_cases']==600,'cut scope mismatch')
    check(len(data['finite_minimum_formula']['attainers'])==101,'incomplete exact finite-length data')
    D=[(10,(1,3)),(10,(2,4))];Ms=[interpolate(A,b,Bs,I) for b,A in D]
    for m,w,v in data['finite_minimum_formula']['attainers']:
        check(len(w)==m and word_count(Ms,w)==v,'long symbolic word witness failed')
    for record in data['controllers']:
        s=record['vertices'];edges=record['edges'];p,d=record['cycle_rate_power']
        for r in record['records']:
            cur=r['start']
            for a in r['word']:
                es=[e for e in edges if e[0]==cur and e[2]==ord(a)-65];check(len(es)==1,'invalid controller edge');cur=es[0][1]
            check(cur==r['end'],'controller endpoint changed')
            for a in r['bridge']:
                es=[e for e in edges if e[0]==cur and e[2]==ord(a)-65];check(len(es)==1,'invalid closing edge');cur=es[0][1]
            check(cur==r['start'] and len(r['bridge'])<s,'return bridge failed')
            check(word_count(Ms,r['word']+r['bridge'])==r['closed_count'],'closed image count failed')
            check(root_cmp(r['image_count'],4,2*r['length'],p,1,d)<=0,'controller lower bound')
            check(root_cmp(p,1,d,r['closed_count'],1,r['closed_reward'])<=0,'controller upper bound')
    # Independently enumerate the inverse-count sums.
    values={0:[1]}
    for m in range(1,8):values[m]=[word_count(Ms,''.join(w)) for w in product('AB',repeat=m)]
    Z={(p,m):sum((Fraction(1,x**p) for x in values[m]),Fraction()) for p in (1,2,3) for m in values}
    for r in data['pressure']['records']:
        p,m,n=r['s'],r['m'],r['n'];actual=Z[p,m+n]/(Z[p,m]*Z[p,n])
        check(actual==Fraction(r['ratio']) and 1<=actual<=4**p,'pressure coefficient mismatch')
    return {'original_test_sets':Bs,'dictionaries':scope,'direct_generator_words':direct,'pressure_checks':len(data['pressure']['records']),'controller_paths':sum(len(x['records']) for x in data['controllers'])}


def main():
    source=Path(__file__).with_name('finite_period_receipt.json');data=json.loads(source.read_text());result=audit(data)
    mutations=[]
    for case in range(8):
        bad=copy.deepcopy(data)
        if case==0:bad['tables'][0]['matrices'][0][0][0]+=1
        elif case==1:bad['tables'][0]['records'][0]['lower']['denominator']=1
        elif case==2:bad['tables'][1]['records'][0]['upper']['generator_reward']+=1
        elif case==3:bad['tables'][0]['records'].pop()
        elif case==4:bad['tables'][0]['records'][0]['upper']['root_interval']=['0','1']
        elif case==5:bad['finite_minimum_formula']['attainers'][-1][2]+=1
        elif case==6:bad['controllers'][0]['records'][0]['bridge']=''
        else:bad['pressure']['records'][0]['ratio']='0'
        try:audit(bad,full=False)
        except (AssertionError,ValueError,KeyError):mutations.append(case)
        else:raise AssertionError('mutation escaped '+str(case))
    result.update({'schema':'ep817-finite-period-independent-v1','status':'PASS','producer_imported':False,'lean_checked':False,'mutations_rejected':mutations,'receipt_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'auditor_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    out=Path(__file__).with_name('independent_audit.json');out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(out.read_text())
if __name__=='__main__':main()
