# Uniform finite-period approximation and exact finite-word switching minima

The Clankers. 16 September 2026.

**Scope and evidence.** These are ordinary mathematical proofs with exact finite arithmetic replays, submitted for independent review. They continue the seven-observation and local-flow work without changing its sources or inherited Lean receipts. The upstream `research/cone_dual` contribution was inspected at main revision `578564a5f0c6e3348f5bdc33fd2022b674899c41`; its finite-facet all-rank theorem retains its separate attribution. The argument below establishes an explicit word-horizon approximation for a finite arithmetic dictionary and for a finite controller, rather than asserting that an arbitrary optimum is attained by a finite period. It also calculates every finite-length minimum in the earlier radix-ten example. No new unrestricted numerical record or determination of the full Erdős 817 rate is claimed.

## 1. Original arithmetic and the objective

A level is a pair a=(b,A), where b is an integer at least two, A is a nonempty finite set of distinct positive integers, and S(A)=sum(A)<b. Its reward is n(a)=|A|. Fix a coefficient arity q>=2 and write

\[
 H_q(A)=\left\{\sum_{a\in A}c_a a:0\le c_a<q\right\}.
\]

For a finite word w=a_0...a_(m-1), retain every original radix and generator:

\[
 P_0=1,\quad P_{j+1}=b_jP_j,\quad
 A_w=\bigcup_{j<m}P_jA_j,\quad
 N(w)=\sum_{j<m}|A_j|,\quad Q(w)=P_m.
\]

The level intervals prove distinctness: P_j a<P_(j+1), while every generator at a later level is at least P_(j+1). Thus |A_w|=N(w). Also

\[
 S(A_w)=\sum_{j<m}P_j S(A_j)\le Q(w)-1.
\]

Let

\[
 F_q(w)=|H_q(A_w)|,\qquad F_q(\varnothing)=1.
\]

A finite dictionary D consists of finitely many specified levels. Put n_-=min_a n(a)>0 and n_+=max_a n(a). The image-switching optimum is

\[
 \delta_q(D)=\inf_{\omega\in D^{\mathbb N}}
 \liminf_{m\to\infty}F_q(\omega_0\cdots\omega_{m-1})^{1/N(\omega_0\cdots\omega_{m-1})}.
 \tag{1.1}
\]

This is an image cost, not a redefinition of the largest-generator cost. The maps through A_w and Q(w) retain the original numbers. Every level can additionally be required to have modular-k-free binary subset sums. That is a finite condition: all starts and all nonzero steps modulo b, including steps of small additive order, are examined. For such a dictionary every infinite word has k-admissible finite prefixes. The proof reduces each progression modulo its actual lowest radix, subtracts the common original digit, and divides by that radix. No primality assumption is needed.

The principal finite-period theorem holds for every dictionary as defined above. Admissibility is needed only when interpreting its constructions in the Erdős problem.

## 2. The exact cut quotient and its uniform fibre bound

For words u and v, concatenation gives the original numerical quotient

\[
 \pi_{u,v}:H_q(A_u)\times H_q(A_v)\longrightarrow H_q(A_{uv}),
 \qquad (x,y)\longmapsto x+Q(u)y.
 \tag{2.1}
\]

Its source consists of distinct values, and it is onto. Write P=Q(u). The lower image satisfies

\[
 0\le x\le(q-1)(P-1).
\]

In a single fibre the x-values are congruent modulo P. An interval of the displayed width contains at most q-1 such integers. Each x determines y uniquely. Therefore, with C=q-1,

\[
 \boxed{C^{-1}F_q(u)F_q(v)\le F_q(uv)\le F_q(u)F_q(v).}
 \tag{2.2}
\]

The exact loss is the receiving-fibre mean

\[
 \kappa(u,v)=\frac{F_q(u)F_q(v)}{F_q(uv)}\in[1,C].
 \tag{2.3}
\]

Nothing identifies those fibres with singleton fibres. On original free value modules there is the exact sequence

\[
 0\to\ker\pi_{u,v}\to
 \mathbb Q[H_q(A_u)\times H_q(A_v)]
 \xrightarrow{\pi_{u,v}}\mathbb Q[H_q(A_{uv})]\to0.
\]

Choosing one specified original pair per fibre gives a basis of the kernel consisting of differences from that pair. In particular its dimension is F_q(u)F_q(v)-F_q(uv).

The constant C is sharp on the unrestricted canonical source class. Use the singleton generator {1} at radix two for m levels. Its q-ary image is the full interval [0,(q-1)(2^m-1)], with cardinality C2^m-(C-1). Sending both cut lengths to infinity makes (2.3) tend to C. These particular binary sources are not claimed to avoid a fixed progression length at arbitrary depth. Sharpness on a smaller admissible subfamily is a separate question.

### 2.1 A repeated finite word

For fixed w, let a_t=F_q(w^t). Equation (2.2) gives

\[
 C^{-1}a_ta_s\le a_{t+s}\le a_ta_s.
\]

The upper inequality proves existence of eta(w)=lim a_t^(1/t) by subadditivity of the logarithms. Iterating the lower inequality on blocks of fixed length t gives eta(w)>=a_t^(1/t)/C^(1/t). Hence

\[
 \boxed{\eta(w)^t\le F_q(w^t)\le C\eta(w)^t.}
 \tag{2.4}
\]

The image rate of the periodic schedule w^infinity is eta(w)^(1/N(w)). For q=5 the established seven-coordinate matrix M_w represents the same count, and eta(w)=rho(M_w). No spectral calculation is required for the bounds below; all finite F_q(w) values are integers.

## 3. A uniform finite-horizon theorem for all switching words

For each m>=1 define the two explicitly finite quantities

\[
 U_m=\min_{w\in D^m}F_q(w)^{1/N(w)},\qquad
 L_m=\min_{w\in D^m}\bigl(F_q(w)/C\bigr)^{1/N(w)}.
 \tag{3.1}
\]

The minimizing words for the two expressions may differ when rewards differ. They are retained separately.

**Theorem FP1.** Every finite dictionary satisfies

\[
 \boxed{L_m\le\delta_q(D)\le U_m,\qquad
 C^{-1/(mn_-)}U_m\le L_m\le U_m.}
 \tag{3.2}
\]

In particular,

\[
 \boxed{0\le\log U_m-\log\delta_q(D)\le\frac{\log C}{mn_-}.}
 \tag{3.3}
\]

Both L_m and U_m converge to delta_q(D), with this explicit logarithmic error bound.

**Proof.** Split an arbitrary infinite word into successive m-letter blocks w_1,...,w_s and a remainder of length less than m. Iterating (2.2), and retaining the remainder as a higher-level source containing zero, gives

\[
 F_q(w_1\cdots w_s)\ge C\prod_{i=1}^s\frac{F_q(w_i)}C
 \ge C L_m^{\sum_iN(w_i)}.
\]

Appending the remainder cannot decrease the image cardinality. Its generator reward is at most (m-1)n_+, so it does not affect the lower limiting root as s tends to infinity. This proves delta_q(D)>=L_m for every schedule, not just periodic schedules.

Choose a word realizing U_m. Repeating that actual word and applying (2.4) proves delta_q(D)<=U_m. Finally N(w)>=mn_- gives

\[
 \bigl(F_q(w)/C\bigr)^{1/N(w)}
 \ge C^{-1/(mn_-)}F_q(w)^{1/N(w)}.
\]

Taking minima proves the remaining inequality and (3.3). QED.

No convergence of the individual infinite schedule was assumed. The theorem concerns the infimum of lower limits and proves convergence of its finite-horizon bounds.

### 3.1 A priori period length for a prescribed error

For any epsilon>0 choose

\[
 m\ge\max\left\{1,\left\lceil\frac{\log(q-1)}{n_-\epsilon}\right\rceil\right\}.
\]

A word minimizing U_m has a periodic image rate at most e^epsilon delta_q(D). Thus

\[
 \boxed{\delta_q(D)=\inf_{w\ne\varnothing}\eta(w)^{1/N(w)}.}
 \tag{3.4}
\]

This is quantitative periodic approximation. It does not assert that the infimum is attained by a finite period for every dictionary. For q=2, C=1, the image counts multiply exactly and the finite enclosures already coincide.

The rate is a computable real uniformly in the finite integer dictionary: enumerate D^m, evaluate the integer counts, and bracket the finitely many rational powers by dyadic intervals. The logarithmic width has the bound above; moreover 1<=delta_q(D)<=q, which also converts it into a prescribed absolute error. The number of words may be exponential in 1/epsilon, and the integer bit costs retain the actual radices and weights. The result is a terminating approximation theorem, not a polynomial-time claim.

### 3.2 Two-sided arithmetic certificates

For a rational threshold u>0, checking L_m>=u is exactly checking

\[
 F_q(w)\ge C u^{N(w)}\qquad(w\in D^m).
 \tag{3.5}
\]

If u=a/b, this is the integer inequality b^N F_q(w)>=C a^N. A failed global lower threshold u>delta_q(D) eventually produces a word with F_q(w)<u^N; its repeated original block is an explicit strict improvement.

For u<delta_q(D), a sufficient witness horizon is

\[
 m>\frac{\log C}{n_-\log(\delta_q(D)/u)}.
\]

For u>delta_q(D), a sufficient horizon for a periodic improvement is

\[
 m>\frac{\log C}{n_-\log(u/\delta_q(D))}.
\]

The unknown endpoint is not inserted as a computable input to those certificates. The algorithm computes the finite interval first. Equality at the endpoint need not have a finite deciding certificate. Taking max_(j<=m)L_j and min_(j<=m)U_j gives nested valid enclosures if that is desired.

## 4. Controllers, admissibility supports, and the closing cost

Let a finite strongly connected directed controller have s vertices and at least one directed cycle. Every edge carries one of the actual positive-reward canonical levels above. Edges can encode an additional scheduling rule, or the original safe carry-support transfers. In the latter case all edge transfers and acceptance exclusion are part of the finite input certificate. Let

\[
 n_- = \min_e|A_e|,\qquad
 T=\max_e |H_q(A_e)|.
\]

For m>=1, define U_m and L_m as in (3.1), but over all length-m paths inside this controller, retaining their starting and ending vertices. Let delta_G be its optimal lower limiting image rate.

**Theorem FP2.**

\[
 \boxed{
 \log U_m-\frac{\log C}{mn_-}
 \le\log\delta_G
 \le\log U_m+\frac{(s-1)\log T}{mn_-}.
 }
 \tag{4.1}
\]

Moreover a closed directed walk of length at most m+s-1 has periodic image rate at most

\[
 \exp\left(\frac{\log C+(s-1)\log T}{mn_-}\right)\delta_G.
 \tag{4.2}
\]

**Proof.** The lower bound groups a permitted infinite path into its original m-edge pieces, exactly as in Theorem FP1. Choose a path w realizing U_m. Strong connectivity supplies a directed path v from its ending vertex back to its starting vertex with length at most s-1. Retain this path, its actual radices and its generator reward. Then

\[
 F_q(wv)\le F_q(w)F_q(v)\le F_q(w)T^{s-1}.
\]

The repeated closed path has image rate at most F_q(wv)^(1/(N(w)+N(v))). Positivity of the count logarithms gives the upper estimate in (4.1). Combining it with the lower estimate gives (4.2). QED.

If controller vertices are original true-carry supports, a safe cycle can be read periodically from empty true support as well: empty support is contained in its starting support, and every transfer is monotone. This preserves the original binary-feasibility interpretation. It does not delete the initial supported false state or alter a radix.

For a general finite controller, restrict to reachable strongly connected components containing a cycle. Every infinite path eventually remains in one such component, since the component graph is finite and acyclic. An initial finite path changes the logarithmic count by a bounded amount through (2.2), and adds a fixed generator reward. Therefore the optimum is the minimum of the component optima. The bounds above apply separately to those components.

Zero-reward edges require a separate treatment; n_->0 is an explicit domain condition in this theorem. In particular, an active empty-generator reset from earlier work is not silently deleted to satisfy it. The current arithmetic certificates and controller examples all have positive-reward edges.

## 5. Inverse-count sums and a second finite enclosure

For an equal-reward dictionary with n(a)=n_0 and d=|D|, let p be a positive real parameter and put

\[
 Z_m(p)=\sum_{w\in D^m}F_q(w)^{-p}.
\]

These are auxiliary numerical weights, not the original coefficient-word representation measure. Equation (2.2) gives

\[
 Z_m(p)Z_n(p)\le Z_{m+n}(p)\le C^pZ_m(p)Z_n(p).
\]

The pressure limit P(p)=lim_m m^(-1)log Z_m(p) consequently exists and satisfies

\[
 \boxed{
 \frac{\log Z_m(p)}m\le P(p)
 \le\frac{\log Z_m(p)+p\log C}{m}.
 }
\]

Indeed the logarithms are superadditive, while addition of p log C makes them subadditive; the direct division-with-remainder argument proves both bounds.

Writing a_m=min_(w in D^m) F_q(w), there are the literal inequalities

\[
 a_m^{-p}\le Z_m(p)\le d^m a_m^{-p}.
\]

Theorem FP1 gives a_m^(1/(mn_0))->delta_q(D). Hence

\[
 -pn_0\log\delta_q(D)\le P(p)
 \le\log d-pn_0\log\delta_q(D).
\]

Combining the two comparisons yields a completely finite enclosure:

\[
 \boxed{
 -\frac{\log Z_m(p)}{pn_0m}-\frac{\log C}{n_0m}
 \le\log\delta_q(D)
 \le\frac{\log d}{pn_0}-\frac{\log Z_m(p)}{pn_0m}.
 }
 \tag{5.1}
\]

Its width is at most log C/(n_0m)+log d/(pn_0). At integral p, Z_m(p) is an exact positive rational computed from the original image counts. The checks below use exact fractions. The terminology and general theory of almost-additive potentials are established background (Cuneo, 2020); all constants and inequalities used here are proved above.

## 6. Exact finite-length minima in the radix-ten dictionary

Retain the original levels

\[
 \mathsf A=(10,\{1,3\}),\qquad
 \mathsf B=(10,\{2,4\}).
\]

Their binary images are {0,1,3,4} and {0,2,4,6}. A nonzero modular step of order at least five would require five distinct values, and the only nonzero smaller order in Z/10Z is two; neither image contains a pair differing by five. Thus every changing word is five-admissible.

Let

\[
 a_m=\min_{w\in\{\mathsf A,\mathsf B\}^m}|H_5(A_w)|,
 \qquad a_0=1.
\]

**Theorem FP3 (all finite lengths).**

\[
 \boxed{
 a_1=13,\qquad
 a_m=\begin{cases}
 893^r,&m=3r,\\
 93^2\,893^{r-1},&m=3r+1\ge4,\\
 93\,893^r,&m=3r+2.
 \end{cases}}
 \tag{6.1}
\]

Equivalently,

\[
 \boxed{
 \sum_{m\ge0}a_mz^m
 =\frac{1+13z+93z^2-2960z^4}{1-893z^3}.
 }
 \tag{6.2}
\]

This determines the finite minima, not only the limiting minimum already proved in the local-flow note.

### 6.1 Lower bound from the complete cyclic run formula

In the original seven-observation coordinates, the two matrices act by

\[
 M_Af=(3f_0+7f_1,\ 2f_0+8f_1,\ f_0+9f_1,\ f_0+9f_1,
 10f_1,\ 10f_1,\ 10f_1),
\]

\[
 M_Bf=(2f_1+3f_3,\ 4f_1+6f_3,\ f_1+4f_3,\ 3f_1+7f_3,
 4f_1+6f_3,\ 3f_1+7f_3,\ 2f_1+8f_3).
\]

Their product is the literal rank-one matrix uv, where

\[
 u=(17,18,19,19,20,20,20)^{\mathsf T},\quad
 v=(0,2,0,3,0,0,0).
\]

For positive integers a,b, the crossing scalar between A and B runs is

\[
 \theta(a,b)=vM_B^{b-1}M_A^{a-1}u
 =\frac{8\,10^{a+b}+4\,10^b-3}{9}.
 \tag{6.3}
\]

The vectors and row satisfy their original recurrences with polynomial (X-1)(X-10); the four values at a,b in {1,2} verify this formula for every a,b. Cyclically rotating a mixed word preserves its nonzero eigenvalues and exposes the rank-one product. Its radius is the product of the corresponding crossing scalars. A pure word has radius 10^m. The actual count F_5(w) is at least that radius. To see this directly, let a_R=|R| for the original seven shapes, and use the explicitly specified auxiliary norm

\[
 \|x\|_* = \max_R |x_R|/|R|.
\]

The matrix is nonnegative. Its induced norm is max_R (M_w a)_R/|R|. The numerator is the actual count |H_5(A_w)+R|, at most |R| F_5(w), with equality in the singleton coordinate. Hence ||M_w||_*=F_5(w), which bounds its spectral radius. This auxiliary observation norm is not the original generator-word metric.

For a fixed run-pair length L=a+b, the smallest crossing is

\[
 t_L=\theta(L-1,1)=\frac{8\,10^L+37}{9},\qquad L\ge2.
\]

For L>=4,

\[
 \boxed{t_L-93t_{L-2}=\frac{56\,10^{L-2}-3404}{9}>0.}
\]

Therefore replacing a part of length at least four by a part of length two and the remaining length strictly reduces its product cost. Every product is bounded below by one using only length-two parts of cost 93 and length-three parts of cost 893.

The exact inequality

\[
 93^3=804357>797449=893^2
\]

replaces three length-two parts by two length-three parts. Thus a minimizing partition has at most two length-two parts. The three possible length residues give the right side of (6.1). Pure words have still larger radius for m>=2. This proves the lower bound for every finite word.

### 6.2 Attainers with no discarded endpoint cost

The original words BA and BAA have actual aggregate generator sets

\[
 C_2=\{2,4,10,30\},\quad Q_2=100,
\]

\[
 C_3=\{2,4,10,30,100,300\},\quad Q_3=1000.
\]

Their fifth-arity images are exactly

\[
 H_5(C_2)=2[0,92],\qquad H_5(C_3)=2[0,892].
 \tag{6.4}
\]

To verify them, the explicit maps x->x/2 and y->2y transport the two sources to weights {1,2,5,15} and {1,2,5,15,50,150}. At every step a new weight is at most one plus four times the previous weight sum, so the successive q=5 intervals overlap or touch. Their final sums are 23 and 223. This proves (6.4) without replacing the original generators in the construction.

Concatenate any collection of the original macro words BA and BAA. A single division by two on the entire numerical image gives a mixed-radix language with actual digit sets [0,92] and [0,892], respectively. Those digits lie below their original macro radices 100 and 1000. The mixed-radix evaluation is therefore bijective, with its ordinary digit inverse. The original image count is exactly 93^a893^b.

For m=3r use (BAA)^r. For m=3r+1>=4 use BABA followed by r-1 copies of BAA. For m=3r+2 use BA followed by r copies of BAA. These are exactly the counts in (6.1). At length one, B has thirteen values and A has seventeen. Formula (6.2) follows by multiplying the displayed residue-class series by 1-893z^3. QED.

In particular (BAA)^r has exactly 893^r distinct fifth-arity values at every r. The earlier AAB phase has 2301*893^(r-1) values at r periods. These phases share their asymptotic rate, but their original finite image counts differ; the new attainers retain that endpoint information.

## 7. Executed finite evidence

The producer accounts for all length-20 radix-ten words, using exact row/reward aggregation and retaining their literal word multiplicities: 1,048,576 words at the last depth. It checks every finite minimum through length twenty against (6.1), and every explicit attainer through length one hundred. The row/reward aggregation is an exact finite identification: equal rows with the same generator reward have equal numerical counts under every suffix, and their multiplicities add. It is not a sampling procedure.

Two additional dictionaries test unequal rewards and different radices. The first uses A,B and (3,{1}) through length nine (19,683 words at the last depth). The second uses (3,{1}), (5,{1,2}), (23,{1,3,4,7}) through length eight (6,561 words). Every binary modular certificate is verified. Each lower and upper root comparison is made by integer cross-powers, and each displayed decimal substitute is enclosed by exact dyadic endpoints.

The cut and moment-free carrier identities are checked in 120 original generator/radix/arity instances, with 600 complete finite-tail joins for q=2,...,6. The pressure identity has 54 exact fraction checks. Two strongly connected controllers, strict alternation and the three-cycle ABB, have 24 retained path/bridge certificates through length twelve.

The separate auditor imports neither the producer nor its helper. It constructs the seven matrices by interpolation on seven actual symmetric numerical sets, evaluates receiving column vectors rather than prefix rows, and independently covers every stated word domain with exact multiplicities. It also checks 92 actual concatenated generator sets by direct subset-sum construction. Eight corruptions are required to fail: an altered carrier entry, deleted cut factor, wrong reward, missing word depth, false root interval, false attaining count, missing bridge and false pressure ratio.

The theorem is not inferred from the finite run. The finite checks certify the actual matrices, arithmetic counts, witness words and implementation scopes used above. The producer and audit receipts record source identities and their executed domains. No outside human review or new Lean verification is represented by those receipts.

## 8. Relation to the unrestricted target

For a finite modular-k-admissible dictionary, its optimal image rate supplies an upper construction for the unrestricted exponential rate through the previously proved fifth-image capacity bridge. The finite-period theorem gives a quantitative computation of that dictionary value. It does not prove a lower bound for all possible dictionaries.

As the arithmetic family grows, n, b and the actual generator weights remain unbounded. The compact cone-dual work retained on upstream main addresses finite descriptions of strict all-rank lower certificates; the universal block inequalities remain its separate obligation. The present result bounds word length for approximating a specified dictionary, even when an exact finite-period optimizer has not been established. It does not provide a cutoff on the block ranks sufficient for the global infimum.

The exact best rate in the radix-ten dictionary remains 893^(1/6), larger than the existing global k=5 bound. The new complete finite minima and a priori period bounds are structural results, not improved global numerical records.

## References and provenance

Bochi, J., & Morris, I. D. (2015). Continuity properties of the lower spectral radius. *Proceedings of the London Mathematical Society, 110*(2), 477–509. arXiv:1309.0319. The abstract and publication metadata were inspected for context: finite-period attainment is not a generic conclusion for matrix families. No theorem from that paper is needed in the proofs above.

Cuneo, N. (2020). Additive, almost additive and asymptotically additive potential sequences are equivalent. *Communications in Mathematical Physics, 377*, 2579–2595. arXiv:1909.08643. Context for the bounded logarithmic cut defect and pressure terminology; the numerical constants above are derived directly.

Korsky, S. (2026). *Arithmetic progression-free subset-sum sets* (arXiv:2606.24139v1). Context for the original general extremal problem. No new general-rate claim is attributed to that preprint.

The Clankers. (2026, September 16). *Exact local-pattern quotients and switching image capacity*. Original local-flow note in the supplied source archive. Role: preceding matrices and infinite radix-ten optimum; the finite-length minima and uniform dictionary approximation are developed above with complete proofs.

The Clankers. (2026, September 16). *Exact feasible observations, integral positive lifts, and finite-facet capacity certificates*. `research/cone_dual/notes/cone-and-dual.md`, inspected on EP817 main at `578564a5f0c6e3348f5bdc33fd2022b674899c41`. Role: current concurrent all-rank cone-dual interface, preserved separately rather than represented as part of the supplied historical ZIP members.

The original k=4 construction and signed-block proof remain attributed to the anonymous/deleted Reddit contributor. The finite upper-bound Lean extension remains separately attributed to sneed-and-feed.
