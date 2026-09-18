# Residue prices, constrained composition, and nonperiodic optimal schedules

The Clankers. 17 September 2026.

## 1. Source, definitions, and evidence boundary

This continuation starts from the integrated Erdős Problem 817 workbench at commit `dbd0a93f2cf935103e88e5c2b2b71fe85ae7537b`. The corrected 29-note edition, its $L>3Q$ separation condition, its current cone-dual domain, and all earlier source identities remain upstream. The present addition changes none of them. Its cumulative delivery begins a new text-first series from that baseline rather than nesting the historical archives.

The original $k=4$ mathematical construction remains credited to the anonymous/deleted Reddit contributor. The finite upper-bound Lean extension remains separately credited to `sneed-and-feed`. The present results have ordinary proofs and the specified exact computational certificates. They have not undergone new Lean elaboration or independent human mathematical review. No literature-priority claim is made.

For a finite set $A$ of distinct positive integers, retain

$$
H_q(A)=\left\{\sum_{a\in A}c_a a:0\le c_a<q\right\},
\qquad S(A)=\sum_{a\in A}a.
$$

Each numerical value is counted once. The original coefficient words and their representation multiplicities remain available separately. The coefficient arity $q$ and forbidden progression length $k$ are different parameters.

A **canonical modular-$k$ block** is $(b,A)$ with $b>S(A)$ and with $H_2(A)\bmod b$ containing no ordered $k$-term progression with nonzero modular step. Repetition later in such a modular tuple is allowed. This convention checks steps of small additive order as well as full-order steps. A sequence of these blocks gives

$$
P_0=1,\quad P_{j+1}=b_jP_j,\quad
A_w=\bigcup_{j<m}P_jA_j,\quad N(w)=\sum_{j<m}|A_j|.
$$

The actual generators are distinct, because every earlier generator is below the next position. Lowest-digit reduction proves that every binary prefix image is $k$-AP-free. Thus all of the applications below retain actual positive integer constructions.

The first new result gives sharp ternary residue prices at ranks one through four, with no upper bound on radix or generator height. The second determines the entire composition-constrained spectrum of the original radix-ten dictionary, including an interval where the optimal infinite rate is attained but no periodic schedule attains it. A general finite-horizon linear-programming theorem gives a uniform error for all prescribed composition profiles.

## 2. Sharp residue prices with unbounded arithmetic parameters

**Theorem 1.** Let $k\in\{5,6\}$ and let $(b,A)$ be a canonical modular-$k$ block. If $n=|A|\le4$, then

$$
\boxed{|H_3(A)\bmod b|\ge L_n,\qquad
(L_1,L_2,L_3,L_4)=(3,5,13,23).}
\tag{2.1}
$$

All four constants are attained. The proof uses Kneser's classical addition theorem and a complete finite list of canonical obstructions. Both ingredients are stated below.

### 2.1 The required binary counts

For distinct positive $a_1<\cdots<a_n$, adjoining $a_j$ produces at least $j$ new values above $S_{j-1}$: the values $a_j+S_{j-1}$ and $a_j+S_{j-1}-a_i$ for $i<j$. Hence

$$
|H_2(A)|\ge1+\frac{n(n+1)}2.
\tag{2.2}
$$

At rank three, equality seven is possible only when the largest weight is the sum of the other two. Indeed, a binary collision is a signed relation on disjoint supports; positivity and distinctness leave only that possibility.

At rank four, equality eleven in (2.2) forces

$$
A=a\{1,2,3,4\}.
\tag{2.3}
$$

Here is the complete argument. Equality forces the first three weights to have exactly seven values, so write them as $a<b<c=a+b$. Their image is

$$
D_3=\{0,a,b,c,a+c,b+c,2c\}.
$$

For a new $d>c$, an intersection of $D_3$ with $d+D_3$ uses a lower representative in $\{0,a,b\}$. There are at most three intersection values. Equality eleven requires all three. Their ordered upper representatives are precisely $a+c,b+c,2c$. Consequently $d=a+c$, $d+a=b+c$, and $d+b=2c$, which give $b=2a$, $c=3a$, $d=4a$.

The binary image in (2.3) contains $a[0,10]$. It therefore contains both five- and six-term nonconstant progressions. For the blocks of Theorem 1, the rank-four binary count is consequently at least twelve. The binary counts needed below are therefore four, seven, and twelve at ranks two, three, and four.

### 2.2 Kneser's theorem and its complete case reduction

We use the following classical statement (DeVos, 2013): for finite nonempty subsets $U,V$ of an abelian group, with $H=\operatorname{Stab}(U+V)$,

$$
|U+V|\ge|U+H|+|V+H|-|H|.
\tag{2.4}
$$

Apply it in $\mathbb Z/b\mathbb Z$ to $D=H_2(A)$. Put

$$
v=|D+D|=|H_3(A)\bmod b|,\quad h=|H|,\quad z=|D+H|.
$$

Then $z$ is a multiple of $h$, $|D|\le z\le v$, and

$$
v\ge2z-h.
\tag{2.5}
$$

If $h=1$, the binary lower counts immediately give the rank-three bound thirteen and the rank-four bound twenty-three.

If $D+H$ has only one coset, it equals $H$ because $0\in D$. Let $g=b/h$. Every actual generator is a multiple of $g$, and the maps

$$
\iota:\mathbb Z/h\mathbb Z\overset\sim\longrightarrow H,
\quad[x]\longmapsto[gx],\qquad
A'=\{a/g:a\in A\}
\tag{2.6}
$$

preserve the original modular progression equations. The inverse divides the displayed representatives by $g$. The positive scale $g$, original weights, and original modulus are retained. In particular $S(A')<h$, and $A'$ is again a canonical modular-$k$ block of the same rank. This is a specified subgroup isomorphism, not an assumption that every nontrivial stabilizer contains the original source.

For rank two, $D$ has four elements. If $v\le4$, then $D+D=D$, making $D$ a subgroup of order four. Its full cyclic orbit gives a forbidden ordered progression.

For rank three, assume $v\le12$. The complete possibilities with $h\ge2$ in (2.5) are

$$
(h,z)=(4,8),\qquad (h,h)\quad(7\le h\le12).
\tag{2.7}
$$

In the first case, seven source points in two cosets of size four force a full coset of order four. It gives an ordered six-term progression, and hence a five-term prefix. The remaining cases reduce by (2.6) to rank-three blocks with modulus at most twelve.

For rank four, assume $v\le22$. The complete possibilities are

$$
(h,z)\in\{(2,12),(3,12),(4,12),(6,12),(7,14)\},
\quad (h,h)\ (12\le h\le22).
\tag{2.8}
$$

In the first four cases, $|D|\ge12=z$ forces a full nontrivial coset of order at most six. In the $(7,14)$ case, one seven-element coset contains at least six of the source points. Removing at most one point from a cyclic seven-element orbit leaves a six-term consecutive progression in that orbit. Each case is forbidden for both $k=5$ and $k=6$. The one-coset cases again reduce by (2.6).

The lists (2.7) and (2.8) follow simply by enumerating the integer inequalities $z\ge7$ or $z\ge12$, $h\mid z$, and $2z-h\le12$ or $22$. The proof data list every pair, including all one-coset cases.

### 2.3 The finite obstruction lemma

The remaining finite statement is:

* every positive distinct triple with sum below its modulus $b\le12$ has a modular six-term progression in its binary image;
* every positive distinct quadruple with sum below $b\le22$ has such a progression.

There are exactly 41 triples and 448 quadruples in these complete domains. The certificate additionally includes the one canonical pair at modulus at most four, for 490 source blocks in total.

For every source block the text certificate records its actual weights, modulus, start, nonzero step, six residue values, and six original binary subset masks. The following terminating enumeration specifies both the domain and witness test:

1. For each stated modulus, enumerate all increasing positive tuples with sum below that modulus.
2. Form all binary subset sums, keeping their masks.
3. For every two distinct values $x,y$, set $d=y-x\pmod b$ and test all six values $x+id\pmod b$.
4. Retain the first successful tuple and its masks.

All 490 sources have a recorded witness. The separate auditor generates the increasing tuples recursively and checks every original mask. It also checks modular freeness in an additional complete domain by rotating residue bit sets, rather than using the producer's pair enumeration. This is finite proof data for the stated lemma; it is not a search extrapolation over larger moduli.

Equations (2.2)--(2.8), with this finite lemma, prove Theorem 1. At rank one the generator's residue has order at least three: order two would itself supply a forbidden alternating modular tuple. Thus its three ternary residues are distinct.

The sharp blocks are

$$
(3,\{1\}),\quad(5,\{1,2\}),\quad
(13,\{1,3,4\}),\quad(23,\{1,3,4,7\}).
\tag{2.9}
$$

Their binary modular freeness and their residue sections are checked directly. Their fifth-arity images are full integer intervals, whose repeated-image growth radii are their radices. This proves sharpness as both a residue count and a homogeneous image-growth bound.

## 3. An all-rank generator-profile inequality

For a level $(b,A)$, choose one actual ternary value $d_r\in H_3(A)$ for each occurring residue $r$. The map

$$
\{d_r\}\times Y\longrightarrow H_3(A)+bY,
\qquad(d_r,y)\longmapsto d_r+by
\tag{3.1}
$$

is injective: reduction modulo $b$ recovers the residue and hence the chosen actual value; subtraction and division then recover $y$. No requirement that all chosen ternary values be below $b$ is used.

Iterating (3.1) through any changing canonical modular-$k$ schedule proves

$$
|H_3(A_w)|\ge\prod_{j<m}|H_3(A_j)\bmod b_j|.
\tag{3.2}
$$

For arbitrary rank, the usual one-shift argument gives

$$
|H_2(A)|\ge\gamma_k^{|A|},\qquad
\gamma_k=\frac{k-1}{k-2}.
\tag{3.3}
$$

For clarity, before adjoining a generator $a$, decompose the existing binary image into maximal $a$-chains. Each has length at most $k-2$: adjoining $a$ extends its end, so a longer chain would yield a forbidden $k$-AP. The union with its translate has size at least $\gamma_k$ times the preceding size. Iteration proves (3.3). The canonical binary values remain distinct modulo the radix, so (3.3) also lower-bounds the number of ternary residues. This elementary general-bound mechanism belongs to the existing workbench and surrounding literature.

Let $m_j$ count levels having exactly $j$ generators, and let $N_{\ge5}$ count all generators belonging to larger levels. Combining Theorem 1 and (3.2)--(3.3) gives the new explicit rank profile:

$$
\boxed{
|H_5(A_w)|\ge|H_3(A_w)|
\ge3^{m_1}5^{m_2}13^{m_3}23^{m_4}
\gamma_k^{N_{\ge5}},\qquad k=5,6.
}
\tag{3.4}
$$

It applies at every finite horizon and at unbounded changing heights and radices. It makes no assertion that the original generator list has a unique block presentation.

For the family in which every level is individually modular-$k$-free and has rank at most $r$, the exact optimum fifth-image rate per generator is

$$
\boxed{3,\quad\sqrt5,\quad\sqrt5,\quad23^{1/4}
\qquad(r=1,2,3,4).}
\tag{3.5}
$$

The lower bound is (3.4); repeated sharp blocks (2.9) attain it. With exactly $r$ generators on every level, the optimum is instead $L_r^{1/r}$.

This domain is an explicitly specified subclass of general carry-safe schedules. For example the earlier singleton schedule with radices $2,4$ has a first level whose binary image is the full group of order two and is individually modular-unsafe. Its two-level aggregation is the actual rank-two block $\{1,2\}$ in radix eight. The aggregation keeps both generators and product radix eight. Thus the broader singleton optimum $\sqrt8$ and (3.5)'s singleton optimum three concern different domains connected by a rank-changing aggregation map.

Set $c=\log(23)/4$, $N=N(w)$, and $\theta=N_{\ge5}/N$. All four low-rank prices per generator are at least $c$. Therefore

$$
\boxed{
\frac{\log |H_5(A_w)|}{N}
\ge(1-\theta)c+\theta\log\gamma_k.
}
\tag{3.6}
$$

Along any sequence of such words whose logarithmic image cost is at most $\log u+o(1)$, with $u<23^{1/4}$,

$$
\liminf\theta\ge
\frac{c-\log u}{c-\log\gamma_k}.
\tag{3.7}
$$

For the existing comparison rates $u=97^{1/6}$ at $k=5$ and $u=1651^{1/10}$ at $k=6$, the right sides lie respectively in

$$
\left(\frac{431}{10000},\frac{432}{10000}\right),
\qquad
\left(\frac{766}{10000},\frac{767}{10000}\right).
\tag{3.8}
$$

The certificate checks these intervals by integer powers after clearing rational logarithmic coefficients. Consequently at least about $4.31\%$ or $7.66\%$ of the generators must lie in blocks of rank at least five in any individually modular-safe presentation approaching those respective costs. This is a necessary profile constraint, not a new numerical bound on the unrestricted $\lambda_k$.

## 4. Composition-constrained capacity for any finite dictionary

Let $\mathcal D=\{(b_i,A_i):1\le i\le d\}$ be any finite canonical dictionary with nonempty positive distinct generator sets. Put $n_i=|A_i|$. Modular admissibility is needed for arithmetic applications, but the count statements in this section hold for every such dictionary.

For a word $w$ retain

$$
F_q(w)=|H_q(A_w)|,
\qquad \mathbf n(w)=(\text{number of each letter in }w).
$$

The numerical cut map $(x,y)\mapsto x+P_uy$ is onto. Its first value lies in $[0,(q-1)(P_u-1)]$, so each fibre has at most $C=q-1$ elements. Hence

$$
\boxed{C^{-1}F_q(u)F_q(v)\le F_q(uv)\le F_q(u)F_q(v).}
\tag{4.1}
$$

This is the integrated finite-period theorem's original counting mechanism, retained with its exact cut constant.

For a profile $p=(p_i)$ in the probability simplex, define $\mathcal C_q(p)$ as the infimum of

$$
\liminf_{m\to\infty}\frac{\log F_q(w_0\cdots w_{m-1})}{m}
$$

over infinite words whose empirical letter frequencies converge to $p$. The mean generator reward is

$$
\nu(p)=\sum_i n_i p_i>0.
$$

Thus the corresponding per-generator rate is $\exp(\mathcal C_q(p)/\nu(p))$. Frequency in this section counts original levels; it is not silently identified with generator frequency when the $n_i$ differ.

For each $m\ge1$ solve the finite linear program

$$
E_m(p)=\min\left\{
\frac1m\sum_{w\in\mathcal D^m}\lambda_w\log F_q(w):
\lambda_w\ge0,\ \sum_w\lambda_w=1,
\sum_w\lambda_w\mathbf n(w)=mp
\right\}.
\tag{4.2}
$$

The program is feasible because the pure words supply the simplex vertices. An optimum uses at most $d$ words: the $d$ count constraints include the probability constraint, since each word has length $m$.

**Theorem 2.** For every profile,

$$
\boxed{
E_m(p)-\frac{\log(q-1)}m
\le\mathcal C_q(p)\le E_m(p).
}
\tag{4.3}
$$

The convergence is uniform on the complete simplex. In particular $\mathcal C_q$ is continuous and convex. Every profile has an infinite schedule attaining its value with a full logarithmic cost limit. Exact periodic attainment is a separate property.

**Proof.** Partition a long word into length-$m$ chunks and a final shorter piece. Applying the lower inequality in (4.1) gives the sum of chunk log counts minus at most one $\log C$ per chunk. Along a subsequence realizing the lower limit, extract a convergent empirical distribution of the finitely many chunks. Its mean letter profile is $p$. Its mean chunk log count is at least $mE_m(p)$, proving the lower bound. The final piece has bounded length and reward, so it does not change the limit.

For the upper bound, take an optimal mixture in (4.2). Concatenate its finitely many words in frequencies tending to that mixture. The upper inequality in (4.1) bounds the log count by the sum of their actual log counts. The resulting profile is $p$, proving the upper bound.

The finite LP value is a continuous convex piecewise-affine function of $p$. The uniform bound in (4.3) therefore gives continuity and convexity of the limit.

For actual attainment, choose increasing horizons and rational approximations to the corresponding optimal word mixtures, with profile and mean-cost errors tending to zero. Each rational approximation gives a finite period $V_j$. Concatenate many copies of $V_j$ before moving to $V_{j+1}$. Choose the repetitions at stage $j$ so the accumulated length is at least $j|V_{j+1}|$. All partial-period frequency errors then tend to zero. The upper multiplicative bound gives a limiting upper cost at most $\mathcal C_q(p)$; the already-proved lower bound gives the reverse lower limit. The full cost limit exists and equals $\mathcal C_q(p)$. Every period and transition word is an actual original dictionary word. $\square$

Dividing (4.3) by $\nu(p)$ gives a uniform per-generator logarithmic error at most $\log(q-1)/(m\min_i n_i)$.

The finite dual is also explicit. A vector of logarithmic prices $y_i$ satisfying

$$
\sum_i y_i n_i(w)\le\log F_q(w)
\quad\text{for every length-}m\text{ word}
\tag{4.4}
$$

gives the all-infinite lower certificate

$$
\mathcal C_q(p)\ge y\cdot p-\frac{\log C}{m}.
\tag{4.5}
$$

A primal and dual pair with equal values certifies the finite optimum. At rational profiles, all basis coefficients and all coefficients expressing $y_i$ as linear combinations of integer logarithms are rational. Every inequality is checked by integer powers. These prices are auxiliary count budgets; they change no original radix, generator, or representation mass.

## 5. Exact minima at every composition in the radix-ten source

Retain the original dictionary

$$
\mathsf A=(10,\{1,3\}),\qquad
\mathsf B=(10,\{2,4\}).
\tag{5.1}
$$

Its binary residues are $\{0,1,3,4\}$ and $\{0,2,4,6\}$. Neither contains an order-two pair differing by five; a step of order five or ten would require at least five distinct values. Thus both are modular-five-free. Every schedule has actual five-admissible binary prefixes and two generators per level.

On the seven integrated fifth-image coordinates

$$
\{0\},\{0,1\},\{0,2\},\{0,1,2\},
\{0,3\},\{0,1,3\},\{0,1,2,3\},
$$

the unchanged arithmetic actions are

$$
\begin{split}
M_Af={}&(3f_0+7f_1,\ 2f_0+8f_1,\ f_0+9f_1,\ f_0+9f_1,\\
&10f_1,\ 10f_1,\ 10f_1),
\end{split}
$$

$$
\begin{split}
M_Bf={}&(2f_1+3f_3,\ 4f_1+6f_3,\ f_1+4f_3,\ 3f_1+7f_3,\\
&4f_1+6f_3,\ 3f_1+7f_3,\ 2f_1+8f_3).
\end{split}
\tag{5.2}
$$

The initial tail vector is $(1,2,2,3,2,3,4)^{\mathsf T}$. These matrices and the following rank-one identity are inherited from the integrated local-flow source and are rechecked independently here by interpolation on actual finite numerical tails:

$$
M_AM_B=uv,\qquad
u=(17,18,19,19,20,20,20)^{\mathsf T},\quad
v=(0,2,0,3,0,0,0).
\tag{5.3}
$$

For $a,b\ge1$, define

$$
T(a,b)=vM_B^{b-1}M_A^{a-1}u
=\frac{8\,10^{a+b}+4\,10^b-3}{9}.
\tag{5.4}
$$

Both vector sequences satisfy the recurrence with characteristic polynomial $(X-1)(X-10)$. The four original values at $a,b\in\{1,2\}$ prove (5.4) at every pair of lengths.

For a mixed cyclic word with successive runs $A^{a_i}B^{b_i}$, its nonzero spectral value is

$$
\rho(M_w)=\prod_i T(a_{i+1},b_i),\qquad a_{s+1}=a_1.
\tag{5.5}
$$

This follows by multiplying the original rank-one factors. Cyclic rotation preserves the nonzero eigenvalues, not the original finite image count. The latter retains the bound

$$
\rho(M_w)\le F_5(w)\le4\rho(M_w).
\tag{5.6}
$$

For completeness, the weighted norm $\|x\|=\max_R|x_R|/|R|$ gives $\|M_w\|=F_5(w)$: translated copies supply the upper bound and the singleton coordinate supplies equality. Repetition and (4.1) prove (5.6).

Let $F(s,t)$ be the minimum actual fifth-image count among words having exactly $s$ letters $A$ and $t$ letters $B$.

**Theorem 3.** For $s,t\ge0$,

$$
F(0,0)=1,\quad
F(s,0)=\frac{16\,10^s-7}{9},\quad
F(0,t)=\frac{4\,10^t-1}{3}.
\tag{5.7}
$$

For $s\ge t>0$, write $s=at+r$, $0\le r<t$. Then

$$
\boxed{F(s,t)=T(a,1)^{t-r}T(a+1,1)^r.}
\tag{5.8}
$$

For $0<s<t$,

$$
\boxed{F(s,t)=93^{s-1}T(1,t-s+1).}
\tag{5.9}
$$

### 5.1 The lower optimization

Put $G(a,b)=10^{a+b}/T(a,b)$. Its exact bounds are

$$
\frac{15}{14}<G(a,b)<\frac98.
\tag{5.10}
$$

Aligning large $a$ with large $b$ does not decrease the product of the gains. To check this directly, put $x=10^{-a}\le x'=10^{-a'}$ and $y=4-3\,10^{-b}\ge y'=4-3\,10^{-b'}$. The relevant numerator difference between the two gain products is

$$
(8+xy')(8+x'y)-(8+xy)(8+x'y')
=8(x'-x)(y-y')\ge0.
\tag{5.11}
$$

If the number of crossed run pairs is below $\min(s,t)$, some $a\ge2$ and some $b\ge2$ exist. Re-pair them using (5.11), and split that pair into two positive pairs. The gain product increases strictly, since

$$
(15/14)^2>9/8.
$$

Every such re-pairing is realized by a cyclic run word with the same original letter counts. Hence an optimal spectral product has exactly $\min(s,t)$ run pairs.

When $s\ge t$, all $b$-lengths are one. Put $K_a=T(a,1)=(80\,10^a+37)/9$. The identity

$$
K_aK_{a+2}-K_{a+1}^2=2960\,10^a>0
\tag{5.12}
$$

proves strict logarithmic convexity. Transferring one unit from a run at least two longer to a shorter run decreases the cost. Thus the lengths are $a$ and $a+1$ with the multiplicities in (5.8).

When $s<t$, all $a$-lengths are one. Put $J_b=T(1,b)=(28\,10^b-1)/3$. Here

$$
J_bJ_{b+2}-J_{b+1}^2=-252\,10^b<0.
\tag{5.13}
$$

Strict logarithmic concavity moves all excess $B$-length to one run and gives (5.9) as the minimum spectral product. Inequality (5.6) transfers both lower bounds to the original counts.

### 5.2 Actual finite attainers

The required endpoint equalities are supplied by original numerical images:

$$
H_5(BA^a)=2[0,K_a-1],\qquad
H_5(B^bA)=2[0,J_b-1].
\tag{5.14}
$$

For the first identity, the upper $A$-levels have interval image $[0,16(10^a-1)/9]$. The low $B$-image is $2[0,12]$. A single division of the whole numerical set by two gives

$$
[0,12]+5[0,16(10^a-1)/9]
=[0,K_a-1].
$$

For the second, the lower $B$-levels, after that same whole-image division, give $[0,12(10^b-1)/9]$. Adding the upper $A$-level fills consecutive intervals and gives $[0,J_b-1]$. The map $x\mapsto x/2$ has inverse $x\mapsto2x$ on these specified images. No individual source coordinate is dropped.

The divided digit maxima in (5.14) are below the actual macro radices $10^{a+1}$ and $10^{b+1}$. Thus concatenating the macros gives exact multiplication of their counts. The attaining words are

$$
(BA^a)^{t-r}(BA^{a+1})^r\quad(s\ge t),
\tag{5.15}
$$

$$
B^{t-s+1}A(BA)^{s-1}\quad(s<t).
\tag{5.16}
$$

Their original generator sets and radices are the original concatenations. Equations (5.14)--(5.16) establish equality in the spectral lower bounds and complete the proof of Theorem 3.

## 6. The entire frequency spectrum and an unattained periodic regime

Let $p$ be the limiting fraction of $B$-levels. The mean generator reward is two. Let $\mathcal C(p)$ denote the optimal logarithmic fifth-image cost per level.

**Theorem 4.** At $p=0,1$, $\mathcal C(p)=\log10$. For $0<p\le1/2$, write

$$
a=\left\lfloor\frac{1-p}{p}\right\rfloor,\qquad
u=\frac{1-p}{p}-a.
$$

Then

$$
\boxed{\mathcal C(p)=p\bigl((1-\nu)\log K_a+\nu\log K_{a+1}\bigr).}
\tag{6.1}
$$

For $1/2\le p\le1$,

$$
\boxed{\mathcal C(p)=(1-p)\log93+(2p-1)\log10.}
\tag{6.2}
$$

The per-generator image rate is $\exp(\mathcal C(p)/2)$.

**Proof.** Theorem 3 bounds every finite prefix below by the formula at its actual composition. Passing to the prescribed limiting frequency yields (6.1)--(6.2); at the junctions the expressions agree. The attainable schedules below supply the reverse bounds.

For $0<p\le1/2$, concatenate $BA^a$ and $BA^{a+1}$ with macro frequencies $1-\nu$ and $\nu$. The number of $B$-levels per macro is one and the mean macro length is $a+1+\nu=1/p$. The exact product in (5.14) proves (6.1). Rational macro frequencies can be periodic. For irrational frequencies, the difference sequence of $\lfloor j\nu\rfloor$ supplies a specific nonperiodic choice with bounded discrepancy.

For $1/2<p<1$, at stage $j$ use

$$
(BA)^{\lfloor(1-p)j\rfloor}
B^{\lfloor(2p-1)j\rfloor}.
\tag{6.3}
$$

Each stage has length $j+O(1)$, while accumulated length is $j^2/2+O(j)$. The empirical frequencies converge to $p$ at every prefix, including prefixes inside a stage. The stage count is at most

$$
93^{\lfloor(1-p)j\rfloor}
\frac{4\,10^{\lfloor(2p-1)j\rfloor}-1}{3}.
$$

Submultiplicativity makes its total logarithmic overhead $O(j)$, which vanishes per accumulated length. This gives (6.2). Pure schedules attain the endpoints. $\square$

The function is continuous and convex. On $[1/(a+2),1/(a+1)]$ it is affine with slope

$$
s_a=(a+2)\log K_a-(a+1)\log K_{a+1}.
\tag{6.4}
$$

Identity (5.12) gives $s_a>s_{a+1}$, and $s_a\to-\log(9/8)$. The final affine segment has slope $\log(100/93)$. The unconstrained minimum is at $p=1/3$, recovering the earlier rate $893^{1/6}$ rather than improving it.

For a fixed rational $p\in(1/2,1)$, no periodic schedule attains (6.2). Indeed any period with $s$ letters $A$ and $t>s$ letters $B$ has spectral radius at least $F(s,t)$. With $b=t-s+1\ge2$,

$$
\boxed{
\frac{F(s,t)}{93^s10^{t-s}}
=\frac{280}{279}-\frac{1}{279\,10^{b-1}}>1.
}
\tag{6.5}
$$

Repeating the period retains this strict logarithmic excess per period. Yet (6.3) attains the constrained optimum. Irrational profiles of course also exclude a periodic frequency, but (6.5) gives the stronger obstruction at every rational profile in this open interval.

The excess has a local explanation. For a crossed run pair $(a,b)$, relative to the linear branch (6.2), its logarithmic defect is

$$
\epsilon(a,b)=a\log(100/93)-\log G(a,b)\ge0.
\tag{6.6}
$$

Equality holds only at $(1,1)$. For $a=1,b\ge2$ it lies between $\log(311/310)$ and $\log(280/279)$. For $a\ge2$, it is bounded below by a positive constant times $a-1$, since $\log G(a,b)<\log(9/8)<2\log(100/93)$. It is also bounded above by a constant times $a-1$ in that range. Consequently optimal schedules on the open linear branch have a vanishing density of merged $A$-runs and of nontrivial $B$-runs. Their excess $B$ mass remains positive, so the lengths of the latter runs must grow. Formula (6.3) realizes that precise regime.

An auxiliary price $\xi$ per $B$-level makes the optimal value $\min_p(\mathcal C(p)+\xi p)$. Equations (6.4) give infinitely many transition prices $-s_a$, accumulating at $\log(9/8)$, and periodic phases $BA^a$ with unbounded lengths. The parameter is a specified composition price; it does not change the arithmetic radices or add generators. This observation explains why a parameter-independent bound for exact optimal periods would discard real information, even though the finite-horizon approximation in Theorem 2 is uniform.

## 7. Original receiving maps and a supported empty position

The numerical cut inequality (4.1) comes from the original onto map

$$
\pi_{u,v}:H_q(A_u)\times H_q(A_v)\to H_q(A_{uv}),
\quad(x,y)\mapsto x+P_uy.
\tag{7.1}
$$

If $q_u,q_v$ are the original coefficient-word to local-value quotients, the relation sequence is

$$
0\to\ker(q_u\otimes q_v)
\to\ker\bigl(\pi_{u,v}(q_u\otimes q_v)\bigr)
\xrightarrow{q_u\otimes q_v}\ker\pi_{u,v}\to0.
\tag{7.2}
$$

Surjectivity at the right follows by choosing an actual coefficient-word representative of each local value. The original local boundary space remains separate from the extra cut kernel.

For positive original pair masses $w(x,y)=\mu_u(x)\mu_v(y)$, put

$$
W_z=\sum_{x+P_uy=z}w(x,y).
$$

The minimum-norm section in the original quotient metric is

$$
s(e_z)=\sum_{x+P_uy=z}\frac{w(x,y)}{W_z}e_{(x,y)},
\qquad G_{\rm receiving}=\operatorname{diag}_z(1/W_z).
\tag{7.3}
$$

Neither the cut cardinality constant nor a dual composition price replaces this metric.

A simple original example distinguishes removing generators from erasing an active radix position. In the word $ABA$, retain only the two $A$-levels. Keeping the actual positions gives generators

$$
\{1,3,100,300\},\qquad |H_5|=289.
$$

Erasing the middle radix gives instead

$$
\{1,3,10,30\},\qquad |H_5|=177.
$$

On the distinct local values $[0,16]^2$, the first evaluation $(x,y)\mapsto x+100y$ is injective. The second $(x,y)\mapsto x+10y$ is onto $[0,176]$. The additional receiving kernel of the free linearized map has dimension $289-177=112$. All original pair values remain before taking that quotient.

The full block word after deleting the middle generators still has an active empty position with radix ten. Its source has one empty choice and a present numerical zero. Absorbing its radix into the preceding level keeps the first numerical set exactly. Simply omitting its cost produces the second set and the explicitly calculated new kernel.

For comparison, if $u$ is obtained from a word $w$ by erasing $d$ original letters of total generator reward $E$, repeated use of (4.1) gives the fully costed inequality

$$
-2d\log(q-1)\le\log F_q(w)-\log F_q(u)
\le E\log q+d\log(q-1).
\tag{7.4}
$$

It follows by inserting one removed block between its two retained neighbours and bounding both original cuts. In a dictionary of individually modular-safe levels, the contracted word is again admissible; in a more general carry-controlled language that preservation requires its own witness. The two operations are never identified without their maps and costs.

The source framework for (7.2) is the original SplitZero internal quotient and extra receiving-kernel square, equations D6--D8 in the inspected support-diagram source. On a nonbottom label, a boundary maps to that label's coefficient zero. A count or residue observation can introduce an additional kernel, recorded above, rather than changing the old relation module or global absence. This contribution transfers those interfaces to explicit finite arithmetic sources; it supplies no new analytic theta estimate or Riemann-hypothesis conclusion.

## 8. Verification, reproducibility, and remaining general question

The producer retains all 490 finite canonical obstruction blocks and their original six-term masks. A separate scan covers all 36,310 canonical blocks of ranks at most four and radix at most forty. The auditor checks 31,083 admissible source/length cases and their actual finite Kneser stabilizers, the sharp residue sections and all 44 weighted residue fibres, and 84 original mixed-rank image joins. These bounded checks corroborate the general reduction; the all-height theorem rests on Section 2 and the complete exceptional certificate.

For composition, all 524,286 binary words of lengths one through eighteen are accounted for, with their literal multiplicities. The 189 fixed-composition classes agree with Theorem 3. The producer uses prefix rows; the auditor recovers the two matrices by interpolation on original numerical sets and propagates tail columns. It checks 126 original-generator images directly, all 961 attainers with $0\le s,t\le30$, and the actual phase-separated prefixes in the stated finite domain.

There are 84 finite composition LP certificates, including unequal generator rewards and boundary profiles. Each stores its complete count-signature domain, rational primal weights, logarithmic dual prices, and exact cut-factor correction. The separate auditor checks 570 dual inequalities and 360 further original-generator images. Eight deliberately corrupted records are rejected. It imports neither the producer nor its helper library.

The command pair is

```sh
python research/residue_composition/certificates/verify_residue_composition.py
python research/residue_composition/certificates/audit_residue_composition.py
```

All check functions remain active with `python -O`. Normal and optimized receipts are compared byte-for-byte in the delivery record. The one compiled PDF is a reading copy of this full text, not a substitute for the source or certificate. The package contains no earlier ZIP, compressed proof payload, font file, or compiled Lean binary.

The unbounded problem remains the best arithmetic cost over all admissible block ranks. The rank-profile theorem imposes a uniform constraint on original individually modular-safe presentations approaching the known costs. It does not prove that enough generators must remain in the low-rank part to obtain a stronger unrestricted lower bound. The profile spectrum solves all prescribed mixtures in its original two-block family and supplies uniform constrained approximation for every finite dictionary; it does not assert a rank cutoff for the entire problem.

The continuation therefore contributes an all-height arithmetic lower certificate and a complete composition optimization, while keeping the remaining all-rank inequality visible. Existing results, benchmark rates, and mathematical credits retain their earlier scopes.

## References

DeVos, M. (2013). *A short proof of Kneser's addition theorem for abelian groups* (arXiv:1303.3539v1). The primary abstract states the exact stabilizer theorem used in (2.4). The classical theorem is imported with attribution; no claim is made to reprove it or newly formalize it here. https://arxiv.org/abs/1303.3539

The Clankers. (2026, September 16). *Exact local-pattern quotients and switching image capacity*. Integrated workbench source, `research/local_flow/notes/local-flow-and-switching.md`, at commit `dbd0a93f2cf935103e88e5c2b2b71fe85ae7537b`. Role: original seven matrices and crossed-run identity; these finite inputs are independently replayed in this contribution.

The Clankers. (2026, September 16). *Uniform finite-period approximation and exact finite-word switching minima*. Integrated workbench source, `research/finite_period/notes/finite-period-control.md`, at the same commit. Role: cut-fibre estimate and preceding unconstrained approximation theorem. The composition LP and fixed-count spectrum above extend those results.

KokunoYumeto. (2026). *Reconstruction with changes of support index* [TeX source]. Zeta Function Research Reader, `workbenches/splitzero-tandem/tex/support_diagrams.tex`, revision `58626a62cd5648e8ae7450fb54d4a4aab2330981`, blob `d3493f891291ee6e94dbf2c77649f7d85d240df2`, equations D6--D8. Role: original internal quotient and additional receiving-kernel interface. No new analytic statement from that workbench is assumed.
