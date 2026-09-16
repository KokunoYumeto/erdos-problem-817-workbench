# Canonical monotone potentials and compilation of arithmetic obstructions

Research continuation, 15 September 2026. This note continues the exact all-rank dual in the retained 14 September integration package. All statements below have ordinary proofs. The finite calibrations use the existing independently audited bounded-rank certificates; they are not new all-rank Lean checks.

## 1. The original support controller and the retained reset

Fix k>=3. A canonical arithmetic level is (b,A), with b>=2, A a finite set of distinct positive integers, and sum A<b. The empty block is allowed as a present zero-digit level. Its digit source has one actual word, not an absent object.

Let C_k={-1,0,1}^(k-2). A state R is a safe sign-and-reversal-invariant support of true-flag carries, so 0 does not belong to R. The separately present false state is (0,false). The actual column equation is

\[
bc'=c+\Delta d,\qquad \Delta d_i=d_i-2d_{i+1}+d_{i+2},\qquad d\in H(A)^k.
\]

The transfer T_(b,A)(R) is the union of all actual true-flag successors and all nonconstant successors of the false state. It is monotone under inclusion of R. Keep an edge only when its target is safe. Every edge retains its radix b, generator reward n=|A|, full source columns, and representation fibers.

The original level (2,empty) sends every safe true support to empty true support. Its only actual digit column is zero, so 2c'=c forces c=c'=0; no nonzero true carry survives. The false zero state survives. Its radix cost is two. Erasing that cost changes every subsequent generator and is not allowed.

The earlier exact finite-set characterization is

\[
\lambda_k=\inf_{A\ne\varnothing,\ k\text{-admissible}}
(2S(A)+1)^{1/|A|}.
\tag{1.1}
\]

A canonical modular-safe block is an empty-true-support self-edge. Every admissible A supplies such an edge at radix 2S(A)+1. These facts, and the represented path/AP correspondence, are proved in the predecessor notes and retained in this contribution's source inventory.

## 2. The greatest bounded subsolution is an explicit future value

For u>0 and a finite safe path p, retain its actual product P(p) of radices and total generator reward N(p). Define

\[
F_u(R)=\inf_{p\text{ finite safe starting at }R}\frac{P(p)}{u^{N(p)}}.
\tag{2.1}
\]

The empty path is included and has value one. There is no assumption that an infimum is attained. Every finite path has a strictly positive value.

**Theorem 2.1.** For every u in [1,3], the following statements hold.

If u<=lambda_k, then 1/2<=F_u(R)<=1 at every safe support. The coefficient function H_u=2F_u belongs to [1,2]^(S_k), is monotone under inclusion of supports, and satisfies the exact equation

\[
\boxed{H_u(R)=\min\left\{2,
\inf_{R\xrightarrow{(b,A)}T}\frac b{u^{|A|}}H_u(T)\right\}.}
\tag{2.2}
\]

It is the greatest nonnegative function bounded above by two that satisfies all original edge inequalities

\[
bH(T)\ge u^{|A|}H(R).
\tag{2.3}
\]

If u>lambda_k, then F_u(R)=0 at every safe support. In particular (2.2) has greatest bounded subsolution zero.

**Proof.** A finite path from an arbitrary safe R can be read from empty true support with the same labels, since every successor then remains contained in the original support. Append the actual reset. The resulting period is admissible, with product 2P(p) and reward N(p). If the reward is positive,

\[
\lambda_k\le(2P(p))^{1/N(p)}.
\]

For u<=lambda_k this gives P(p)/u^(N(p))>=1/2. Zero-reward paths have product at least one. Taking infima proves the bounds.

If R is a subset of T, every label path safe from T is safe from R, with unchanged cost. Therefore F_u(R)<=F_u(T). Separating empty paths from nonempty paths by their first edge proves (2.2), including the possibility that the inner infimum is not achieved. Positive multiplication commutes with these infima.

Let G take values in [0,2] and satisfy (2.3). Multiplication along any finite path gives

\[
G(R)\le\frac{P(p)}{u^{N(p)}}G(\operatorname{end}p)
\le2\frac{P(p)}{u^{N(p)}}.
\]

Infimizing proves G<=2F_u. The function 2F_u itself satisfies (2.2), so it is the greatest subsolution.

Finally, if u>lambda_k, (1.1) provides a literal modular-safe self-edge (q,A) with theta=q/u^(|A|)<1. From any R apply the reset and then repeat this edge h times. Its cost is 2theta^h, tending to zero. Thus F_u(R)=0. Every path in this sequence retains its positive numerical cost and actual source words. QED.

This is an exact dichotomy over all generator ranks, not an assumption about an unknown general lower estimate. It does not evaluate the threshold lambda_k.

## 3. A stronger form of the all-rank dual

The theorem gives the equivalent compact formulation

\[
\boxed{
\lambda_k=\max\{u\in[1,3]:\exists H:S_k\to[1,2],\
H\text{ is inclusion-monotone and satisfies (2.3) on all actual safe edges}\}.
}
\tag{3.1}
\]

Necessity uses H_u. For sufficiency, an admissible A has the modular-safe self-edge (2S(A)+1,A) at empty true support. Cancel its positive H(empty) in (2.3); then use (1.1). The same argument proves feasibility at u=lambda_k, so the maximum is attained.

The monotonicity is proved from future feasibility, rather than imposed on the earlier past-path construction. The coefficient interval still comes from the exact reset cost; no source Gram or arithmetic weight has been rescaled. The number of coefficients depends on k alone. The infinitely many actual block inequalities in (3.1) remain the arithmetic task.

When u>lambda_k, the limit H_u(R)=0 is a zero coefficient at the same admitted support. The coordinate observation R^S_k->R at that support sends the limiting vector to zero; it does not remove the false state or turn its label into external absence. This distinguishes a vanishing infimal cost from a missing source object. A finite violating arithmetic period, rather than the notation for that limit alone, is the useful obstruction certificate.

## 4. Compiling a low-cost path into an actual modular block

Suppose a finite safe path has

\[
2P(p)<u^{N(p)}.
\tag{4.1}
\]

Read its labels from empty true support and append the present zero reset. If its nonempty levels are (b_j,A_j), set

\[
C=\bigcup_jP_jA_j,\qquad Q=2P(p),
\]

where P_j is the retained product of all preceding radices, including empty levels. Canonical inequalities imply that the generators are distinct and |C|=N(p). Also

\[
S(C)\le\sum_jP_j(b_j-1)=P(p)-1<Q.
\]

The reset makes the whole period's true transfer empty. A nonconstant modular k-AP in H(C) modulo Q would give its nonconstant initial carry path through that period, contradicting the empty transfer. Hence (Q,C) is an actual modular-safe certificate. Inequality (4.1) gives

\[
\lambda_k\le Q^{1/|C|}<u.
\]

This is a typed compiler from a finite supported path to a finite arithmetic certificate and then to an infinite family of distinct integer generators. It preserves every intermediate radix and zero-word choice.

If a closed safe cycle has product P and positive reward N with P<u^N, it already produces an admissible periodic integer construction from empty true support by monotonicity. To obtain a modular certificate with the reset retained, repeat it any integer h with 2(P/u^N)^h<1 and then apply the compiler. At u=B^(1/p), the strict test is entirely integral:

\[
(2P^h)^p<B^{hN}.
\]

Conversely, u>lambda_k supplies such a low-cost path by repeating the self-edge used in the proof of Theorem 2.1. Thus the failure of a threshold has an actual finite certificate. The theorem gives neither a uniform bound on its rank nor a stopping bound for a search at a correct threshold.

## 5. Which obstruction changes coefficients, and which changes the rate

A failed inequality for a chosen H need not rule out its threshold. In the restricted rank-one controller for k=5 or k=6, u=sqrt(8) is the proved optimum. The choice H identically one fails the safe first level (2,{1}) because 2<sqrt(8). Its incoming/outgoing coefficient ratio can be repaired: (2.3) requires H(T)/H(R)>=sqrt(2). The canonical future potential supplies that change. This example concerns the specified restricted controller, not a claim that sqrt(8) is globally feasible.

A self-edge has no coefficient ratio available to repair. The new ten-generator block has an empty-support self-edge at radix 1651. At the old global upper threshold u=93^(1/6), (2.3) would require 1651^3>=93^5, which fails. This obstruction changes the arithmetic upper bound independently of every proposed H. Its actual block and modular proof are delivered in the companion note.

For the eight previously audited finite controllers, future values can be computed in exact rational powers. At u=B^(1/p), write f=F_u^p. The recurrence is

\[
f(R)=\min\{1,\min_{R\to T}(b^p/B^{|A|})f(T)\}.
\]

The new checker computes these values, proves 2^(-p)<=f<=1, checks every retained cost representative, verifies equality in the recurrence, and checks support-inclusion monotonicity. The original full profile audits retain their separate scope. All eight k=5,6 and rank=1,...,4 calibrations pass, including states that need a nonconstant potential.

## 6. General pattern matrices and the preserved boundary

For the preceding binary-rigid translation-invariant integer pattern matrix L, replace the AP second-difference matrix by L and the reset radix by its established value R_L=max(2,max_i m_i), where m_i is the positive row mass. The same proof gives

\[
F_u(Q)\in[1/R_L,1],\qquad H_u=R_LF_u\in[1,R_L]
\]

at every feasible threshold. The monotone Bellman equation has terminal value R_L, and the path compiler retains the factor R_L. This transfer uses the literal support diagram, actual pattern columns, integral carries, and old quotient maps. It does not claim a new analytic estimate for the Zeta source.

The new graph packet gives another source-level obstruction mechanism in that framework. A scalar relation among complete-graph score points is prolonged to an actual packet whose sole last second defect is that same relation. Its scalar observation is zero while its original source defect remains visible. The resulting arithmetic progression is the obstruction returned by the compiler at the source level.

## References and proof scope

The Clankers. (2026, September 14). *Supported zero resets and exact variable-block capacity*; *A compact all-rank dual from the retained reset cost* [Research notes]. Exact prior package `EP817_ZETA_INTEGRATION_20260914`. These supply the original controller and finite-set interface. The complete notes and their hash-bound certificates are retained as predecessors.

KokunoYumeto. (2026). *Reconstruction with changes of support index* [TeX source]. Zeta Function Research Reader, revision 42df8a2de002d5fc7090641fac46ea11be05fa71. Original support and internal quotient conventions.

The Clankers. (2026, September 15). *Graphical obstruction propagation and a stronger six-term construction* [Companion research proof]. This contribution. No new Lean verification or completed evaluation of the all-rank feasible maximum is claimed.
