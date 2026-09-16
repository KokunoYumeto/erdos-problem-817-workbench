# Supported zero resets and exact variable-block capacity

Research continuation, 14 September 2026. Ordinary mathematical proofs and exact finite certificates; independent mathematical review pending. No new Lean elaboration is claimed. This note extends the preceding fixed-block work to schedules in which both the generator block and its size may change at every level.

## 1. Original problem and scope

For a finite set A of distinct positive integers, retain its actual subset-sum set H(A), including zero, and its sum S(A). A is k-admissible when H(A) has no ordered nonconstant k-term arithmetic progression. The extremal quantity g_k(N) minimizes max(A) among N-element admissible sets. The original mathematical construction for k=4 remains attributed to the anonymous/deleted Reddit contributor; sneed-and-feed retains separate credit for its finite upper-bound Lean formalization.

A canonical level is a pair (b,A), where b>=2 is an integer and S(A)<b. In an infinite schedule retain

\[
P_0=1,\quad P_{j+1}=b_jP_j,\quad
G_m=\bigcup_{j<m}P_jA_j,\quad N_m=\sum_{j<m}|A_j|.
\]

Generators are distinct: each one at level j is strictly below P_(j+1), and all generators at later levels are at least P_(j+1). A subset chooses one actual digit in D_j=H(A_j) at every level. Consequently its numerical image is exactly

\[
H(G_m)=\left\{\sum_{j<m}P_jd_j:d_j\in D_j\right\}.
\tag{1}
\]

Mixed-radix digit evaluation is bijective on the product of distinct digit images. Subset representations within each image retain their multiplicities. No distinctness of all binary subset sums is assumed.

Fix r>=1. Permit every level to have at most r generators, and require N_m to tend to infinity. For the moment the empty block is also permitted. Define

\[
\delta_{k,r}=\inf_{\substack{|A_j|\le r,\ N_m\to\infty\\
H(G_m)\ k\text{-AP-free for every }m}}
\liminf_{m\to\infty}P_m^{1/N_m}.
\tag{2}
\]

Indices before the first positive N_m have no effect on this limit. The objective is the retained radix cost per actual generator. Empty levels have positive radix cost and zero generator reward. Section 3 proves that they can be absorbed exactly into nonempty levels; their introduction does not enlarge the infimal value beyond that attainable by nonempty canonical schedules.

The previous quantity Gamma_(k,n) uses the SAME n-element block at every level. The inclusion of those schedules in (2) gives delta_(k,r)<=Gamma_(k,n) for every n<=r. The current theorem treats changes in the actual weights and in block size, as well as arbitrary changing radices.

**Main theorem.** For every k>=3 and r>=1, delta_(k,r) is an attained, exactly computable algebraic number. It is the minimum cost/reward ratio on an explicit finite controller using only

\[
(2,\varnothing),\qquad
1\le |A|=n\le r,\quad S(A)<b\le2\cdot3^n.
\tag{3}
\]

A better verified modular anchor of size n and radix q_n replaces the corresponding cutoff by 2q_n. The minimum is attained by a periodic schedule. Moreover

\[
\delta_{k,r+1}\le\delta_{k,r},\qquad
\lambda_k:=\lim_{N\to\infty}g_k(N)^{1/N}
=\inf_{r\ge1}\delta_{k,r}.
\tag{4}
\]

The equality in (4) is a characterization, not a numerical evaluation of the unbounded-rank infimum. The sharp general lower law remains unproved in this contribution.

## 2. Carry paths with all support and column data retained

For a k-tuple of actual digits d, put

\[
\Delta(d)_i=d_i-2d_{i+1}+d_{i+2},\quad 0\le i<k-2.
\]

The original relation at consecutive levels is

\[
b_jc_{j+1}=c_j+\Delta(d^{(j)}),\quad c_0=0.
\tag{5}
\]

Multiplying by P_j and summing gives

\[
\sum_{j<m}P_j\Delta(d^{(j)})=P_mc_m.
\tag{6}
\]

Thus terminal carry zero is exactly the integer second-difference condition. Every integral prefix carry satisfies

\[
|c_{m,i}|\le2(1-P_m^{-1})<2,
\]

because each column defect has magnitude at most 2(b_j-1) and
sum_(j<m) P_j(b_j-1)=P_m-1. The exact carry domain is therefore contained in C_k={-1,0,1}^(k-2), independently of the sizes of the blocks or radices.

A flag records whether the first two digit rows have ever differed. Canonical evaluation makes this precisely numerical inequality of their first two values. When the flag remains false, the first two current digits agree; starting from carry zero, divisibility in (5) then forces each later digit of that column to agree too. The only reachable false-flag state is therefore (0,false). Its actual constant-column paths are always retained.

For a level (b,A) let I_(b,A) be the targets from (0,false) with a nonconstant column. For c in C_k, let T_(b,A)(c) be the complete set of targets from c, using all actual columns in H(A)^k. A controller state R records the reachable true-flag carries, with deterministic update

\[
\mathcal T_{b,A}(R)=I_{b,A}\cup\bigcup_{c\in R}T_{b,A}(c).
\tag{7}
\]

The separately retained false state is understood in (7); the full active support is {(0,false)} union {(c,true):c in R}. In particular R=empty does not mean that the original source is absent. The controller is safe exactly when 0 is not in R. Every accepted path gives a numerical progression by (1) and (6); every numerical progression recovers its unique rows and its integral prefix carries by division. The path/tuple correspondence is exact.

The transfer (7) is monotone: R subset R' implies T(R) subset T(R'). This follows from the displayed union and is the precise simulation relation used in the replacement argument. The finite alphabet can be evaluated without choosing all k digits independently. For fixed c and the first two actual digits, the remaining digits are forced modulo b by (5); each residue has at most one representative in the canonical digit image. The verifier retains every actual binary-mask fiber of every digit.

## 3. A supported zero level is a universal reset

**Lemma 1.** For every safe true-flag support R, the level (2,empty) sends R to the empty true-flag support and retains the false state.

**Proof.** Its digit set is exactly {0}. Equation (5) becomes 2c'=c. For integral c,c' in {-1,0,1}^(k-2), this is possible only when c=c'=0. Since safe R excludes true carry zero, no true path survives this level. The false zero path has the actual all-zero column and survives. QED.

An empty block is a PRESENT level with one subset choice and one numerical digit. Its word space is Q[{empty word}], of dimension one. The scalar amplitude observation sends its basis vector to zero; its kernel is the whole one-dimensional word space. Sending that space to the zero object is the explicit additional observation, not the original subset-sum image. The radix multiplier two remains in P_(j+1)=2P_j. Erasing it would change every later generator.

Empty levels can also be eliminated without discarding their effect. Each empty level after a nonempty level multiplies that preceding level's radix. A leading run of empty levels with product L is absorbed by sending the first nonempty (b,A) to (Lb,LA). The literal generator sets and final radix product are unchanged, S(LA)<Lb, and block sizes are unchanged. Internal and trailing empty runs are handled by the same rule. For completeness, write a_i for log P just after the i-th nonempty level, e_i for the sum of log radices in the following empty run, and N_i for its cumulative generator reward. Then a_i/N_i <= (a_i+e_i)/N_i <= (a_(i+1)/N_(i+1)) (N_(i+1)/N_i). Since 1<=N_(i+1)-N_i<=r and N_i tends to infinity, the outer sequences have the same limit inferior, also when it is infinite. These are respectively the pre-empty and absorbed-endpoint costs. Thus elimination preserves the infimal objective in (2), even for empty runs of unbounded length. For a periodic schedule with positive reward, cyclically start at a nonempty level and absorb the finitely many empty runs in its period.

This is also a concrete instance of the original SplitZero distinction: the level has a nonbottom active support even though its numerical coefficient is zero. The inherited reconstruction and original-versus-further-kernel square are the interfaces used here; no theta-source estimate is imported.

## 4. A rank-dependent finite cutoff even when all blocks vary

Let C_n be a verified n-element block whose subset-sum digits are k-AP-free modulo q_n, with S(C_n)<q_n. Its transfer from empty true support returns empty support. Such anchors exist for every n: take C_n={1,3,...,3^(n-1)} and q_n=3^n. At the least base-3 digit, a modular 3-AP in the binary digits would have to be constant; stripping common digits proves modular 3-AP-freeness modulo 3^n. Its first three entries exclude a nonconstant k-AP for any k>=3.

**Lemma 2 (cost-bounded replacement).** An arbitrary canonical level (b,A) with |A|=n can be replaced, from any safe incoming support, by

\[
(2,\varnothing),\ (q_n,C_n).
\tag{8}
\]

The replacement has the same generator reward n, total radix cost 2q_n, and final true support empty. When b>2q_n its cost is strictly smaller.

**Proof.** Lemma 1 resets the incoming support to empty; modular admissibility of the anchor returns empty. Its intermediate support is safe. If the original outgoing support was R', empty is a subset of R'; by monotonicity, every remaining original suffix that was safe from R' is safe from the replacement support. QED.

This compares two explicitly constructed schedules. It does not identify their scalar generator values. At the n binary choices, the ternary anchor has distinct subset sums, so the identity on masks induces a surjection from its value-basis space to Q[H(A)]. Its kernel is spanned by differences of masks with the same original A-value. Choosing the mean of each fiber gives the original quotient Gram diag(1/mu_A(y)); the corresponding source metric correction is retained. At the controller boundary the map is the explicit inclusion empty -> R'. Those are the two distinct comparison maps, not an asserted arithmetic isomorphism of arbitrary integers.

Replace every overlarge level by (8), and every empty level's radix by two. At aligned original block boundaries generator reward is unchanged, accumulated cost is no larger, and the new support is contained in the old one. All inserted intermediate levels are safe. The resulting schedule belongs to the finite dictionary

\[
\mathscr D_{k,r}=\{(2,\varnothing)\}\cup
\{(b,A):1\le n=|A|\le r,\ S(A)<b\le2q_n\}.
\tag{9}
\]

Taking the limit inferior along the aligned boundaries proves that it cannot have a larger optimal rate. Conversely the finite dictionary is a subclass of (2); empty absorption supplies an original nonempty schedule when needed. Thus (9) has exactly the same infimum as the unrestricted bounded-rank class.

Every positive-weight tuple in (9) is literally enumerated; no rescaling of candidate weights is performed. Invalid one-level blocks receive an actual integer progression witness. In the applied calculations the independently checked anchors are

\[
(q_1,C_1)=(3,\{1\}),\quad
(q_2,C_2)=(5,\{1,2\}),\quad
(q_3,C_3)=(13,\{1,3,4\}),\quad
(q_4,C_4)=(23,\{1,3,4,7\}).
\tag{10}
\]

They work for k=5 and k=6 and give the exact cutoffs 6,10,26,46. These cutoffs control every larger original radix through (8), not through finite empirical evidence.

## 5. Exact symmetry transport and the finite controller

Subset-sum images have the involution d -> S(A)-d. On column paths it maps c to -c and preserves all binary representations by complementing the chosen subsets. Reversal of the k rows maps c to its reversed coordinate tuple. Equation (5) commutes with both operations. At the initial state, a nonconstant modular progression has unequal consecutive digits at both ends; on true states the flag is already retained. Hence all reachable true supports are invariant under

\[
c\longmapsto-c,\qquad c\longmapsto\operatorname{rev}(c).
\tag{11}
\]

No coefficient vector is being identified with zero. A symmetric support is in bijection with the set of full orbits that it contains; the inverse takes their union. Transfer images are evaluated on all original vectors in each source orbit before this reversible support encoding.

Put d=k-2. Burnside counting gives the number of nonzero orbits

\[
a_d=\frac{3^d+3^{\lceil d/2\rceil}+1+3^{\lfloor d/2\rfloor}}4-1.
\tag{12}
\]

The four fixed-point counts are respectively 3^d, 3^ceil(d/2) for reversal, one for negation, and 3^floor(d/2) for negated reversal. Removing the zero orbit gives (12). Thus the safe support controller has at most 2^(a_d) states, including the empty true support. For k=5 this is 2^9=512, rather than the unrestricted powerset count 2^26. For k=6 it is 2^24. Actual reachable state sets can be much smaller.

Every safe state has a reset edge to the initial support. The entire reachable safe graph is therefore strongly connected. Edges retain their radix b, generator reward n, and original block A. The empty reset edge has n=0 and strictly positive cost log 2.

For a directed cycle C with total reward N(C)>0 and radix product B(C), define rate B(C)^(1/N(C)). There are finitely many simple cycles. Zero-reward cycles have strictly positive cost and do not improve any cost/reward ratio. If rho is the least log B(C)/N(C), all cycles have nonnegative sum of log b-rho n. Remove cycles from a finite path; the residual simple path has bounded length and bounded remaining cost. Dividing by cumulative generator reward and taking the limit inferior proves the lower bound rho for every infinite positive-reward path. Repeating a minimizing cycle attains it. Monotonicity permits its period to start from empty true support even when the cycle was first encountered at a larger support.

All cycle comparisons are exact integer-power comparisons. This proves the main finite-optimization theorem and periodic attainment. The underlying minimum-cycle-ratio principle is classical; the supported reset and the resulting complete arithmetic cutoff are the additional construction-specific ingredients.

## 6. Exact evaluations for variable blocks of sizes at most four

The results are

\[
\boxed{\delta_{5,1}=\delta_{6,1}=8^{1/2},\quad
\delta_{5,2}=\delta_{6,2}=\delta_{5,3}=\delta_{6,3}=5^{1/2},\quad
\delta_{5,4}=\delta_{6,4}=23^{1/4}.}
\tag{13}
\]

These allow every block value, every size at most the stated bound, and every infinite canonical schedule. Attaining periods are (2,{1}),(4,{2}) at rank bound one; the constant level (5,{1,2}) at bounds two and three; and (23,{1,3,4,7}) at bound four. The first period is verified from the actual initial support; it need not return to that support after one period, so the full eventual periodic support trace is retained.

Each lower certificate gives a positive rational h on every reachable safe support and integers B,p such that

\[
 b^p h(R')\ge B^n h(R)
\tag{14}
\]

for every actual safe edge, including n=0. Multiply along the path to obtain

\[
 P_m^p\ge B^{N_m}h(R_0)/h(R_m).
\]

There are finitely many positive rational potentials. Their ratio disappears under the N_m-th root, proving rate at least B^(1/p) for every schedule. The attaining period has exactly that cost. This is a finite proof certificate for (13), not a numerical approximation to a spectral radius.

The rank-four dictionaries each contain 41,571 literal levels including the reset. For k=5, 17,846 levels have an immediate integer obstruction, leaving 23,725 usable levels. Their complete controller has 16 reachable safe states, 49,506 safe labeled transfers and 330,094 rejected transfers. For k=6, there are 13,080 immediate obstructions, 28,491 usable levels, 128 reachable safe states, 259,832 safe transfers and 3,387,016 rejected transfers. Every valid source carry is tested; the two column transcripts respectively contain 9,722,718 and 18,969,820 labeled nonzero-source columns.

Parallel edges with the same source, target and reward may use the cheapest radix for finding a potential, but all original labels and transfers remain in the certificate and are checked against (14). The producer uses rational arithmetic only. A separate auditor imports no producer code: it reconstructs the literal domain with combinations rather than recursive partitions, generates columns by an independent closed-prefix formula, and checks all source fibers, all carry transitions, the complete support graph, every potential inequality, and the attaining period.

The known six-generator blocks still give upper rates 97^(1/6) for k=5 and 93^(1/6) for k=6. Since 23^3>97^2 and 23^3>93^2, (13) rules out beating those rates with ANY canonical schedule whose individual blocks have at most four generators. The previous fixed-block rank-five classification does not cover arbitrary changes among rank-five blocks; that larger class remains unevaluated here.

## 7. Return to the unrestricted rate and source metrics

For any periodic safe schedule, aggregate one period into C=union_j P_j A_j and Q=product_j b_j. Its generators are distinct, |C| is the total period reward, and S(C)<Q. Repeating the period is the literal constant-Q lift of C. Consequently every cycle upper construction bounds the original lambda_k, so lambda_k<=delta_(k,r).

Conversely, for every k-admissible finite A, the modulus 2S(A)+1 is safe: each modular second difference of actual values in [0,S(A)] is divisible by that modulus and strictly smaller in magnitude, hence zero over the integers. Thus delta_(k,|A|)<=(2S(A)+1)^(1/|A|). The exact product A star B=A union (2S(A)+1)B satisfies

\[
2S(A\star B)+1=(2S(A)+1)(2S(B)+1).
\]

Euclidean division identifies its subset-sum image with H(A) times H(B) and splits every progression into factor progressions. Minimizing this sum observable gives submultiplicativity; its comparison 2g_k(N)+1<=h_k(N)<=2N g_k(N)+1 proves existence of lambda_k and its equality with inf_A(2S(A)+1)^(1/|A|). These maps prove (4). No assumption of an unknown lower bound occurs. The separate note compact-global-dual.md additionally constructs an exact all-rank dual whose finitely many potential coefficients lie in [1,2]; its block inequalities remain an infinite arithmetic family.

Across arbitrary levels, representation multiplicity remains the product of the level multiplicities. If mu_j(y) counts subsets of A_j with value y, the original orthonormal word-space quotient has Gram diag(1/mu_j(y)); at m levels its Gram is the tensor product of those original Grams. The identity into the unit value-coordinate metric has norm

\[
\prod_{j<m}\sqrt{\max_y\mu_j(y)}.
\tag{15}
\]

Neither the finite controller nor the reset removes (15). They control feasible supports and explicit constructions; a proof of the matching all-rank lower rate must also control the original arithmetic information that grows with rank. The present result does not evaluate inf_r delta_(k,r), give its convergence modulus, or prove the Riemann hypothesis.

## 8. Reusable extension to linear-pattern cohomology

The companion note in the Zeta payload proves an unconditional dichotomy for every integer matrix L with equal row length t>=2 and row sums zero. If L has a nonconstant binary kernel vector, every nonempty positive generator set has a nonconstant forbidden pattern; the witness map is epsilon -> a epsilon for an actual generator a. Otherwise the pattern is binary-rigid and admits a uniform singleton anchor. Writing m_i for the sum of the positive entries in row i, canonical carries satisfy |c_i|<m_i (a zero row keeps carry zero). The supported zero level of radix max(2,max_i m_i) resets all safe nonzero carries. Its positive cost is retained. A modular anchor and reset then give the finite bounded-rank dictionary exactly as above.

This is a transfer of the original support, relation, and additional-observation-kernel interfaces. It is not an arithmetic weight estimate for the theta quotient. The source-metric return remains explicit, including the one-dimensional word source at a zero-digit level.

## 9. Reproduction and publication boundary

Run the producer, then the independent auditor, for example:

```sh
python certificates/verify_variable_blocks.py --k 5 --rank 4 --output certificates/variable_k5_r4.json.gz
python certificates/audit_variable_blocks.py certificates/variable_k5_r4.json.gz --producer certificates/verify_variable_blocks.py --output certificates/audit_k5_r4.json
```

The two largest records are losslessly compressed. Their source, compressed, and plaintext hashes are bound by the release verifier. The same commands apply to k=6 and rank bounds one through three. The separate reset-pattern checker tests the general matrix dichotomy, all state coordinates in the stated calibration domains, original generator-preserving absorption of empty levels, the Burnside orbit count, and a representation-collision quotient metric. Negative tests must reject deliberately modified domain, support, fiber, potential, and reset data.

The publication payload also carries the preceding research/splitzero_outer directory byte-for-byte with its original evidence labels and its 47,259-case audit bindings. Existing Lean sources, pins, receipts, and accepted claim statuses are untouched. GitHub access in this execution was read-only; actual publication status belongs in the release record, not in the mathematical statements. The supplied publisher opens draft PRs only and never merges them or updates main.

## References and precise roles

Korsky, S. (2026). *Arithmetic progression-free subset-sum sets* (arXiv:2606.24139v1). https://arxiv.org/html/2606.24139v1 . Role: original conventions and benchmark general bounds; not a source of (3), (9), or (13).

Karp, R. M. (1978). A characterization of the minimum cycle mean in a digraph. *Discrete Mathematics, 23*(3), 309–311. https://doi.org/10.1016/0012-365X(78)90011-0 . Role: classical graph-optimization background; the cost/reward proof used here is included explicitly.

Megiddo, N. (1978). Combinatorial optimization with rational objective functions. In *Proceedings of the tenth annual ACM symposium on Theory of computing* (pp. 1–12). https://doi.org/10.1145/800133.804326 . Role: classical minimum-ratio-cycle context, not a claim of novelty for cycle optimization.

The Clankers. (2026, September 14). *Support-preserving outer control for Erdős Problem 817*. Retained research/splitzero_outer source from EP817_SPLITZERO_OUTER_20260914.zip. Role: original word-to-value quotient, source metrics, and fixed-block classification through rank five. That fixed-block domain remains separately specified.

The Clankers. (2026, September 14). *SplitZero transfer to Erdős 817: Uniform carry cohomology and exact mixed-base capacity*. EP817 revision 98fd25802a387138053064e11ddd2f6d2007d55b, research/splitzero_transfer. Role: prior uniform inverse and fixed-block/mixed-radix interfaces.

KokunoYumeto. (2026). *Reconstruction with changes of support index*. Zeta revision 42df8a2de002d5fc7090641fac46ea11be05fa71, workbenches/splitzero-tandem/tex/support_diagrams.tex. Role: original reconstructed support diagrams, internal quotients, and the distinction between original boundaries and a further observation kernel. Later Zeta main was observed separately; no newer analytic conclusion is imported.
