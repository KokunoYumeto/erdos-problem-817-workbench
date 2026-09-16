# Supported zero resets for translation-invariant integer patterns

Research contribution returned from the Erdős 817 workbench to the SplitZero workbench. The original support reconstruction, internal relation quotient, and source-metric distinctions are retained. All general statements below have written proofs; the accompanying computations are exact finite calibrations and EP817 certificates, not new Lean elaboration or a theta-source weight estimate.

## 1. A precise all-pattern dichotomy

Let L be any finite integer matrix with t>=2 columns and row sums zero. Keep every row, including redundant and zero rows. For a subset X of the integers, a forbidden pattern is a tuple y in X^t with Ly=0 whose entries are not all equal. For a finite positive generator set A, X=H(A) includes zero. Put m_i=sum_j max(L_ij,0); the zero row has m_i=0. Set M=max_i m_i, with M=0 when there are no rows.

There are two exhaustive, finitely decidable cases.

**Case I.** There is a nonconstant epsilon in {0,1}^t with L epsilon=0. Then every nonempty generator set A has a forbidden pattern. For any actual a in A, the typed map epsilon -> a epsilon belongs to H(A)^t, has nonconstant entries, and is killed by L. The domain of nonempty admissible generator sets is empty. This conclusion is obtained from the displayed witness, not from a claim that a general additive-pattern problem is impossible.

**Case II.** The only binary kernel vectors are constant. Call this finite property binary rigidity. Put

\[
q=\max(2,M+1),\qquad R=\max(2,M).
\tag{1}
\]

Then all the finite and infinite constructions in Sections 2–5 below exist, and the infinite canonical scheduling optimization at every fixed maximum block size is exactly computable.

This is an unconditional dichotomy for the stated matrix class. Binary rigidity is tested by the finite enumeration of 2^t columns, rather than assumed as an unknown global extremal hypothesis. The AP second-difference matrices belong to Case II, with M=2, q=3, R=2. The row (2,-3,1), describing an affine three-point pattern with unequal spacing, also belongs to Case II and gives q=4, R=3. The row (1,1,-1,-1) belongs to Case I: (1,0,1,0) is a retained nonconstant binary witness. A Sidon formulation that excludes such trivial patterns would have a different forbidden set and needs its own flag definition; that different problem is not silently substituted here.

## 2. The original integral relation and bounded carries

At level j let b_j>=2, let D_j be an actual subset-sum image contained in [0,b_j-1], and let P_0=1, P_(j+1)=b_jP_j. The map from digit rows to numerical rows is

\[
\operatorname{ev}_{\mathbf b}(d)_i=\sum_{j<m}P_j d_i^{(j)}.
\]

It is bijective on the product of the distinct canonical digit images. All original binary representations of each digit remain in its fiber. Multiplication by L commutes with evaluation:

\[
L\operatorname{ev}_{\mathbf b}(d)=\sum_{j<m}P_jLd^{(j)}.
\tag{2}
\]

For an actual forbidden-pattern row define prefix carries by

\[
c_{
u,i}=P_\nu^{-1}\sum_{j<\nu}P_j(Ld^{(j)})_i.
\tag{3}
\]

The numerator is integral-divisible by P_nu when the terminal numerical equation holds, since the remaining tail is divisible by that power. Consecutive prefixes give the exact relation

\[
b_jc_{j+1}=c_j+Ld^{(j)},\qquad c_0=c_m=0.
\tag{4}
\]

Conversely, (4) telescopes to Ly=0. Because the row sums vanish and the positive and negative masses both equal m_i,

\[
|(Ld^{(j)})_i|\le m_i(b_j-1),\qquad
|c_{\nu,i}|\le m_i(1-P_\nu^{-1})<m_i.
\tag{5}
\]

For m_i>0, the complete integer carry coordinate lies in {1-m_i,...,m_i-1}; a zero row keeps coordinate zero. The finite source retains all these coordinates, not merely a basis of the rational row space.

A flag records whether any digit column so far is nonconstant across the t rows. Canonical digit uniqueness makes this exactly nonconstancy of the numerical tuple. The only reachable false-flag state is zero carry: a constant column is killed by every original row and preserves zero carry. Acceptance is zero carry with true flag. Equations (2)–(5) give explicit inverse maps between accepting labeled paths and represented numerical patterns.

## 3. The reset is a present zero, with positive cost

A level with no generators has digit image {0}. Its word source Q[{empty word}] is one-dimensional. Its scalar amplitude observation kills the basis vector, while the original value-basis source remains present. The extra kernel of that scalar observation is the whole one-dimensional space. This is a literal instance of the original-boundary/further-observation-kernel distinction in the inspected SplitZero reconstruction.

Apply such a level with radix R from (1). Its relation is R c'=c. Every allowed nonzero carry has a coordinate of magnitude between one and R-1; it has no integral outgoing transition. At a safe controller state there is no true zero carry, so all true paths disappear. The false zero path has its actual all-zero label and survives. Hence the reset sends every safe true-flag support to empty.

The full active support still contains the false zero state. It is a nonbottom support in the reconstruction semilattice of active states. The reconstructed coefficient zero at that support and external absence remain distinct. The controller's shorthand 'empty true support' never discards the constant paths.

The level has positive logarithmic cost log R and no generator reward. It multiplies the position of every later generator by R. Omitting this factor would alter the integer construction. For an internal empty level, the exact absorption map multiplies the preceding nonempty radix by R. A leading empty product C sends the first level (b,A) to (Cb,CA). These maps preserve actual generator values, original subset masks, and total radix product. Thus zero levels can be retained for optimization and then removed with their full cost stored in neighboring radices.

## 4. Finite anchors and the complete bounded-rank reduction

In Case II, the singleton digit image {0,1} is pattern-free modulo q. Indeed |(L epsilon)_i|<=m_i<q, so modular zero forces actual zero, and binary rigidity then forces a constant column. The same argument at the least base-q digit and induction proves that

\[
C_n=\{1,q,\ldots,q^{n-1}\},\quad Q_n=q^n
\tag{6}
\]

is an n-generator modular anchor for every n. Its sum is smaller than Q_n, and all repeated-root or coefficient relations in L remain part of the same row equations.

Fix a maximum nonempty block size r. A schedule may change every radix, every positive weight, and every block size from one through r. At any safe prefix, replace a level (b,A) of size n with the reset (R,empty) followed by (Q_n,C_n). The result is safe, has reward n, cost R Q_n, and outgoing true support empty. That support is contained in any original safe outgoing support. The exact deterministic carry transfer is monotone under support inclusion, so the original remaining suffix stays safe. If b>R Q_n, the replacement strictly lowers cost.

The word-level substitution is a new construction, not an equality of old and new amplitudes. The anchor has distinct binary subset sums, so the identity on masks gives a surjection from its value-basis space to the original Q[H(A)]. The added kernel consists exactly of old representation collisions. This quotient and the outgoing support inclusion are the two stated comparison maps.

After all replacements the dictionary is finite:

\[
(R,\varnothing),\qquad
1\le |A|=n\le r,\quad S(A)<b\le Rq^n.
\tag{7}
\]

A better explicitly verified size-n modular anchor replaces q^n by its actual modulus. Equations (4) and (5) give a finite deterministic controller on sets of true carries. Every safe support has a reset edge back to the initial support, so all reachable safe supports communicate through that support. Assign to an edge cost log b and reward |A|. Zero-reward cycles have positive cost; cycles with positive reward have exact cost exp(sum log b/sum |A|). Removing cycles from any finite path bounds its excess over the smallest cycle ratio by the bounded residual simple path. Repeating a least-ratio cycle attains the bound. Support monotonicity allows its periodic word to start at the initial support.

**Theorem.** For every binary-rigid row-sum-zero integer matrix L and every r>=1, the optimum over all positive-reward canonical schedules with block sizes at most r equals the minimum positive-reward cycle ratio in (7). It is attained periodically and is an exactly computable algebraic number. This conclusion quantifies over arbitrary original radices and integer weights, not only a preset finite collection.

An attaining period is mapped back to one ordinary finite generator block by C=union_j P_j A_j, Q=product_j b_j. The source has exactly sum_j |A_j| distinct generators and S(C)<Q. The explicit labeled path correspondence certifies its infinite repetitions.

## 5. Exact relation to the unrestricted growth rate

For binary-rigid L, M>=1. For finite L-admissible A,B define

\[
A\star_L B=A\cup(MS(A)+1)B.
\]

Euclidean division identifies their actual subset-sum image with H(A) times H(B). If a target tuple satisfies Lz=0, the first coordinate row amplitude has magnitude at most m_i S(A)<=M S(A), strictly below the base. Divisibility therefore makes each factor tuple satisfy its original L equations. Admissibility in both factors forces a constant target tuple. The new cost is exactly multiplicative:

\[
MS(A\star_L B)+1=(MS(A)+1)(MS(B)+1).
\tag{8}
\]

Let g_L(N) be the minimum largest generator. Minimize the sum observable in (8), and use

\[
Mg_L(N)+1\le h_L(N)\le MN g_L(N)+1.
\]

The submultiplicative log argument proves existence of lambda_L=lim_N g_L(N)^(1/N). Every admissible A has the modular certificate (MS(A)+1,A), by the same row-amplitude divisibility. Thus

\[
\lambda_L=\inf_{A\ne\varnothing\ L\text{-admissible}}
(MS(A)+1)^{1/|A|}
=\inf_{r\ge1}\delta_{L,r}.
\tag{9}
\]

Formula (9) does not evaluate that infimum or give its convergence modulus. It supplies an exact increasing-rank family of finite problems and finite construction witnesses for every strict rate improvement. The numerical evaluations in the attached certificates concern L equal to the AP matrices for k=5 and k=6, with maximum block size at most four.

## 6. Original cohomology and metric interfaces

For a supported finite set S of original words, let V_S=Q[S], W_S=Q[ev(S)], and pi_S(e_w)=e_ev(w). Its original relation module is R_S=ker pi_S. These are transport-compatible under support inclusion and reconstruct over the original split scalar using LinearDiagram.Total. The quotient map sends a boundary to its receiving supported zero. A later amplitude observation W_S->Q may have its own additional kernel; it is not substituted for R_S.

The word fibers also give the exact minimum-norm quotient metric. In the original orthonormal word basis, the section of e_y is the average of the mu_S(y) actual words with value y, and its Gram is diag(1/mu_S(y)). For S subset T, the two sections differ by an actual T-relation; its squared norm is 1/mu_S(y)-1/mu_T(y). At several canonical levels the quotient Gram is the tensor product of the actual level Grams. The norm of the identity into unit value coordinates is product_j sqrt(max_y mu_j(y)). The reset has mu(0)=1 but retains its radix cost. These formulas separate value-space metrics, original relation directions, and numerical construction costs.

This contribution returns a finite-source control technique to the Zeta workbench. It does not assert that the theta quotient has become a finite carry system. The source-comparison map used is the original support/quotient reconstruction applied to these explicitly defined word spaces. No arithmetic Mellin observation kernel, spectral packet, or source metric is replaced. The Zeta programme's separate growing-source metric estimate retains its own scope.

The companion compact-global-dual.md proves a further exact all-rank dual: the original rate is the largest u admitting a coefficient function H in [1,R] on the full finite safe-support set, with bH(T)>=u^|A| H(S) for every actual canonical edge. The uniform interval follows from appending the retained reset to any finite safe path. Its remaining constraints quantify over all generator blocks; no finite rank truncation is substituted for them.

## 7. Applications and evidence

For the AP matrix with k=5 or k=6, the companion EP817 note proves

\[
\delta_{k,1}=\sqrt8,\quad
\delta_{k,2}=\delta_{k,3}=\sqrt5,\quad
\delta_{k,4}=23^{1/4}.
\]

These permit changes among every block of every admitted size. Both rank-four lower certificates cover the full 41,571-label dictionaries. A separate auditor verifies their original binary fibers, every carry profile, all safe and rejected support transfers, positive rational potential inequalities, and an attaining periodic word. The reusable calibration checker also tests ten integer matrices, 1,102 reset carry states, 512 rigid binary columns, 1,364 literal empty-level absorptions, seven orbit counts, and a nontrivial collision quotient with Gram entry 1/2. Finite calibrations corroborate the written all-matrix proof; they are not a substitute for it.

No original SplitZero or Lean file is changed by this add-only workbench. The producer, independent auditor, complete compressed proof records, and exact source hashes are included so that the arithmetic application can be replayed without checking out the EP817 repository. No independent human review or new Lean success is claimed.

## References

KokunoYumeto. (2026). *Reconstruction with changes of support index* [TeX source]. Zeta Function Research Reader, revision 42df8a2de002d5fc7090641fac46ea11be05fa71, workbenches/splitzero-tandem/tex/support_diagrams.tex. Role: original support reconstruction, relation quotients and comparison kernels.

The Clankers. (2026, September 14). *Support-preserving outer control for Erdős Problem 817*. Role: original word-fiber quotient metric, section corrections, and fixed-block certificates retained in the EP817 integration payload.

The Clankers. (2026, September 14). *Supported zero resets and exact variable-block capacity*. Companion EP817 research/variable_blocks note. Role: full AP proof and exact maximum-block-size classifications.

Karp, R. M. (1978). A characterization of the minimum cycle mean in a digraph. *Discrete Mathematics, 23*(3), 309–311. https://doi.org/10.1016/0012-365X(78)90011-0 . Classical graph-optimization context; specialized proofs are included above.

Megiddo, N. (1978). Combinatorial optimization with rational objective functions. In *Proceedings of the tenth annual ACM symposium on Theory of computing* (pp. 1–12). https://doi.org/10.1145/800133.804326 . Classical ratio-objective context, not a source of the supported-reset arithmetic construction.
