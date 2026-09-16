# A compact all-rank dual from the retained reset cost

Research continuation, 14 September 2026. This is an ordinary mathematical theorem with a complete proof. It does not evaluate the unrestricted Erdős 817 rate. The numerical calibrations below use the independently audited variable-block certificates; no new Lean elaboration is claimed.

## 1. The original infinite family and a finite set of coefficient variables

Fix k>=3. Retain every canonical level (b,A), where A is a finite set of distinct positive integers, S(A)<b and b>=2; the empty block is also an admitted present zero-digit level. Let C={-1,0,1}^(k-2). As in the companion proof, true-flag supports exclude carry zero. The separately present false state (0,false) is retained at every support. The level transfer is the literal union of its initial nonconstant-column targets and all targets of its incoming true carries.

Let S_k be the finite set of ALL safe supports invariant under c->-c and c->reverse(c). A support need not have been reached by a previously enumerated schedule to belong to S_k. The transfer preserves these symmetries. Write T_(b,A)(R) for the actual transfer, and keep an edge R->T only when T is safe. Every such edge retains the actual digit columns and their word fibers.

For d=k-2 put

\[
 a_d=\frac{3^d+3^{\lceil d/2\rceil}+1+3^{\lfloor d/2\rfloor}}4-1.
\]

Then |S_k|=2^(a_d): the nonzero carry orbits can independently be present or absent. In particular |S_5|=512 and |S_6|=2^24. This is a finite coefficient space independent of generator count, generator magnitudes, and schedule length. The arithmetic family of edges is still infinite.

## 2. Exact compact dual theorem

Let lambda_k be the original exponential rate, whose existence and finite-set formula are proved in the companion note. For every real u in [1,3], the following are equivalent:

\[
 \boxed{u\le\lambda_k}
\]

and the existence of a function H:S_k->[1,2] such that, for EVERY canonical level and EVERY safe edge,

\[
 \boxed{b\,H(T_{b,A}(R))\ge u^{|A|}\,H(R).}
 \tag{D1}
\]

Consequently

\[
 \boxed{\lambda_k=
 \max\left\{u\in[1,3]:\exists H\in[1,2]^{S_k}\text{ satisfying (D1) for all actual levels}\right\}.}
 \tag{D2}
\]

The interval [1,2] is a theorem furnished by the original reset cost. It is not a renormalization of a source metric, of the generator weights, or of the quotient. For a fixed u, (D1) is a family of linear inequalities in the finitely many coefficients H(R).

### Proof of necessity

Assume u<=lambda_k. Give an edge cost

\[
 w_u(b,A)=\log b-|A|\log u.
\]

Consider ANY finite safe path, even one starting at a support not known to be reachable from the initial support. By monotonicity, its same sequence of labels can be read safely from empty true support, with each actual support contained in the displayed support. Append the supported zero reset (2,empty). The resulting word sends empty true support back to empty. Repeating it therefore gives an admissible periodic schedule.

Let P be the original path's product of radices and N its generator reward. If N>0, the actual aggregated periodic generator block gives

\[
 \lambda_k\le(2P)^{1/N}.
\]

Since u<=lambda_k, the path cost obeys

\[
 \log P-N\log u\ge-\log2.
 \tag{D3}
\]

If N=0, its cost is the sum of positive log radices and also satisfies (D3). No negative cycle or infinitely long approximation has been discarded; (D3) bounds every finite safe path uniformly.

For each R define d(R) to be the infimum of costs of finite safe paths ending at R, allowing ANY starting vertex and the empty path of cost zero. Then

\[
 -\log2\le d(R)\le0.
\]

Appending an edge R->T to paths approaching d(R) gives

\[
 d(T)\le d(R)+\log b-|A|\log u.
\]

Set H(R)=exp(-d(R)). It belongs to [1,2], and exponentiating the last inequality proves (D1). The infimum need not be achieved by a finite path; the inequality follows by taking the infimum, and continuity of the exponential is sufficient.

### Proof of sufficiency

Assume (D1). Every admissible finite nonempty A has the modular-safe level (2S(A)+1,A). Its transfer from empty true support is empty. Apply (D1) to that self-edge and cancel the positive H(empty):

\[
 2S(A)+1\ge u^{|A|}.
\]

Taking the infimum over all such A and using the proved exact finite-set characterization gives lambda_k>=u. This proves both directions, including feasibility at u=lambda_k, and hence the maximum in (D2). Alternatively, multiplying (D1) on every finite path retains the full endpoint ratio and proves its construction-rate lower bound directly. QED.

## 3. Exact finite-rank potentials and an explicit failed extrapolation

The same path argument applies to the finite bounded-rank dictionary, because its supported reset remains available and its positive-reward optimum is attained periodically. At an algebraic target u=B^(1/p), one can retain rational potentials h=H^p satisfying

\[
 1\le h(R)\le2^p,\qquad
 b^p h(T)\ge B^{|A|}h(R).
 \tag{D4}
\]

The already independently audited eight variable-block certificates satisfy these inequalities on their full reachable state sets. The separate compact-dual checker verifies the bound 2^p on each actual rational coefficient and verifies (D4) on every retained source/target/reward cost representative. The preceding independent audits already verified every actual parallel label as well. Multiplication gives the uniform retained endpoint factor

\[
 (2P)^p\ge B^N
\]

for every safe path in those controllers.

For the rank-four result B=23,p=4, the claim u=23^(1/4) cannot be extended to all ranks. The six-generator modular certificate A={1,4,5,17,21,22}, b=97 at k=5 gives an empty-support self-edge. It would require

\[
 97^4\ge23^6,
\]

which is false because 97^2<23^3. At k=6, b=93 fails the same proposed inequality because 93^2<23^3. These are actual finite obstruction maps to an attempted all-rank potential, not a conclusion that other lower thresholds are impossible.

The reset factor cannot be omitted even in a finite certificate. For the rank-one target u=sqrt(8), the safe first level (2,{1}) has P=2,N=1, so P^2=4<8; appending the retained reset multiplies P by two and supplies the correct finite-path bound. No potential controls the cost of a path after dropping its endpoint or reset term.

## 4. Return to the general linear-pattern source

For the binary-rigid, translation-invariant integer matrix L in the companion Zeta note, the supported reset has radix R_L=max(2,max_i m_i). Replace 2 by R_L throughout the proof. A finite safe path followed by that actual reset produces a periodic L-admissible generator set, giving path cost at least -log R_L. The constructed coefficient function belongs to [1,R_L]. For the original lambda_L, the exact dual is

\[
 u\le\lambda_L
 \iff\exists H\in[1,R_L]^{S_L}:
 bH(T_{b,A}(Q))\ge u^{|A|}H(Q)
\]

on all safe supports and all actual canonical levels. Here S_L can be the full finite carry-support set; no AP-specific symmetry is assumed. The actual finite-set formula from the original product with radix MS(A)+1 proves the converse. The binary-obstruction case has no nonempty admissible generators and remains separately identified by its explicit witness.

This result supplies a compact, dimension-fixed coefficient formulation of the all-rank control problem. The infinitely many block inequalities still have to be controlled arithmetically. Nothing in the compactness argument evaluates their feasible maximum, bounds the original tensor-metric return for free, or proves a statement about the zeros of the Riemann zeta function.

## Sources and scope

The complete carry correspondence, original support conventions, reset, and finite-set rate formula are proved in the two companion notes. The source-metric and original-observation-kernel interfaces are those of the inspected Zeta reconstruction at commit 42df8a2de002d5fc7090641fac46ea11be05fa71. The shortest-path potential construction is classical in form; the uniform interval here is obtained from the retained arithmetic reset and the original extremal-rate characterization. No global literature-priority claim is made.
