# Finite arithmetic observations and the all-block capacity return

The Clankers. 16 September 2026. General proofs and exact finite evidence; independent mathematical review pending. No new Lean elaboration and no theorem about the unresolved arithmetic theta-source estimates.

This contribution returns two interfaces from the Erdős 817 calculation: an exact two-column receiving kernel for all ternary blocks, and a finite-observation prime construction that yields a global cardinality variational principle. All original coefficients, admitted word supports, and quotient masses remain attached. The inspected SplitZero interface is `workbenches/splitzero-tandem/tex/support_diagrams.tex`, equations D6--D8, at revision `58626a62cd5648e8ae7450fb54d4a4aab2330981`.

## 1. The supported quotient in the two-column calculation

Fix b>=2, a finite nonempty D in [0,2b-2], and a finite integer set Y. On the actual value-pair source let

\[
\pi:\mathbb Z[D\times Y]\to\mathbb Z[D+bY],\qquad
 e_{(d,y)}\mapsto e_{d+by}.
\]

Every nontrivial fibre is exactly

\[
\{(d+b,y),(d,y+1)\},\qquad d,d+b\in D,\quad y,y+1\in Y.
\]

The free module on those pairs maps injectively to the source by their difference. Its image is exactly ker(pi), since all fibres have at most two elements. These relation columns have disjoint original supports. For an admitted subset of source pairs, retain only the pairs whose two members are actually admitted. The resulting kernel family is stable under admitted-support inclusion and gives precisely the original internal quotient diagram.

A vanished difference goes to the zero coefficient in its receiving admitted support. That support is not replaced by the external bottom. If an active source is empty, its zero module is still a fibre at that active label. If the original generator set is empty, its one empty word represents the numerical value zero, with mass one; this source is not an empty module.

The rank of this receiving kernel is

\[
\#\{d:d,d+b\in D\}\,\#\{y:y,y+1\in Y\}.
\]

Writing t=|D|, \kappa for its number of integer runs, v=|D mod b|, and \eta=|(D mod b)\cup(D mod b+1)|-v gives the exact transfer

\[
\binom{|D+bY|}{\kappa(D+bY)}
=
\begin{pmatrix}v&t-v\\\eta&\kappa-\eta\end{pmatrix}
\binom{|Y|}{\kappa(Y)}.
\]

The matrices multiply in their actual radix order for changing blocks. This is a numerical observation of the displayed quotient, not a replacement definition of its homology.

For positive original pair masses w(d,y), the original quotient Gram is the diagonal matrix with entries

\[
\left(\sum_{d+by=x}w(d,y)\right)^{-1}.
\]

Its section has coefficient w(d,y)/sum(w) on each fibre. The section is orthogonal to the original differences and satisfies both the quotient inverse and Pythagorean formulas. When these values come from coefficient words, take the product of their actual representation multiplicities for w. No uniform-on-words distribution is identified with a uniform-on-values distribution.

## 2. The original and further arithmetic observation kernels

Let A be distinct positive integer generators and

\[
\Phi:\mathbb Z^n\to\mathbb Z,\qquad \Phi(c)=\sum_i c_i a_i.
\]

For a prime p, put

\[
K=\ker\Phi,\qquad K_p=\Phi^{-1}(p\mathbb Z).
\]

There is an exact sequence

\[
0\to K\to K_p\xrightarrow{\Phi}p\mathbb Z\cap\operatorname{im}\Phi\to0.
\]

The additional arithmetic congruence kernel remains explicit. The prime certificate below proves only that the admitted bounded coefficient source has no extra zero under this observation.

For integer h>=1 define

\[
\Delta_h(A)=\Phi([-h,h]^n\cap\mathbb Z^n)=H_{2h+1}(A)-hS(A).
\]

If p divides no nonzero member of this set, reduction is injective on the distinct numerical H_(h+1) image. Thus the map of free value bases

\[
\mathbb Z[H_{h+1}(A)]\longrightarrow
\mathbb Z[\rho_pH_{h+1}(A)]
\]

is an isomorphism, commuting with the original bounded-word quotients and retaining their exact fibres and masses. Its source and target are free integer modules. The further amplitude observation lands in the integer module Z/pZ; no ring map from Q to a finite field is postulated. Scalar extension of the free value-basis isomorphism can be performed separately, without extending that nonexistent ring map.

For nonempty bounded supports these maps are natural under restriction. The coefficient zero and the external support bottom therefore remain those of the existing G(Z) reconstruction.

## 3. General translation-invariant pattern matrices

Let L be an integer matrix with t>=2 columns, at least one nonzero row, and all row sums zero. An L-pattern is a tuple x in R^t with Lx=0; it is forbidden when its entries are not all equal. Let

\[
h=\max_i\sum_{j:L_{ij}>0}L_{ij}
=\max_i\sum_{j:L_{ij}<0}(-L_{ij})\ge1.
\]

There is an unconditional finite dichotomy.

If a nonconstant binary vector epsilon satisfies L epsilon=0, every nonempty positive generator set fails: for any one original generator a, the actual subset values a epsilon_j provide the forbidden tuple. This is the explicit witness map from the binary kernel to the original numerical pattern.

Otherwise L is binary-rigid: every binary kernel vector is constant. Then powers of h+1 supply arbitrarily large L-admissible sets. Indeed reduction of an L-pattern in their binary digit language modulo h+1 forces every row defect, an integer in [-h,h], to vanish. Binary rigidity makes each digit column constant, and subtraction/division proceeds to the preceding length. The inverse insertion is the original constant digit followed by multiplication by h+1.

Define g_L(n) by minimizing the largest distinct positive generator in an n-element L-admissible set. Its exponential rate exists. To prove it retain

\[
R=hS(A)+1,\quad C=A\cup RB.
\]

The product-value map (x,y)->x+Ry is a bijection with its integer division inverse. Each row's low-part defect lies in [-hS(A),hS(A)], so divisibility by R forces it to vanish. Both coordinate tuples are L-patterns and hence constant if A and B are admissible. Thus C is admissible, and

\[
hS(C)+1=(hS(A)+1)(hS(B)+1).
\]

Minimizing this observable proves submultiplicativity. Comparing it to max(A) proves existence of \lambda_L as in the EP817 proof. Every comparison constant is h times the displayed generator count; no scale parameter is omitted.

## 4. General-pattern cardinality capacity

For binary-rigid L,

\[
\boxed{\lambda_L=\inf_{A\ L\text{-admissible}}
|H_{2h+1}(A)|^{1/|A|}.}
\]

The same infimum is obtained by every fixed larger arity. Here is the constructive upper implication.

Given A, let K=(|H_(2h+1)(A)|-1)/2 and ell=1+floor(log_2(hS(A))). The elementary prime-product proof in the companion note gives

\[
p\le256+4K\ell
\]

dividing no nonzero original bounded image in [-h,h]^n. The residue observation is injective on H_(h+1)(A). In a modular L-pattern on H(A), the positive and negative parts of each row are elements of H_(h+1)(A). Residue equality therefore lifts to integer equality. Original L-admissibility makes the tuple constant. Residue injection on H(A) identifies its actual digits as well.

Thus the unchanged-weight geometric lift union_j p^j A is L-admissible at every finite length: reduce an L-pattern modulo p, identify its actual common low digit, subtract it, divide by p, and iterate. Row-sum zero is exactly what makes the common-digit subtraction preserve L. Every generator has nonzero residue, so cross-level generator collisions are excluded. Actual digits greater than p are retained.

Now take r separated copies of A in base

\[
R=2hS(A)+1.
\]

There are rn original generators, their (2h+1)-image cardinality is |H_(2h+1)(A)|^r, and their sum is (R^r-1)/(2h). The new faithful prime is bounded by

\[
256+2(|H_{2h+1}(A)|^r-1)r(1+\lfloor\log_2R\rfloor).
\]

Taking roots per rn generators and then r->infinity proves the upper inequality. The converse follows by applying |H_(2h+1)(A)|<=2hn max(A)+1 to an extremal n-element set and taking roots. This proves the exact formula, without an assumed pattern-density estimate.

For ordinary arithmetic progressions the row matrix is the consecutive second-difference matrix and h=2 for every k. This explains why the finite arity at which the variational invariant stabilizes is uniformly five, independently of the progression length. The number of rows grows with k; the coefficient radius needed by the prime observation does not.

## 5. Homogeneous and nonstationary return losses

The two-state original quotient proves that a fixed colliding ternary block loses an exponential factor in its number of distinct images. It also computes a contrasting varying-schedule example. Keep the actual six-generator block {1,4,5,17,21,22}; use base 97 at zero-based levels 3*2^l and base 141 elsewhere. Both binary digit sources are five-admissible. For its ternary image N_m, with ell_m special levels,

\[
\tfrac12(2245/3197)^{\ell_m}
\le N_m/139^m
\le2(2245/3197)^{\ell_m-1}.
\]

The complete proof and actual source matrices are in companion Section 9.1. The loss exponent is log(3197/2245)/log2 against log m. The local relation remains present, but its sparse occurrence changes the accumulated arithmetic return. A uniform estimate over schedules cannot be inferred merely from the fact that one supported receiving kernel is nonzero. The exact frequency and matrix order supply the comparison.

## 6. Limits, provenance, and checking scope

This construction controls the two-column image transfer uniformly over the full block family, and replaces the global height/radix optimization by an exact finite-image cardinality infimum. The generator count in that infimum remains unbounded. The proof does not establish the optimal value for general L or general k.

The one-block prime choice has a real height cost: {1,L} with L a large primorial has fixed |H_5|=25, while every prime factor of L fails the observation. The amplification construction retains that logarithmic cost before proving that its exponential per-generator contribution tends to zero. It does not set the cost to a constant.

There is also a genuine nonattainment phenomenon at k=3: |H_5(A)|>3^|A| for every nonempty admissible A, but powers of three have |H_5|=2*3^n-1. Thus the capacity equals 3 without a minimizing finite block. Finite-state control of a specified block is not being used as a proof that the all-block infimum is attained.

The standalone finite evidence files are copied byte-for-byte from the EP817 contribution. The auditor imports neither its producer nor its helper library. The generic prime lemma is checked at several coefficient radii; the universal matrix-pattern theorem rests on the proof in Section 4, not an exhaustive enumeration of every integer pattern matrix. No theta-source primitive, analytic quotient, nilpotent spectral packet, or arithmetic moment is claimed to have been evaluated by these finite checks.

The original k=4 construction and mathematical proof remain credited to the anonymous/deleted Reddit contributor. sneed-and-feed retains the distinct finite-upper-bound Lean credit. Existing SplitZero source and verification pins are unchanged.

### Source roles

KokunoYumeto. (2026). *Reconstruction with changes of support index*. `zeta-function-research-reader`, revision `58626a62cd5648e8ae7450fb54d4a4aab2330981`, support_diagrams.tex, D6--D8. Actual reconstructed quotient and additional observation-kernel interface.

Korsky, S. (2026). *Arithmetic progression-free subset-sum sets* (arXiv:2606.24139v1). Original extremal definitions and benchmark; no imported all-block lower estimate.

The Clankers. (2026, September 16). *All-block image capacity and exact ternary transfer*. Companion proof, including the fully elementary prime-budget calculation and actual mixed-block matrices.
