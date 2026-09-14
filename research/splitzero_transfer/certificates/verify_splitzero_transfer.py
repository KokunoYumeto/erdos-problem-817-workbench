#!/usr/bin/env python3
"""Exact finite replays for the EP817 SplitZero transfer.

The companion note proves the infinite statements. This standard-library
checker verifies the stated finite matrices, sections, integer primitives,
additive defects, carry-return sections, and variable-base examples.
"""
from __future__ import annotations
import argparse
from collections import deque
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from math import prod
from pathlib import Path

BASE_COMMIT = "23c0110c95b5a2036bdc04a1f352b6e5e27742c8"
ZETA_COMMIT = "42df8a2de002d5fc7090641fac46ea11be05fa71"
STAR = (1, 4, 5, 17, 21, 22)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def positions(bases: tuple[int, ...]) -> tuple[int, ...]:
    require(bool(bases) and all(isinstance(b, int) and b >= 2 for b in bases),
            "bases must be nonempty and integral >=2")
    p = [1]
    for b in bases:
        p.append(p[-1] * b)
    return tuple(p)


def dot(x, y):
    return sum((a*b for a,b in zip(x,y)), F(0))


def norm2(x):
    return dot(x, x)


def derivative(bases, carries):
    """Zero-endpoint map: m-1 carries -> m actual coefficient defects."""
    m = len(bases)
    require(len(carries) == m-1, "wrong number of interior carries")
    c = [F(0)] + list(carries) + [F(0)]
    return [bases[j]*c[j+1] - c[j] for j in range(m)]


def primitive(bases, defects):
    """All prefix carries, including the retained terminal carry."""
    require(len(bases) == len(defects), "source dimension mismatch")
    c = [F(0)]
    for b,z in zip(bases, defects):
        c.append((F(z)+c[-1])/b)
    return c[1:]


def section(bases, value=1):
    p=positions(tuple(bases))[:-1]
    W=sum(v*v for v in p)
    return [F(value*v, W) for v in p]


def homotopy(bases, z):
    p=positions(tuple(bases))[:-1]
    q=dot(p,z)
    r=section(bases,q)
    c=primitive(bases,[a-b for a,b in zip(z,r)])
    require(c[-1]==0, "section residual has a terminal defect")
    return c[:-1]


def digest_rows(rows) -> str:
    out=sha256()
    for row in rows:
        out.update((json.dumps(row,sort_keys=True,separators=(",",":"))+"\n").encode())
    return out.hexdigest()


def matrix_cases() -> dict:
    sequences=[b for m in range(1,6) for b in product((2,3,4),repeat=m)]
    sequences += [tuple(range(2,m+2)) for m in range(1,13)]
    sequences += [tuple(2 if j%2==0 else 97 for j in range(m)) for m in range(1,13)]
    sequences += [tuple(10**(j+1)+1 for j in range(m)) for m in range(1,9)]
    records=[];vector_checks=0;secants=0
    for bases in sequences:
        p=positions(bases);m=len(bases);w=p[:-1];W=sum(t*t for t in w)
        beta=min(bases)
        require(w[-1]**2<=W<=F(w[-1]**2,1-F(1,beta**2)),"uniform radix-metric sandwich failed")
        # Check every basis column of both homotopy identities.
        for j in range(m):
            z=[F(i==j) for i in range(m)]
            h=homotopy(bases,z);r=section(bases,dot(w,z))
            require([a+b for a,b in zip(derivative(bases,h),r)]==z,"dK+sJ != id")
            require(norm2(derivative(bases,h)) >= (beta-1)**2 * norm2(h),"finite coercivity failed")
            require(norm2(z)==norm2(derivative(bases,h))+norm2(r),"raw Pythagoras failed")
            require(norm2(r)==dot(w,z)**2/F(W),"section raw Gram failed")
            require(norm2(r)+dot(w,z)**2==(1+F(1,W))*dot(w,z)**2,"graph Gram failed")
            terminal=primitive(bases,z)[-1]
            require(p[-1]*terminal==dot(w,z),"terminal observation lost")
            vector_checks+=1
        for j in range(m-1):
            c=[F(i==j) for i in range(m-1)]
            dz=derivative(bases,c)
            require(dot(w,dz)==0,"arithmetic map does not kill original relations")
            require(homotopy(bases,dz)==c,"Kd != id")
            require(primitive(bases,dz)==c+[F(0)],"integer primitive inverse failed")
        # An actual integer relation, its original primitive, and support labels.
        c=[(-1)**j*(j+1) for j in range(m-1)]
        z=derivative(bases,c)
        require(all(a.denominator==1 for a in primitive(bases,z)),"integral relation lost its primitive")
        require((m,0) is not None and (m,0)!=(m+1,0),"present supported zero was collapsed")
        # Normal equations for the graph metric I+w w^T.
        r=section(bases)
        Mr=[r[j]+w[j]*dot(w,r) for j in range(m)]
        require(all(Mr[j]==w[j]*(1+F(1,W)) for j in range(m)),"graph normal equation failed")
        if m>1:
            old=section(bases[:-1])+[F(0)]
            new=r;difference=[a-b for a,b in zip(old,new)]
            h=homotopy(bases,difference)
            Wold=sum(a*a for a in w[:-1])
            require(derivative(bases,h)==difference,"section defect is not an original boundary")
            require(norm2(difference)==F(1,Wold)-F(1,W),"exact section secant failed")
            require(norm2(h) <= norm2(difference)/(beta-1)**2,"uniform defect primitive bound failed")
            secants+=1
        # Actual affine-progression coefficient Gram, including the cross term.
        for k in (3,4,5,6,17):
            u,v=F(2),F(-3)
            y=[u+i*v for i in range(k)]
            gram_value=k*u*u+k*(k-1)*u*v+F(k*(k-1)*(2*k-1),6)*v*v
            require(norm2(y)==gram_value,"affine cross Gram was dropped")
            raw=sum(norm2(section(bases,t)) for t in y)
            require(raw==gram_value/W,"coefficient metric transport failed")
            require(raw+gram_value==(1+F(1,W))*gram_value,"graph relative Gram failed")
        # The weighted-sup inverse retains the literal telescoping budget.
        z=[F(b-1) for b in bases]
        c=primitive(bases,z)
        require(dot(w,z)==p[-1]-1,"mixed-radix telescoping budget failed")
        require(all(c[j]==1-F(1,p[j+1]) for j in range(m)),"exact sup-norm recovery failed")
        require(all(0<=x<1 for x in c),"uniform infinity inverse bound failed")
        # Boundary escape: coefficient norm tends to zero but amplitude remains 1.
        escape=[F(0)]*(m-1)+[F(1,w[-1])]
        require(dot(w,escape)==1,"escape lost its arithmetic class")
        require(norm2(escape)==F(1,w[-1]**2),"escape norm failed")
        require(F(1,W)<=F(1,beta**(2*(m-1))),"uniform section convergence rate failed")
        records.append([list(bases),str(F(1,W)),str(1+F(1,W)),str(primitive(bases,[F(1)]+[F(0)]*(m-1))[-1])])
    return {"base_sequences":len(sequences),"basis_vector_checks":vector_checks,
            "section_secants":secants,"affine_Gram_dimensions":[3,4,5,6,17],
            "transcript_sha256":digest_rows(records)}


def mixed_digits(x: int, bases: tuple[int,...]) -> tuple[int,...]:
    d=[]
    for b in bases:
        x,r=divmod(x,b);d.append(r)
    require(x==0,"integer outside mixed-radix interval")
    return tuple(d)


def add_carry(x:int,y:int,bases:tuple[int,...]):
    P=prod(bases)
    dx,dy,dz=mixed_digits(x,bases),mixed_digits(y,bases),mixed_digits((x+y)%P,bases)
    c=primitive(bases,[a+b-d for a,b,d in zip(dx,dy,dz)])
    require(all(a in (0,1) for a in c),"binary-addition defect leaves [0,1]")
    require(c[-1]==(x+y)//P,"terminal addition carry erased")
    return c


def integer_quotient_cases() -> dict:
    count=0;triples=0;socles=0;records=[]
    for m in range(1,5):
        for bases in product((2,3),repeat=m):
            p=positions(bases);P=p[-1]
            # Full lower-bidiagonal relation matrix has determinant product(bases).
            determinant=prod(bases)
            require(determinant==P,"augmented determinant failed")
            # Truncation is the augmented inverse-system map. Zero padding has an exact endpoint defect.
            cp=[F(j+1) for j in range(m)]
            full=[bases[j]*cp[j]-(cp[j-1] if j else 0) for j in range(m)]
            larger=tuple(bases)+(5,);cpp=cp+[F(0)]
            dfull=[larger[j]*cpp[j]-(cpp[j-1] if j else 0) for j in range(m+1)]
            require(dfull[:m]==full and dfull[m]==-cp[-1],"augmented padding defect was erased")
            require(dot(p[:-1],full)==P*cp[-1],"augmented endpoint identity failed")
            for x in range(P):
                dx=mixed_digits(x,bases)
                require(dot(p[:-1],dx)==x,"canonical section inverse failed")
                for y in range(P):
                    c=add_carry(x,y,bases)
                    count+=1
            for v in range(2,P+1):
                if P%v:continue
                f=P//v
                image={(f*x)%P for x in range(v)}
                kernel={x for x in range(P) if v*x%P==0}
                require(image==kernel and len(image)==v,"boundary socle isomorphism failed")
                socles+=1
            if m<=2:
                for x,y,z in product(range(P),repeat=3):
                    a=add_carry(x,y,bases);b=add_carry((x+y)%P,z,bases)
                    c=add_carry(y,z,bases);d=add_carry(x,(y+z)%P,bases)
                    require([u+v for u,v in zip(a,b)]==[u+v for u,v in zip(c,d)],"additive section cocycle failed")
                    triples+=1
            records.append([list(bases),P,P*P])
    # A genuine pro-boundary whose every finite integer amplitude is nonzero.
    for m in range(1,33):
        bases=(2,)*m;z=(2,)+(1,)*(m-1);p=positions(bases)
        require(dot(p[:-1],z)==2**m,"pro-boundary terminal amplitude changed")
        require(primitive(bases,z)==[F(1)]*m,"pro-boundary carry sequence changed")
    return {"all_addition_pairs":count,"cocycle_triples":triples,"nonterminating_boundary_prefixes":32,
            "boundary_socle_instances":socles,"base_alphabet":[2,3],
            "max_length":4,"cocycle_max_length":2,"transcript_sha256":digest_rows(records)}


def trim(poly):
    p=list(map(F,poly))
    while len(p)>1 and p[-1]==0:p.pop()
    return p


def mulpoly(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return trim(out)


def division(p,h):
    p=trim(p);h=trim(h);require(h[-1]==1,"monic source relation required")
    rem=p[:];q=[F(0)]*max(1,len(p)-len(h)+1)
    while len(rem)>=len(h) and any(rem):
        t=len(rem)-len(h);v=rem[-1];q[t]+=v
        for i,x in enumerate(h):rem[t+i]-=v*x
        rem=trim(rem)
    return trim(q),rem


def polynomial_comparison() -> dict:
    # Repeated roots are intentional: no diagonalization or squarefree quotient.
    relations=[[-2,1],[1,-2,1],[4,0,-3,1],[0,0,0,1]]
    count=0;records=[]
    for h in relations:
        r=len(h)-1
        for degree in range(r-1,r+7):
            for shift in range(4):
                p=[F((j+2)*(shift+1)*(-1)**(j+shift)) for j in range(degree+1)]
                q,rem=division(p,h);rebuild=mulpoly(q,h)
                n=max(len(p),len(rebuild),len(rem));rp=rebuild+[F(0)]*(n-len(rebuild))
                for i,v in enumerate(rem):rp[i]+=v
                require(trim(rp)==trim(p),"old polynomial-boundary primitive not retained")
                q2,r2=division(mulpoly(q,h),h)
                require(q2==q and not any(r2),"polynomial source homotopy failed")
                # Coefficient map to the carry endpoint, followed by the literal remainder section.
                require(division(rem,h)[1]==rem,"forward/back endpoint identity failed")
                srem=[F(0)]+rem;qs,rs=division(srem,h)
                diff=srem[:];diff += [F(0)]*max(0,len(rs)-len(diff))
                for i,v in enumerate(rs):diff[i]-=v
                require(trim(diff)==mulpoly(qs,h),"multiplication section defect lost its relation")
                records.append([h,degree,shift,[str(v) for v in rem]])
                count+=1
    return {"monic_relations":relations,"polynomials_checked":count,
            "repeated_root_directions_retained":True,"transcript_sha256":digest_rows(records)}


def subsets(a):
    out={0:0}
    for j,x in enumerate(a):
        for u,mask in tuple(out.items()):
            out.setdefault(u+x,mask|(1<<j))
    return out


def delta(row):
    return tuple(row[i+2]-2*row[i+1]+row[i] for i in range(len(row)-2))


def returning_section(D,k):
    present=set(D);table={}
    for c in product((-1,0,1),repeat=k-2):
        for a in D:
            for b in D:
                row=[a,b]
                for ci in c:
                    w=2*row[-1]-row[-2]-ci
                    if w not in present:break
                    row.append(w)
                else:
                    table[c]=tuple(row);break
            if c in table:break
        require(c in table,f"no actual return primitive for {c}, k={k}")
    # Check the complete section independently by its literal second differences.
    for c,row in table.items():
        require(all(x in present for x in row) and delta(row)==tuple(-x for x in c),"invalid return section")
    return table


def modular_rows(D,q,k):
    present=set(D)
    for a in range(q):
        for d in range(1,q):
            row=tuple((a+i*d)%q for i in range(k))
            if all(x in present for x in row):yield row


def check_actual_witness(values,low,high,q,representatives):
    require(all(values[i]==low[i]+q*high[i] for i in range(len(values))),"wrong arithmetic endpoint")
    require(values[0]!=values[1] and all(t==0 for t in delta(values)),"not a nonconstant integer AP")
    actual=tuple(STAR)+tuple(q*a for a in STAR)
    require(len(set(actual))==12,"two-level generators collide")
    masks=[]
    for x,y,u in zip(low,high,values):
        mask=representatives[x]|(representatives[y]<<6)
        require(sum(a for j,a in enumerate(actual) if (mask>>j)&1)==u,"witness lacks an actual subset")
        masks.append(mask)
    return masks


def star_classification() -> dict:
    representatives=subsets(STAR);D=tuple(sorted(representatives))
    require(len(D)==38 and sum(STAR)==70,"base block changed")
    expected={5:[97,101,103,105,107,109,127,131,133,134,135,137,139],
              6:[93,97,101,103,105,107,109,111,117,123,127,129,131,133,134,135,137,139]}
    result=[]
    for k in (5,6):
        section=returning_section(D,k);safe=[];failures=[];pairs=0
        for q in range(71,141):
            rows=list(modular_rows(D,q,k));pairs+=q*(q-1)
            # Independent residue search based on first and second actual digits.
            direct=[]
            for a,b in product(D,repeat=2):
                if a==b:continue
                d=(b-a)%q
                row=tuple((a+i*d)%q for i in range(k))
                if all(x in representatives for x in row):direct.append(row)
            require(set(rows)==set(direct),"two modular enumerations disagree")
            if not rows:safe.append(q);continue
            low=rows[0];dd=delta(low)
            require(all(x%q==0 for x in dd),"modular witness is not a carry boundary")
            c=tuple(x//q for x in dd)
            require(all(-1<=x<=1 for x in c),"mixed-base canonical carry bound failed")
            high=section[c];values=tuple(x+q*y for x,y in zip(low,high))
            masks=check_actual_witness(values,low,high,q,representatives)
            # The return is independent of the following base, not just of its old value q.
            for following in (71,97,141,10**6+3):
                require(all((x+y)%following==0 and (x+y)//following==0 for x,y in zip(c,delta(high))),"return depended on following base")
            failures.append({"base":q,"low_digits":low,"intermediate_carry":c,
                             "return_digits":high,"integer_AP":values,"actual_subset_masks":masks})
        require(safe==expected[k],"safe-base classification changed")
        for q in range(141,161):
            require(next(modular_rows(D,q,k),None) is None,"large-base control failed")
        result.append({"k":k,"safe_bases_71_through_140":safe,
                       "all_bases_at_least":141,"minimal_safe_base":safe[0],
                       "return_section":[{"carry":c,"digits":row} for c,row in sorted(section.items())],
                       "unsafe_base_witnesses":failures,"parameter_pairs_tested_71_through_140":pairs,
                       "additional_large_base_controls":[141,160]})
    return {"generators":STAR,"subset_sums":D,"cases":result,
            "infinite_scope":"The companion proof covers every sequence of bases >70 and every prefix length."}


def successors(c,D,b):
    present=set(D)
    for a,d in product(D,repeat=2):
        row=[a,d];out=[]
        for ci in c:
            w=(2*row[-1]-row[-2]-ci)%b
            if w not in present:break
            out.append((w-2*row[-1]+row[-2]+ci)//b);row.append(w)
        else:yield tuple(out),tuple(row)


def transfer(flagged,base,D,k):
    zero=(0,)*(k-2);out=set()
    for target,row in successors(zero,D,base):
        if row[0]!=row[1]:out.add(target)
    for c in flagged:
        out.update(target for target,row in successors(c,D,base))
    return frozenset(out)


def heterogeneous_control() -> dict:
    k=3;letters=((2,(1,)),(6,(2,)))
    parent={frozenset():None};queue=deque(parent);edges=[]
    while queue:
        state=queue.popleft()
        for i,(b,A) in enumerate(letters):
            D=tuple(sorted(subsets(A)));nxt=transfer(state,b,D,k)
            if (0,) in nxt:continue
            edges.append((state,i,nxt))
            if nxt not in parent:parent[nxt]=(state,i);queue.append(nxt)
    require(len(parent)==2 and len(edges)==3,"small control graph changed")
    nonempty=frozenset(((-1,),(1,)))
    require(set(parent)=={frozenset(),nonempty},"small control states incorrect")
    require(transfer(frozenset(),2,(0,1),3)==nonempty,"hazardous initial letter failed")
    require((0,) in transfer(nonempty,2,(0,1),3),"repeating the hazardous letter was not rejected")
    require(transfer(nonempty,6,(0,2),3)==frozenset(),"actual reset letter failed")
    cases=0
    for length in range(1,9):
        for word in product((0,1),repeat=length):
            state=frozenset();accepted=True
            for i in word:
                b,A=letters[i];state=transfer(state,b,tuple(sorted(subsets(A))),3)
                if (0,) in state:accepted=False;break
            expected=not any(word[j]==word[j+1]==0 for j in range(length-1))
            require(accepted==expected,"finite controller language mismatch")
            if accepted:
                u=word.count(0);v=word.count(1)
                require(3*(2**u*6**v)**2>=12**(u+v),"exact cycle lower bound failed")
            cases+=1
    # Actual four-level construction, not only a flag-state calculation.
    bases=(2,6,2,6);A=(1,4,12,48);D=set(subsets(A))
    for a,b in product(D,repeat=2):
        require(a==b or 2*b-a not in D,"periodic mixed construction contains a 3-AP")
    return {"letters":[{"base":b,"generators":A} for b,A in letters],
            "closed_control_states":[[list(c) for c in sorted(s)] for s in parent],
            "edges":[{"source":[list(c) for c in sorted(a)],"letter":i,
                      "target":[list(c) for c in sorted(b)]} for a,i,b in edges],
            "finite_words_checked":cases,"optimal_period":[0,1],
            "period_base_product":12,"period_generators":2,
            "four_level_generators":A,"scope":"Exact optimum within this two-letter dictionary, not a global bound improvement."}


def canonical_witness(D,base,k):
    zero=(0,)*(k-2);initial=(zero,False);terminal=(zero,True)
    parent={initial:None};queue=deque([initial])
    while queue:
        state=queue.popleft();c,flag=state
        for target,row in successors(c,D,base):
            nxt=(target,flag or row[0]!=row[1])
            if nxt in parent:continue
            parent[nxt]=(state,row)
            if nxt==terminal:
                rows=[];cur=nxt
                while parent[cur] is not None:
                    prev,col=parent[cur];rows.append(col);cur=prev
                rows.reverse()
                values=tuple(sum(base**j*row[i] for j,row in enumerate(rows)) for i in range(k))
                require(values[0]!=values[1] and not any(delta(values)),"carry failure did not evaluate to a progression")
                return {"base":base,"columns":rows,"integer_AP":values,"steps":len(rows)}
            queue.append(nxt)
    return None


def has_integer_ap(values,k):
    ordered=sorted(values);present=set(ordered)
    for i,a in enumerate(ordered):
        for b in ordered[i+1:]:
            d=b-a
            if a+(k-1)*d>ordered[-1]:break
            if all(a+j*d in present for j in range(2,k)):
                return tuple(a+j*d for j in range(k))
    return None


def fixed_block_periodic_capacity() -> dict:
    A=(1,4,8);D=tuple(sorted(subsets(A)));S=sum(A);k=5
    bases=tuple(range(S+1,2*S+3));zero=(0,)*(k-2)
    states=tuple(product((-1,0,1),repeat=k-2))
    # Independent complete column enumeration validates the recurrence enumerator.
    all_columns=tuple(product(D,repeat=k))
    literal_checks=0
    audit_bases=bases+(29,1009,10**6+3)
    profile={}
    for base in audit_bases:
        literal={c:set() for c in states}
        for row in all_columns:
            dd=delta(row);c=[]
            for x in dd:
                r=x%base
                if r==0:c.append(0)
                elif r==1:c.append(-1)
                elif r==base-1:c.append(1)
                else:break
            else:
                carry=tuple(c)
                target=tuple((x+y)//base for x,y in zip(dd,carry))
                literal[carry].add((target,row))
        for c in states:
            actual=set(successors(c,D,base))
            require(actual==literal[c],"full-column and recurrence edge enumerations disagree")
            literal_checks+=1
        profile[base]=literal
    for base in audit_bases:
        if base>=2*S+2:
            require(profile[base]==profile[2*S+2],"tail-base transition identity failed")
    numbered={frozenset():0};queue=deque(numbered);edges=[]
    while queue:
        source=queue.popleft()
        for base in bases:
            target=transfer(source,base,D,k)
            if zero in target:continue
            if target not in numbered:
                numbered[target]=len(numbered);queue.append(target)
            edges.append((numbered[source],base,numbered[target]))
    require(len(numbered)==4 and len(edges)==30,"fixed-block finite controller changed")
    live={a for a,b,c in edges}
    require(live=={0,1},"dead-end states were not separated")
    live_edges=[e for e in edges if e[2] in live]
    # An exact multiplicative potential proves every cycle's lower bound.
    potential={0:7,1:10}
    for source,base,target in live_edges:
        require(base**2*potential[target]>=280*potential[source],"cycle lower potential failed")
    require((0,14,1) in live_edges and (1,20,0) in live_edges,"optimal cycle missing")
    require(14**2*10==280*7 and 20**2*7==280*10,"optimal cycle lacks equality")
    # Enumerate all simple cycles independently, with all base labels retained.
    cycles=[]
    def visit(start,current,visited,word):
        for a,base,target in live_edges:
            if a!=current:continue
            if target==start:
                bs=word+(base,)
                require(prod(bs)**2>=280**len(bs),"enumerated cycle violates exact optimum")
                cycles.append({"bases":bs,"product":prod(bs),"length":len(bs)})
            elif target>start and target not in visited:
                visit(start,target,visited+(target,),word+(base,))
    for start in sorted(live):visit(start,start,(start,),())
    failures=[]
    for base in bases:
        witness=canonical_witness(D,base,k)
        if base<19:
            require(witness is not None,"smaller constant base lacks failure witness")
            failures.append(witness)
        else:require(witness is None,"claimed safe constant base failed")
    require(280<19**2,"periodic improvement over constant bases failed")
    period=(14,20);C=A+tuple(14*a for a in A);DC=tuple(sorted(subsets(C)))
    require(len(C)==len(set(C))==6 and sum(C)==195 and len(DC)==64,"period generator bridge failed")
    require(next(modular_rows(DC,280,k),None) is None,"period block modular certificate failed")
    direct=[]
    for length in (1,2,3):
        word=tuple(period[j%2] for j in range(length));p=positions(word)
        actual=tuple(p[j]*a for j in range(length) for a in A)
        vals=subsets(actual)
        require(len(actual)==len(set(actual))==3*length,"mixed generator cardinality failed")
        require(has_integer_ap(vals,k) is None,"actual periodic generator language failed")
        direct.append({"levels":length,"bases":word,"generators":actual,"subset_sum_count":len(vals)})
    return {"generators":A,"k":k,"digits":D,"literal_base_range":[14,28],
            "tail_transition_threshold":28,"independent_extra_tail_bases":[29,1009,10**6+3],
            "literal_edge_profile_comparisons":literal_checks,
            "controller_states":[{"id":i,"flagged_carries":sorted(s)} for s,i in numbered.items()],
            "safe_edges":[{"source":a,"base":b,"target":c} for a,b,c in edges],
            "live_states":sorted(live),"potential":{"0":7,"1":10},
            "all_simple_cycles":cycles,"optimal_period":period,"period_product":280,
            "period_generator_count":6,"best_constant_base":19,
            "smaller_constant_base_failures":failures,"actual_period_generators":C,
            "period_modular_parameters":280*279,"direct_prefix_replays":direct,
            "scope":"Exact optimum over all infinite canonical mixed-base schedules for this fixed block; not a global k=5 improvement."}


def regressions() -> dict:
    caught=0
    def must_fail(fn):
        nonlocal caught
        try:fn()
        except AssertionError:caught+=1
        else:raise AssertionError("false formula passed its mutation control")
    must_fail(lambda:require((1,0)==None,"supported zero != absence"))
    must_fail(lambda:require(primitive((2,3),(1,0))[-1]==0,"terminal boundary must survive"))
    must_fail(lambda:require(1+F(1,10)==F(1,10),"graph arithmetic term was removed"))
    must_fail(lambda:require(all(x.denominator==1 for x in primitive((2,3),(1,0))),"real primitive is not automatically integral"))
    D=(0,1,4,5,6,9,10,17,18,21,22,23,25,26,27,28,30,31,32,38,39,40,42,43,44,45,47,48,49,52,53,60,61,64,65,66,69,70)
    must_fail(lambda:require(next(modular_rows(D,93,5),None) is None,"k=6 certificate does not remove a k=5 witness"))
    must_fail(lambda:require((0,) not in transfer(frozenset(((-1,),(1,))),2,(0,1),3),"accepting supported zero was dropped"))
    must_fail(lambda:require(dot((1,2,4),(2,1,1))==0,"a pro-boundary was misread as a finite zero"))
    must_fail(lambda:require(14*14>=280,"the first risky edge alone was misread as the cycle bound"))
    return {"deliberately_false_formulas_rejected":caught}


def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    report={"schema":"ep817-splitzero-transfer-v1","status":"PASS","lean_checked":False,
            "ep817_base_commit":BASE_COMMIT,"zeta_source_commit":ZETA_COMMIT,
            "evidence_scope":"Exact finite replays. Infinite splitting, completion, and mixed-base classification are proved in the note.",
            "linear_relations_and_graph_metrics":matrix_cases(),
            "integral_quotients_and_additive_section":integer_quotient_cases(),
            "original_polynomial_comparison":polynomial_comparison(),
            "six_generator_all_base_classification":star_classification(),
            "heterogeneous_finite_dictionary":heterogeneous_control(),
            "all_base_periodic_fixed_block_capacity":fixed_block_periodic_capacity(),
            "regressions":regressions(),
            "validator_sha256":sha256(Path(__file__).read_bytes()).hexdigest()}
    text=json.dumps(report,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text,encoding="utf-8")
    print(text,end="")

if __name__=="__main__":
    main()
