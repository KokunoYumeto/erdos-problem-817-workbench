"""Small independent exact checks for the reviewed separation and stability steps."""
import argparse,json
from itertools import product,groupby
from pathlib import Path

def require(x,msg):
    if not x:raise AssertionError(msg)
def incidence(Y,R):return sum(all(y+r in Y for r in R) for y in Y)
def mm(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def identity(n):return [[int(i==j) for j in range(n)] for i in range(n)]

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    P={0,3};Q=3;L=7;Y=P|{L-x for x in P};R={0,1}
    require(L>2*Q and incidence(Y,R)==1 and incidence(P,R)==0,'small delivered-threshold counterexample')
    sep=0
    for Q in range(7):
        for mask in range(1,1<<(Q+1)):
            P={i for i in range(Q+1) if mask>>i&1}
            L=3*Q+1;Y=P|{L-x for x in P}
            for rmask in range(1,1<<(Q+1),2):
                R={i for i in range(Q+1) if rmask>>i&1};V={max(R)-r for r in R}
                require(incidence(Y,R)==incidence(P,R)+incidence(P,V),'corrected separation identity')
                sep+=1
    A=[[3,7,0,0,0,0,0],[2,8,0,0,0,0,0],[1,9,0,0,0,0,0],[1,9,0,0,0,0,0],[0,10,0,0,0,0,0],[0,10,0,0,0,0,0],[0,10,0,0,0,0,0]]
    B=[[0,2,0,3,0,0,0],[0,4,0,6,0,0,0],[0,1,0,4,0,0,0],[0,3,0,7,0,0,0],[0,4,0,6,0,0,0],[0,3,0,7,0,0,0],[0,2,0,8,0,0,0]]
    v=[1,2,2,3,2,3,4];count=0
    for n in range(1,11):
        for w in product((0,1),repeat=n):
            M=identity(7)
            for d in w:M=mm(M,(A,B)[d])
            N=sum(a*b for a,b in zip(M[0],v))
            if len(set(w))==1:bad=n
            else:
                start=next(i for i in range(n) if w[i]==0 and w[i-1]==1)
                u=w[start:]+w[:start]
                runs=[(symbol,len(list(g))) for symbol,g in groupby(u)]
                aa=[length for symbol,length in runs if symbol==0]
                bb=[length for symbol,length in runs if symbol==1]
                bad=sum(aa[(i+1)%len(aa)]+b for i,b in enumerate(bb) if (aa[(i+1)%len(aa)],b)!=(2,1))
            require(N**6>=893**(2*(n-bad))*93**(3*bad),'exact stability lower inequality')
            require(N**3<=64*893**(n-bad)*1000**bad,'exact stability upper inequality')
            count+=1
    result={'status':'PASS','coefficient_domain':'Z; integer powers, no floats','separation_counterexample':{'Q':3,'P':[0,3],'L':7,'R':[0,1],'actual_incidence':1,'claimed_sum':0},'corrected_separation':'L>3Q ensures every cross-component distance exceeds Q','finite_separation_cases':sep,'scope':'Q=0..6, all nonempty P in [0,Q], all R containing0, L=3Q+1; all binary schedules length1..10','stability_words':count,'non_claims':['Finite tests do not substitute for the universal written separation or run-factorization proofs.']}
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
if __name__=='__main__':main()
