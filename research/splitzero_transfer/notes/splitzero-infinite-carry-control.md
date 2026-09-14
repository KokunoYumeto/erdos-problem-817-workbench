# SplitZero transfer to Erdős 817: uniform carry cohomology and exact mixed-base capacity

14 September 2026. Research contribution by The Clankers, submitted for independent mathematical review.

Erdős 817 base: `23c0110c95b5a2036bdc04a1f352b6e5e27742c8` in `KokunoYumeto/erdos-problem-817-workbench`.

Inspected Zeta source: `42df8a2de002d5fc7090641fac46ea11be05fa71` in `KokunoYumeto/zeta-function-research-reader`. The original support reconstruction, relation quotients, section defects, and source-metric graph formulas are the interfaces used below. The comparison does not import an unproved arithmetic weight estimate.

**Evidence.** The infinite statements have the written proofs below. The accompanying independent integer/rational replay checks the specified finite instances, complete carry-return tables, and controller certificates. No new Lean elaboration is claimed. The existing mathematical attribution of the anonymous/deleted Reddit contributor and the separate Lean contribution of `sneed-and-feed` remain unchanged. These results do not depend on the unformalized variance argument in PR #2.

## 1. Results and exact research objective

For a finite set of distinct positive integers define

\[
 H(A)=\left\{\sum_{a\in U}a:U\subseteq A\right\},\qquad
 S(A)=\sum_{a\in A}a.
\]

The set includes zero. An ordered progression is a tuple \((x,x+d,\ldots,x+(k-1)d)\), and it is nonconstant when \(d\ne0\). An admissible set has no such tuple in its subset-sum image. The extremal function is

\[
 g_k(n)=\min\{\max A: |A|=n,\ H(A)\text{ is }k\text{-AP-free}\}.
\]

The earlier general-k contribution establishes the exponential rate and a cofinal finite-certificate formulation. Section 10 recalls the proof necessary to connect the new results to that original function.

The present continuation proves three types of infinite control.

**Theorem SX1 (uniform relation recovery).** For every sequence of integer radices \(b_j\ge\beta\ge2\), and every finite-dimensional Hilbert coefficient space with its specified metric, the mixed-radix relation operator has an explicit inverse. Its unweighted Hilbert inverse norm is at most \(1/(\beta-1)\), uniformly in radix sequence, truncation length, and coefficient dimension. On the weighted bounded-sequence source defined in Section 4 its inverse has norm at most one, with equality on every nonzero coefficient space. The integral relation condition is retained separately and exactly.

**Theorem SX2 (completion with the original arithmetic observation).** The graph-norm completion of the original finite-support arithmetic complex retains its full coefficient quotient. It has an explicit continuous deformation retraction, including the source homotopy. Forgetting the arithmetic component has precisely that quotient as its kernel. The finite original and graph quotient metrics, their relation-valued section differences, and the complete return cost are calculated in Section 5.

**Theorem SX3 (all-radix fixed-block capacity).** For every nonempty finite set \(A\) of distinct positive integers and every \(k\ge3\), the optimum over *all* infinite canonical mixed-radix constructions made from \(A\) is exactly computable from a finite controller. The radix range needed for that optimum is

\[
 S(A)+1,\ldots,2S(A)+2.
\]

When admissible infinite constructions exist, the optimum is attained by a periodic radix sequence. Its rate is an explicitly computable algebraic number. Section 8 gives the formula and a proof covering arbitrary radix schedules, rather than a bounded search.

Two full applications are obtained. For \(A_* =\{1,4,5,17,21,22\}\), all infinite canonical mixed-radix constructions are classified, and their exact optimal rates are \(97^{1/6}\) for \(k=5\) and \(93^{1/6}\) for \(k=6\). For \(A=\{1,4,8\}\), the exact \(k=5\) optimum is \(280^{1/6}\), attained by alternating radices \(14,20\); the best constant radix is \(19\), with strictly larger rate \(19^{1/3}\).

The latter is an improvement within its specified fixed-block family. The \(A_*\) construction still gives the better global upper bound. The results do not evaluate the infimum over every possible block \(A\), and do not assert a complete resolution of the original extremal problem.

## 2. Original support and integral relation diagrams

### 2.1 The support construction actually used

The Zeta source `formal/splitzero/DERIVED_MATHEMATICS.md`, Sections 1–4, constructs the following object. A diagram of \(R\)-modules \(V_i\), indexed by a join-semilattice with bottom, has total carrier the disjoint union of its fibres. Addition transports both coefficients to the join. The supported scalar zero sends \((i,x)\) to \((i,0)\); the external scalar \(\tau\) sends it to \((\bot,0)\). Natural linear maps and transition-stable relation quotients induce maps on those same reconstructed totals.

Use that construction here with the index set \(\mathbb N_0\), join \(\max\), and the zero module at index zero. At positive index \(m\), use the actual length-m coefficient, relation, and quotient spaces constructed next. Transports in the original complex are zero padding. Thus a relation at length m maps to the quotient's \((m,0)\), not to the bottom label. The identities are fibrewise ordinary linear identities and hence lift through the source's reconstruction functor. No new scalar or definition of homology is introduced.

Fix one entire radix sequence

\[
 b_j\in\mathbb Z,\quad b_j\ge2,\qquad
 P_0=1,\quad P_{j+1}=b_jP_j.
 \tag{2.1}
\]

The uniform estimates later quantify over every such sequence. Incompatible radix prefixes are not silently made comparable support labels.

### 2.2 The zero-endpoint complex over the integers

At length \(m\ge1\), set

\[
 U_m=\mathbb Z^{m-1},\quad V_m=\mathbb Z^m,\qquad
 \varepsilon_m(z)=\sum_{j=0}^{m-1}P_jz_j.
\]

For the interior carries \(c_1,\ldots,c_{m-1}\), set \(c_0=c_m=0\) and define

\[
 (d_mc)_j=b_jc_{j+1}-c_j,\qquad0\le j<m.
 \tag{2.2}
\]

**Proposition SX4.** The following sequence is split exact over \(\mathbb Z\):

\[
 0\longrightarrow U_m\xrightarrow{d_m}V_m
 \xrightarrow{\varepsilon_m}\mathbb Z\longrightarrow0.
 \tag{2.3}
\]

Its displayed integral section is \(a\mapsto(a,0,\ldots,0)\). A relation \(z\) has the unique original primitive

\[
 c_r=P_r^{-1}\sum_{j<r}P_jz_j
 =-P_r^{-1}\sum_{r\le j<m}P_jz_j,
 \qquad1\le r<m.
 \tag{2.4}
\]

**Proof.** Multiplying (2.2) by \(P_j\) telescopes to \(P_mc_m-c_0=0\). If \(\varepsilon_m(z)=0\), the second expression in (2.4) is integral because every \(P_j\) with \(j\ge r\) is divisible by \(P_r\). Subtracting consecutive prefix sums proves (2.2). Starting from \(c_0=0\), that recurrence determines every carry uniquely. Surjectivity and the section are immediate from \(P_0=1\). This proves exactness, including the integer lattice condition. □

The quotient is the original numerical evaluation quotient, not the quotient by an unspecified larger observation kernel. Padding both z and its interior primitive with zeros commutes with (2.2) and preserves (2.4). The induced positive-length quotient transport is the identity on \(\mathbb Z\).

### 2.3 Keeping the terminal carry and its extra quotient

Allow \(c_m\) to vary. The resulting map \(d_m^+:\mathbb Z^m\to\mathbb Z^m\) has diagonal \(b_0,\ldots,b_{m-1}\), subdiagonal \(-1\), and determinant \(P_m\). Its exact sequence is

\[
 0\longrightarrow\mathbb Z^m\xrightarrow{d_m^+}\mathbb Z^m
 \xrightarrow{\varepsilon_m\bmod P_m}\mathbb Z/P_m\mathbb Z
 \longrightarrow0.
 \tag{2.5}
\]

Indeed the same prefix recurrence has integral carries exactly when the total amplitude is divisible by \(P_m\). The terminal identity is

\[
 \boxed{\varepsilon_m(z)=P_mc_m.}
 \tag{2.6}
\]

The map from the original quotient in (2.3) to (2.5) is reduction \(\mathbb Z\to\mathbb Z/P_m\mathbb Z\), with added kernel \(P_m\mathbb Z\). This is the explicit instance of the Zeta source's original-boundary versus further-observation-kernel square.

The augmented systems have *truncation* maps, not the original zero-padding chain maps. For zero padding \(\iota\), the exact defect is

\[
 d_{m+1}^+\iota c-\iota d_m^+c=-c_m e_m.
 \tag{2.7}
\]

Truncating both sides instead gives the commuting inverse-system square and the quotient reduction \(\mathbb Z/P_{m+1}\to\mathbb Z/P_m\).

For every positive divisor \(v\mid P_m\), the original arithmetic boundary term is

\[
 \mathbb Z/v\mathbb Z\overset\sim\longrightarrow
 \ker\bigl(v:\mathbb Z/P_m\mathbb Z\to\mathbb Z/P_m\mathbb Z\bigr),
 \quad[x]\longmapsto[(P_m/v)x].
 \tag{2.8}
\]

If the displayed image vanishes, divisibility forces \(v\mid x\); and every element killed by v is a multiple of \(P_m/v\). This proves both directions, without primality or coprimality. It is the literal integer instance of the BoundarySocle interface described in Zeta PR #30. A kernel element killed by v is sent to its own supported fibre zero.

Complexifying (2.3) gives its ordinary complex coefficient quotient. In contrast, \((\mathbb Z/P_m\mathbb Z)\otimes\mathbb C=0\), since multiplication by \(P_m\) is invertible on \(\mathbb C\). This explicit scalar-extension map kills the torsion quotient. Sections 3–6 therefore retain the integer and complex diagrams separately.

## 3. Integral inverse-limit control and the exact additive defect

Let

\[
 \widehat{\mathbb Z}_{\mathbf b}=\varprojlim_m\mathbb Z/P_m\mathbb Z,
\]

with the actual reduction maps. Give the products of copies of \(\mathbb Z\) their product-discrete topology. Define

\[
 \rho(z)_m=\sum_{j<m}P_jz_j\pmod{P_m}.
\]

**Proposition SX5.** There is a topologically exact sequence

\[
 0\longrightarrow\prod_{r\ge1}\mathbb Z\xrightarrow d
 \prod_{j\ge0}\mathbb Z\xrightarrow\rho
 \widehat{\mathbb Z}_{\mathbf b}\longrightarrow0,
 \qquad(dc)_j=b_jc_{j+1}-c_j,
 \tag{3.1}
\]

where \(c_0=0\). Its kernel identification has the continuous inverse (2.4), using each finite prefix. It has a continuous set-theoretic digit section

\[
 s:\widehat{\mathbb Z}_{\mathbf b}\longrightarrow
 \prod_{j\ge0}\{0,\ldots,b_j-1\}.
 \tag{3.2}
\]

**Proof.** Telescoping gives \(\rho d=0\). If \(\rho z=0\), every prefix sum is divisible by \(P_r\), so (2.4) constructs its unique integral primitive. Every coordinate uses finitely many source coordinates, proving continuity. For a compatible residue sequence, choose representatives in \([0,P_m-1]\). The difference between consecutive representatives is a unique multiple \(P_md_m\), with \(0\le d_m<b_m\). These are the unique digits. They prove surjectivity and the continuous section. The digit domain is compact, its target Hausdorff, and the bijection and explicit inverse are continuous. The section also proves the quotient-topology assertion for \(\rho\). □

The section has the retained additive defect

\[
 s(x)+s(y)-s(x+y)=d a(x,y),\qquad a_r(x,y)\in\{0,1\}.
 \tag{3.3}
\]

The carries are given by ordinary mixed-radix addition with initial carry zero. Since two digits and an incoming carry sum to at most \(2b_j-1\), the next carry is again zero or one. Injectivity of d proves the full cocycle identity

\[
 a(x,y)+a(x+y,z)=a(y,z)+a(x,y+z).
 \tag{3.4}
\]

All maps have their actual product topologies. A continuous group homomorphism from the compact group \(\widehat{\mathbb Z}_{\mathbf b}\) to any coordinate \(\mathbb Z\) has finite image and therefore zero image. Thus the continuous digit lift is correctly represented by (3.3), with its primitive, rather than by asserting additivity.

The terminal condition remains essential. In base two the infinite carry sequence \(c_r=1\), \(r\ge1\), gives

\[
 z=(2,1,1,\ldots),\qquad
 \rho(z)=0,\qquad \varepsilon_m(z)=2^m\quad(m\ge1).
 \tag{3.5}
\]

The truncation map to (2.5) sends these amplitudes to zero modulo \(2^m\); the map to the original integer quotient records \(2^m c_m\). Thus an infinite relation is not substituted for a finite zero-endpoint progression witness. The exact comparison is (2.6).

## 4. Dimension- and radix-uniform inverses on infinite sources

Let E be any finite-dimensional real or complex Hilbert space with its given positive form G. No coordinate Gram is changed. Let

\[
 \mathcal H_E=\ell^2(\mathbb N_0;E),\quad
 (Sx)_0=0,\quad(Sx)_j=x_{j-1}\ (j\ge1),
\]

and let \(B\) be multiplication by \(b_j\), with domain

\[
 \mathcal Y_{\mathbf b,E}=\{x:\sum_j b_j^2\|x_j\|_G^2<\infty\}.
\]

This domain, with norm \(\|Bx\|\), is a Hilbert space even when the radices are unbounded. Under \(x_j=c_{j+1}\), the relation map is exactly

\[
 d=B-S=(I-SB^{-1})B.
 \tag{4.1}
\]

Since \(\|SB^{-1}\|\le1/\beta\), the inverse is

\[
 \boxed{K_{\mathbf b}=B^{-1}\sum_{t=0}^{\infty}(SB^{-1})^t,
 \quad (K_{\mathbf b}z)_j=P_{j+1}^{-1}\sum_{h=0}^jP_hz_h.}
 \tag{4.2}
\]

The operator series converges in norm. Multiplication verifies both inverse laws on the displayed domains. It gives the uniform estimates

\[
 \|K_{\mathbf b}z\|_{\ell^2(G)}\le\frac1{\beta-1}\|z\|_{\ell^2(G)},
 \qquad
 \|BK_{\mathbf b}z\|\le\frac\beta{\beta-1}\|z\|.
 \tag{4.3}
\]

Both follow from the geometric series and \(\|B^{-1}\|\le1/\beta\). Alternatively,

\[
 \|dx\|\ge\|Bx\|-\|Sx\|
 \ge(1-\beta^{-1})\|Bx\|
 \ge(\beta-1)\|x\|.
 \tag{4.4}
\]

These inequalities apply to every zero-extended finite interior carry vector. Their constants do not involve the horizon, any upper bound on the radices, or \(\dim E\). If E is an affine-progression coefficient space, its full Gram remains part of each norm.

Actual infinite digit defects can be bounded rather than square-summable. Define

\[
 \mathcal Z^\infty_{\mathbf b,E}
 =\{z:\|z\|_{\mathbf b,\infty}:=
            \sup_j\|z_j\|_G/(b_j-1)<\infty\}.
\]

The same formula is a bounded isomorphism

\[
 d:\ell^\infty(E)\overset\sim\longrightarrow
 \mathcal Z^\infty_{\mathbf b,E}.
\]

The exact telescoping budget

\[
 \sum_{h=0}^jP_h(b_h-1)=P_{j+1}-1
\]

proves

\[
 \|(K_{\mathbf b}z)_j\|_G
 \le(1-P_{j+1}^{-1})\|z\|_{\mathbf b,\infty},
 \quad\boxed{\|K_{\mathbf b}\|\le1.}
 \tag{4.5}
\]

For nonzero E, equality of the operator norm follows from \(z_j=(b_j-1)e\), for a unit vector e: the inverse is \((1-P_{j+1}^{-1})e\), whose supremum norm is one. The forward bound is at most \((\beta+1)/(\beta-1)\).

These are genuine uniform statements on the entire specified infinite sources. Integrality remains the condition in (3.1); real inverse existence alone does not make its values integral. The relation complex and the admissible digit restrictions meet through the exact carry correspondence in Section 7.

## 5. Completing the original quotient without losing its evaluation class

### 5.1 The comparison kernel of ordinary completion

On finite-support E-valued sequences retain

\[
 \varepsilon(z)=\sum_jP_jz_j.
\]

The complexified version of (2.3) has degree-one quotient E. The ordinary Hilbert completion has the onto map \(d:\mathcal Y_{\mathbf b,E}\to\mathcal H_E\) from (4.2); its degree-one quotient is zero. The explicit comparison is the completion map of complexes, inducing \(E\to0\) on these quotients.

One can see the lost class directly. For fixed \(a\in E\), let

\[
 z^{(N)}=P_N^{-1}e_Na.
\]

Then \(\|z^{(N)}\|=P_N^{-1}\|a\|\to0\), while \(\varepsilon z^{(N)}=a\). The original arithmetic evaluation is discontinuous in the raw Hilbert norm.

### 5.2 The graph-norm completion and its contraction

Retain that observation by using the literal graph map

\[
 j:c_{00}(E)\longrightarrow\mathcal H_E\oplus E,
 \qquad z\longmapsto(z,\varepsilon z),
\]

with norm

\[
 \|z\|_{\rm gr}^2=\sum_j\|z_j\|_G^2+\|\varepsilon z\|_G^2.
 \tag{5.1}
\]

**Proposition SX6.** The completion of this norm is \(\mathcal H_E\oplus E\). Its completed relation complex has quotient E and the explicit contraction

\[
 \widehat d x=(dx,0),\quad
 \pi(z,a)=a,\quad s(a)=(0,a),\quad
 \widehat K(z,a)=K_{\mathbf b}z,
\]

\[
 \boxed{\widehat K\widehat d=I,
 \qquad \widehat d\widehat K+s\pi=I.}
 \tag{5.2}
\]

**Proof.** Given \((u,a)\), truncate u to finite \(u^{(n)}\), and choose \(N>n\) so that
\(P_N^{-1}\|a-\varepsilon u^{(n)}\|<1/n\). Then
\(u^{(n)}+P_N^{-1}e_N(a-\varepsilon u^{(n)})\) tends to u and has evaluation exactly a. Thus the graph is dense in the stated direct sum. On relations its second component is zero. Finite relation primitives are dense in \(\mathcal Y_{\mathbf b,E}\) with norm \(\|Bx\|\), equivalent to \(\|dx\|\) by (4.4) and its upper counterpart. This proves the completed source and map. Both identities in (5.2) follow from the inverse laws in (4.2). □

The completed graph here is a closed linear relation equal to the whole direct sum, rather than the graph of a single-valued closed operator on the old Hilbert space. The forgetful projection

\[
 \mathcal H_E\oplus E\longrightarrow\mathcal H_E
\]

has the exact kernel \(0\oplus E\). It identifies the arithmetic directions erased by the earlier completion. The coefficient zero at a nonbottom support remains that fibre's zero throughout these maps.

### 5.3 Full metrics and the original return cost

At finite length let

\[
 w_m=(P_0,\ldots,P_{m-1}),\qquad W_m=\sum_{j<m}P_j^2.
\]

The least-norm section of the *unchanged* evaluation is

\[
 r_m(a)_j=P_ja/W_m.
 \tag{5.3}
\]

Indeed it has evaluation a, and every zero-amplitude vector is orthogonal to it. For every lift z of a,

\[
 \|z\|^2=\|z-r_ma\|^2+W_m^{-1}\|a\|_G^2.
\]

The raw and graph quotient Grams are therefore exactly

\[
 \boxed{G_m^{\rm raw}=W_m^{-1}G,
 \quad G_m^{\rm gr}=(1+W_m^{-1})G.}
 \tag{5.4}
\]

In particular the return to the original metric retains

\[
 G_m^{\rm raw}=G_m^{\rm gr}-G,
\]

\[
 \boxed{\log\det G_m^{\rm raw}
 =\log\det G_m^{\rm gr}-(\dim E)\log(1+W_m).}
 \tag{5.5}
\]

The determinant correction is fully evaluated in terms of the actual radices. Since every radix is at least \(\beta\),

\[
 P_{m-1}^2\le W_m\le
 \frac{P_{m-1}^2}{1-\beta^{-2}},
 \quad
 0\le\log(1+W_m)-2\log P_{m-1}
 \le\log\left(1+\frac1{1-\beta^{-2}}\right).
 \tag{5.6}
\]

The final upper constant is at most \(\log(7/3)\). Thus the graph splitting has uniform coercivity, while the exact original-metric return still contains twice the logarithm of the accumulated radix product, up to the displayed bounded error. This is the specific cost that a claim of a free extremal improvement would have omitted.

For \(m<n\), padding the old section gives the original-boundary identity

\[
 \iota r_m-r_n=d_nh_{m,n},\qquad
 h_{m,n}=K_{\mathbf b}(\iota r_m-r_n),
\]

where its terminal coordinate is zero and the remaining coordinates are the original finite primitive. Moreover

\[
 \|(\iota r_m-r_n)a\|^2
 =(W_m^{-1}-W_n^{-1})\|a\|_G^2,
\]

\[
 \|h_{m,n}a\|\le
 (\beta-1)^{-1}\sqrt{W_m^{-1}-W_n^{-1}}\,\|a\|_G.
 \tag{5.7}
\]

The graph section converges to \((0,a)\) with error \(W_m^{-1/2}\|a\|_G\le\beta^{-(m-1)}\|a\|_G\). Both convergence and the representative correction are uniform in dimension when measured in the original coefficient metric.

For the actual affine progression coefficients \((u,v)\mapsto(u+iv)_{0\le i<k}\), that metric is

\[
 M_k=\begin{pmatrix}
 k&k(k-1)/2\\
 k(k-1)/2&k(k-1)(2k-1)/6
 \end{pmatrix}.
 \tag{5.8}
\]

Its full cross term is retained in (5.4)–(5.7). A dimension-independent operator estimate in this metric is not an assertion that the embedding into the k coordinates is an isometry for the Euclidean metric on \((u,v)\).

## 6. Typed comparison with the Zeta source, including its remaining kernel

The source inspected in `PGS.tex`, (PGS.3), retains the literal monic polynomial sequence

\[
 \mathcal P_{N-r}\xrightarrow{\times\chi}\mathcal P_N
 \xrightarrow J E=\mathbb C[S]/(\chi),\qquad
 r=\deg\chi,\quad N\ge r-1.
 \tag{6.1}
\]

Use its actual monic remainder section \(r_\chi\) and its original boundary primitive

\[
 q_\chi(P)=\frac{P-r_\chi JP}{\chi}.
\]

Take precisely this E, with any of its specified positive source Grams, as coefficient space in Section 5. There are explicit chain maps from (6.1)'s two-term complex to the graph complex and back:

\[
 F^0=0,\quad F^1(P)=(0,JP),\qquad
 G^0=0,\quad G^1(z,e)=r_\chi e.
 \tag{6.2}
\]

On the graph complex \(FG=s\pi\); its difference from the identity is the original homotopy \(\widehat K\). On the polynomial complex \(GF=r_\chi J\); its difference from the identity is the original division homotopy \(q_\chi\). Specifically,

\[
 q_\chi(\chi Q)=Q,\qquad
 \chi q_\chi(P)+r_\chi JP=P.
 \tag{6.3}
\]

These equations prove a chain-homotopy equivalence to the *specified finite presentation*. Repeated roots and nilpotent directions in E are retained; no eigenbasis or squarefree quotient is used. Coefficient operations commute with the radix operators because the latter act by scalar identities on E. At polynomial degrees, multiplication by S and remainder differ by the displayed \(\chi\)-multiple obtained by division, with the source degree raised when necessary.

For the Zeta source's full observation \(J:\mathscr B\to E\) and its specified section r, the original source complex instead has the explicit decomposition

\[
 [V\xrightarrow\Theta\mathscr B]\longrightarrow
 [V\xrightarrow\Theta\ker J]\oplus[0\to E],
 \quad F\longmapsto(F-rJF,JF),
 \tag{6.4}
\]

with inverse \((u,e)\mapsto u+re\). Here \(J\Theta=0\) and \(Jr=I\), exactly as in the inspected source interface. Its remaining quotient is \(\ker J/\Theta V\). Formula (6.2) compares the E summand; (6.4) retains the complementary source and quotient rather than asserting that a finite observation exhausts the original infinite cohomology.

This is the operative transfer from the workbench: retain supported zeros, use actual boundaries for representative changes, compute the graph-completion comparison kernel, and return the exact metric. The uniform estimates in Section 4 are proved for the new radix operator itself. They are not attributed to a theorem about the unevaluated Zeta arithmetic moments.

## 7. The original digit feasibility problem and mixed-base carries

Take any sequence of finite nonnegative digit sets \(D_j\subseteq[0,b_j-1]\) containing zero. For a fixed horizon m, the literal evaluation map is

\[
 \operatorname{ev}_{\mathbf b}:\prod_{j<m}D_j\overset\sim\longrightarrow
 L_m=\left\{\sum_{j<m}P_jd_j:d_j\in D_j\right\}.
\]

Its inverse is the actual mixed-radix digit expansion. At k rows, define the column map

\[
 \Delta(d)_i=d_{i+2}-2d_{i+1}+d_i,
 \qquad0\le i<k-2.
\]

The square relating column second differences and numerical second differences commutes:

\[
 \Delta\left(\sum_jP_jd^{(j)}\right)
 =\sum_jP_j\Delta(d^{(j)}).
 \tag{7.1}
\]

By (2.3), the right side vanishes exactly when the column-defect sequence has an original integral zero-endpoint primitive. Its recurrence is

\[
 b_jc_{j+1}=c_j+\Delta(d^{(j)}),\qquad c_0=c_m=0.
 \tag{7.2}
\]

This is a fibre-product characterization of the allowed digit tuples with the original relation image. It does not replace that finite feasible set by its linear span.

The bounded-source estimate (4.5), applied to \(|\Delta_i|\le2(b_j-1)\), gives the exact prefix bound

\[
 |c_{r,i}|\le2(1-P_r^{-1})<2.
\]

Every integral carry is therefore in

\[
 \mathcal C_k=\{-1,0,1\}^{k-2},
 \tag{7.3}
\]

independent of every radix and of the horizon. A flag records whether any column has unequal first two digits. Unique mixed-radix evaluation makes this equivalent to inequality of the first two numerical terms. Initial state is \((0,\mathrm{false})\); acceptance is \((0,\mathrm{true})\).

A labeled accepting path evaluates, by (7.1)–(7.2), to an actual nonconstant progression. Conversely each such progression has unique digit rows and the primitive (2.4), and hence determines its accepting path. A zero carry with true flag is an accepting supported state, not an absent state. The all-constant false state remains active.

The original subset multiplicities are available alongside this path correspondence. When \(D_j=H(A_j)\), a column \((d_0,\ldots,d_{k-1})\) has ordered subset-representation multiplicity \(\prod_i\mu_{A_j}(d_i)\). These positive integer edge weights multiply along paths. If only existence is observed, the exact semiring map

\[
 \mathbb N\longrightarrow\{0,1\},\qquad n\longmapsto[n>0],
\]

carries addition to logical OR and multiplication to logical AND. This support observation is applied to the nonnegative path counts, not to an arbitrary signed linear combination. Labels and witness paths remain available before this observation.

### 7.1 Finite dictionaries and all infinite schedules

Let \(\mathcal L\) be a finite dictionary of pairs \(\ell=(b,A)\), with A distinct positive and \(S(A)<b\). The associated digit set is its actual \(H(A)\). The only reachable false-flag state is \((0,\mathrm{false})\): from it a column whose first two digits agree must be entirely constant, since canonical residues determine the subsequent digits in (7.2).

A controller state is thus the set R of reachable true-flag carries. Its deterministic transfer T_l adds the nonconstant initial columns and all successors from R. The state is safe exactly when \(0\notin R\). There are at most

\[
 2^{3^{k-2}-1}
 \tag{7.4}
\]

safe states. Zero padding preserves earlier arithmetic-progression witnesses, so an infinite dictionary schedule is admissible exactly when every controller prefix remains safe.

The graph optimization below is the classical minimum-cycle-ratio mechanism; Karp (1978) treats the mean-cycle setting. Replacing an edge of reward n by a private chain of n edges, with its entire cost on the first edge and zero on the remaining edges, preserves cycle costs and converts reward into ordinary path length. The specialized proof is included here.

Give an edge labeled \(\ell\) cost \(\log b\) and reward \(|A|\). The least achievable limiting inferior cost per generator is

\[
 \rho(\mathcal L)=
 \min_{C\text{ reachable directed simple cycle}}
 \frac{\log\prod_{\ell\in C}b_\ell}{\sum_{\ell\in C}|A_\ell|},
 \tag{7.5}
\]

with value infinity when there is no cycle.

**Proof.** For \(\rho\) equal to the displayed minimum, every cycle has nonnegative sum of \(\log b-\rho|A|\), since a cycle decomposes into simple cycles. Removing cycles from any finite walk leaves a simple path of uniformly bounded length. Its residual sum has a uniform finite lower bound. As the generator reward tends to infinity, this proves the lower limiting bound. Repeating a minimizing cycle after a finite access path attains it. In fact its periodic word alone is safe from the initial state: the transfer maps are monotone, the empty flagged set is contained in the cycle state, and all intermediate cyclic states are safe. □

For a period of length t, let \(Q=\prod_{j<t}b_j\) and

\[
 C=\bigcup_{j<t}P_jA_j.
\]

Its generators are distinct and

\[
 |C|=\sum_{j<t}|A_j|,\qquad
 S(C)\le\sum_{j<t}P_j(b_j-1)=Q-1.
\]

Repeating the period is the literal constant-Q lift of C. Its full carry certificate is safe by the previous path proof. A modular certificate is a further property and is checked separately when used.

## 8. Exact optimization over every radix for a fixed block

Fix A, \(n=|A|\), \(S=S(A)\), and \(D=H(A)\). Allow every sequence of integer radices \(b_j>S\). Define

\[
 \gamma_k(A)=\inf_{\text{all-prefix safe schedules}}
 \liminf_{m\to\infty}\left(\prod_{j<m}b_j\right)^{1/(mn)},
 \tag{8.1}
\]

with empty infimum infinity. Shifting from this product to the largest generator of the actual \((m+1)\)-level prefix changes the denominator from mn to \((m+1)n\) and adds the fixed logarithm of \(\max A\). The limiting inferior rate agrees, including the infinite case.

**Proposition SX7 (finite tail transfer).** For all \(b\ge2S+2\), the complete labeled carry transfer is identical, on every \(c\in\mathcal C_k\).

**Proof.** A column has \(|\Delta_i(d)|\le2S\), so \(|c_i+\Delta_i(d)|\le2S+1<b\). Divisibility in (7.2) is therefore equivalent to \(c+\Delta(d)=0\), and the target carry is zero. Both membership and the target are independent of b; the actual digits and the flag remain unchanged. □

Replace each radix greater than \(2S+2\) by \(2S+2\), retaining its original value in the comparison data. The map between numerical languages is the explicit bijection

\[
 \Psi_m=\operatorname{ev}_{\mathbf b'}
             \operatorname{ev}_{\mathbf b}^{-1}.
 \tag{8.2}
\]

It retains every actual digit word. The full labeled path equations coincide by SX7, so \(\Psi_m\) preserves and reflects the ordered k-AP relation and the constant-tuple relation. It is an isomorphism of these finite relational structures. On generators the map is \(P_ja\mapsto P'_ja\); the induced bijection of chosen subsets commutes with (8.2), including all representation multiplicities. The map is not asserted to be addition on unrestricted integers. The exact accumulated radix cost changes by the specified factor \(\prod_j b'_j/b_j\le1\).

Thus the finite dictionary

\[
 \mathcal L_A=\{(b,A): S+1\le b\le2S+2\}
\]

has exactly the same optimum (8.1). Formula (7.5) proves

\[
 \boxed{\gamma_k(A)=
 \min_{C\text{ reachable simple cycle in }\mathcal L_A}
 \left(\prod_{b\in C}b\right)^{1/(n|C|)}.}
 \tag{8.3}
\]

This is a terminating exact calculation. The digit set, every transition, the reachable subsets, and the finite simple-cycle list can all be enumerated. Cycle comparisons use integer powers, not approximate logarithms. If H(A) is k-AP-free, base \(2S+1\) gives a safe cycle by the second-difference bound; if it contains an integer k-AP, every initial transfer accepts and the cycle set is empty. This proves SX3 for every A.

### 8.1 A periodic construction that improves every constant radix for its block

Take

\[
 A=\{1,4,8\},\quad S=13,\quad D=\{0,1,4,5,8,9,12,13\},\quad k=5.
\]

The exact radix range is 14 through 28. The complete reachable controller has four states and 30 safe edges. Two states have no safe outgoing edge in that range, and SX7 proves that larger radices supply none either. An infinite safe schedule therefore remains in the other two states:

\[
 R_0=\varnothing,\qquad
 R_1=\{(-1,1,-1),(1,-1,1)\}.
\]

The smallest radices on their four possible edge types are

\[
 R_0\to R_0:19,\quad R_0\to R_1:14,\quad
 R_1\to R_0:20,\quad R_1\to R_1:19.
 \tag{8.4}
\]

The receipt retains all 30 edges and all four actual carry sets, not just these minima. Assign the positive potential values \(u(R_0)=7\), \(u(R_1)=10\). Every edge on an infinite path obeys the exact inequality

\[
 b^2u(R')\ge280u(R).
 \tag{8.5}
\]

For the edges 14 and 20 it is equality; for a self-edge it follows from \(19^2>280\). All larger labels preserve the inequality. Multiplying (8.5) over a path gives

\[
 \left(\prod_{j<m}b_j\right)^2
 \ge280^m\frac{u(R_0)}{u(R_m)}
 \ge\frac7{10}\,280^m.
\]

The cycle \(R_0\xrightarrow{14}R_1\xrightarrow{20}R_0\) attains the asymptotic bound. Hence

\[
 \boxed{\gamma_5(\{1,4,8\})=280^{1/6}.}
 \tag{8.6}
\]

Constant radices 14 through 18 have explicit accepting paths, and every radix at least 19 is safe. Their best rate is \(19^{1/3}\), strictly larger because \(280<19^2\).

The period is the actual six-generator block

\[
 C=\{1,4,8,14,56,112\},\quad Q=280,\quad S(C)=195.
\]

It has 64 distinct subset sums. A separate modular enumeration confirms five-term freeness modulo 280. This yields, for every \(n\ge1\), the construction bound

\[
 g_5(n)\le112\,280^{\lceil n/6\rceil-1}.
\]

The result establishes a strict benefit of nonconstant radices for this fixed block; it does not improve the stronger global upper construction from \(A_*\).

## 9. Complete mixed-base classification of the six-generator block

Return to

\[
 A_* =\{1,4,5,17,21,22\},\quad S(A_*)=70.
\]

Its actual 38-digit set is

\[
\begin{split}
D_* = \{&0,1,4,5,6,9,10,17,18,21,22,23,25,26,27,28,30,31,32,\\
        &38,39,40,42,43,44,45,47,48,49,52,53,60,61,64,65,66,69,70\}.
\end{split}
\]

For \(k=5\) and \(k=6\) there is an explicitly checked total section

\[
 r_k:\{-1,0,1\}^{k-2}\longrightarrow D_*^k,
 \qquad \Delta(r_k(c))=-c.
 \tag{9.1}
\]

The complete tables, of 27 and 81 rows respectively, are in the receipt. They are generated deterministically: for each c, enumerate the first two digits a,b in increasing order and extend by

\[
 d_{i+2}=2d_{i+1}-d_i-c_i.
\]

Take the first complete row in \(D_*^k\). Every table entry is then independently checked by literal integer second differences. This specifies the map fully and gives a finite proof certificate for its domain-complete existence; no missing row is treated as an assumption.

Let q>70 have a nonconstant modular k-AP with actual low digits d. Its initial carry is \(c=\Delta(d)/q\in\{-1,0,1\}^{k-2}\). At the next column use \(r_k(c)\). For **every** following radix \(b>70\),

\[
 c+\Delta(r_k(c))=0=b\cdot0.
\]

The resulting two-level integer progression is

\[
 y_i=d_i+q(r_k(c))_i.
 \tag{9.2}
\]

It is nonconstant because distinct low digits below q cannot be canceled by a multiple of q. The receipt gives actual subset masks of the twelve generators for each of its values.

If a bad radix appears at a later level, choose constant zero columns before it and after the returning column. This gives the same witness multiplied by its actual preceding position P_j. Conversely, when every radix has no nonconstant modular k-AP, induction from zero carry leaves only constant columns. Thus:

**Proposition SX8.** An infinite canonical mixed-radix schedule for \(A_*\) is all-prefix k-AP-free, for k=5 or k=6, exactly when every radix is modular-safe for that k.

The finite safe certificates at q=97 for k=5 and q=93 for k=6 imply ordinary integer k-AP-freeness of D_*: a nonconstant progression within [0,70] has a nonzero step modulo those bases. Every radix q>=141 is then safe because an integer second difference has absolute value at most 140, so modular second differences must vanish over the integers. The exact safe lists below 141 are:

\[
\begin{split}
\mathcal B_5\cap[71,140]=\{&97,101,103,105,107,109,127,131,\\
                         &133,134,135,137,139\},\\
\mathcal B_6\cap[71,140]=\{&93,97,101,103,105,107,109,111,117,123,\\
                         &127,129,131,133,134,135,137,139\}.
\end{split}
\tag{9.3}
\]

Two independent modular enumerations verify the lists, including all composite-modulus steps. All 57 unsafe k=5 bases and all 52 unsafe k=6 bases have the explicit witnesses (9.2). Equations (9.1)–(9.3) prove the classification of every infinite schedule, not just the tested finite intervals.

In particular

\[
 \boxed{\gamma_5(A_*)=97^{1/6},\qquad
        \gamma_6(A_*)=93^{1/6}.}
 \tag{9.4}
\]

Nonconstant radix schedules cannot improve these rates for this entire fixed-block family. This conclusion follows from the original digit return section, not merely from a graph-size or norm estimate.

## 10. Return to the full Erdős 817 objective

For completeness the exact bridge to the global rate is as follows. For admissible A,B, set

\[
 A\star B=A\cup(2S(A)+1)B.
\]

The map \((x,y)\mapsto x+(2S(A)+1)y\) is a bijection of actual subset-sum images, with Euclidean division as inverse. Its second-difference identity has first factor bounded by \(2S(A)\), strictly less than the radix. Every progression therefore splits into progressions in both factors. Thus \(A\star B\) is admissible, its cardinality adds, and

\[
 2S(A\star B)+1=(2S(A)+1)(2S(B)+1).
\]

Let \(F_k(n)\) be the least \(2S(A)+1\) for admissible n-element A, with \(F_k(0)=1\). Then \(F_k(m+n)\le F_k(m)F_k(n)\). Writing \(n=t\ell+r\), \(0\le r<\ell\), proves

\[
 \lim_n\frac{\log F_k(n)}n=\inf_{\ell\ge1}\frac{\log F_k(\ell)}\ell.
\]

The exact comparison \(2g_k(n)+1\le F_k(n)\le2ng_k(n)+1\) proves existence of

\[
 \lambda_k=\lim_n g_k(n)^{1/n}
 =\inf_A(2S(A)+1)^{1/|A|}.
\]

Every block A gives the finite capacity (8.3). Repeating its minimizing period gives an original integer construction, so \(\lambda_k\le\gamma_k(A)\). Conversely, the universal radix \(2S(A)+1\) shows \(\gamma_k(A)\le(2S(A)+1)^{1/|A|}\) whenever A is admissible. Therefore

\[
 \boxed{\lambda_k=\inf_{A\ne\varnothing}\gamma_k(A).}
 \tag{10.1}
\]

The earlier full noncanonical carry constructions also have an explicit receiving map into this same optimization. For a valid geometric certificate (b,A) whose prefixes have m|A| distinct generators, retain the actual prefix C_m=union_{j<m}b^jA and send it to (2S(C_m)+1,C_m). Its sum is S(A)(b^m-1)/(b-1), and its cost per generator tends to b^{1/|A|}. The universal second-difference argument proves that receiving modular certificate. Thus the canonical outer infimum represents the rates of those noncanonical constructions through actual finite generator sets, rather than discarding their carry or representation data.

All blocks in this infimum consist of distinct positive integers; the infinity convention covers inadmissible ones. Each individual value \(\gamma_k(A)\) is determined by a terminating finite computation and is attained periodically when finite. The outer class of blocks remains unbounded.

The known general lower and upper bounds in the inspected Korsky paper leave \(\log\lambda_k\) between scales \(1/k\) and \(\log k/k\) for large k. An intended stronger lower scale would require an absolute-c inequality of the form

\[
 \log\gamma_k(A)\ge c\frac{\log k}{k}
\]

for the full class of A in that regime. This is a precisely identified research target, not a premise of SX1–SX8. A violating block and its minimizing cycle would be a finite explicit witness and would give an infinite original generator family through Section 7.

The infinite linear relation source is now uniformly split, its lost completion kernel is reconstructed, its arithmetic metric return is explicit, and every fixed-block infinite radix problem is finite and exactly solved. What is still needed for the full extremal rate is a uniform inequality over the *different digit-feasible subsets* arising as A varies. The graph metric identity (5.5) and the fibre-product equation (7.1) identify the terms that such an argument must retain. No uniform lower bound over those feasible sets follows just by counting the dimensions of their ambient linear quotients.

## 11. Verification and claim-local evidence

Run the standalone standard-library checker:

```sh
python research/splitzero_transfer/certificates/verify_splitzero_transfer.py \
  --output research/splitzero_transfer/certificates/splitzero_transfer_receipt.json
```

The completed run checks 395 finite radix sequences, 1,833 basis-vector identities, 389 exact section secants, full affine-progression Grams at dimensions 3,4,5,6,17, integer original primitives, the weighted-sup telescoping budget, and the finite graph-metric formulas. The sequences include heterogeneous small bases, increasing bases, alternating bases 2 and 97, and rapidly growing integer bases.

The integral quotient suite checks 30,940 addition pairs, 1,260 additive-cocycle triples, 160 boundary-socle instances, the augmented zero-padding defect, and 32 nonterminating-boundary prefixes with nonzero actual amplitudes. The polynomial suite checks 128 monic-division examples on four actual polynomials, including repeated-root and nilpotent cases. Those polynomials are finite calibration inputs, not identified as actual Zeta zero packets.

The A_* suite retains the complete 27-row and 81-row return sections, the 57 and 52 unsafe-base witnesses, actual subset masks, and both full safe-base lists. It checks 800,310 start/step parameters for each progression length in the principal finite interval, plus the stated large-base controls. The following radix in each return identity is tested independently at four different sizes; its full independence is the proof in Section 9.

The fixed-block periodic suite independently enumerates all eight-digit columns to verify 486 complete carry-transition profiles. It retains every state and edge of the four-state controller, all 25 labeled simple cycles, and the integer potential certificate (8.5). It also checks the five smaller constant-base failures, the actual period block, 78,120 modular parameters at base 280, and actual generator prefixes through three levels.

A separate two-letter dictionary, \((2,\{1\})\) and \((6,\{2\})\), checks 510 finite words and its two-state controller. Its safe language forbids two consecutive first letters; the exact optimum is \(\sqrt{12}\), attained by alternating letters. This is a finite heterogeneous-source calibration, not a claimed improvement of the global k=3 bound.

Eight intentionally false formulas must be rejected, including loss of the terminal carry, replacement of a supported zero by absence, omission of the graph term, unjustified integrality of a real primitive, a wrong progression-length claim, and mistaking an infinite congruence boundary for a finite zero. Explicit checks remain active under `python -O`. The normal and optimized runs are byte-identical, and byte-compilation passes. Source and full-receipt hashes are recorded in the accompanying check record.

The ordinary infinite proofs above and these finite tests have different scopes. No finite loop is presented as checking every radix schedule or every Hilbert vector. The complete source identifications, evidence scopes and theorem identifiers are in the claim inventory. No new Lean source is presented as checked; this session has no Lean executable. Existing certificates and the original workbench remain unchanged.

## References and inspected-source roles

The Clankers. (2026, September 12). *SplitZero: Reconstruction, internal homology, and balanced finite jets* [Research and formalization note]. Zeta Function Research Reader, `formal/splitzero/DERIVED_MATHEMATICS.md`, inspected at `42df8a2de002d5fc7090641fac46ea11be05fa71`. Role: the original reconstructed carrier, quotient and transported homology kernel. https://github.com/KokunoYumeto/zeta-function-research-reader/blob/42df8a2de002d5fc7090641fac46ea11be05fa71/formal/splitzero/DERIVED_MATHEMATICS.md

The Clankers. (2026, September 13). *SplitZero integration of residue and period comparisons* [Research note]. Same pinned repository, `workbenches/tau-split-integration/RESEARCH_NOTE.md`. Role: original relation versus additional observation kernel, section primitives and supported quotient maps. https://github.com/KokunoYumeto/zeta-function-research-reader/blob/42df8a2de002d5fc7090641fac46ea11be05fa71/workbenches/tau-split-integration/RESEARCH_NOTE.md

The Clankers. (2026, September 13). *Arithmetic source-metric transfer inside the original SplitZero quotient* [Research note]. Same pinned repository, `workbenches/tau-arithmetic-metric-transfer/RESEARCH_NOTE.md`. Role: full source metrics, least-norm sections, original-boundary secants and retained return costs. https://github.com/KokunoYumeto/zeta-function-research-reader/blob/42df8a2de002d5fc7090641fac46ea11be05fa71/workbenches/tau-arithmetic-metric-transfer/RESEARCH_NOTE.md

KokunoYumeto. (2026, September 14). *The literal phase graph as a weighted source and its exact Schur correction* [Source chapter PGS]. Same pinned repository, `workbenches/splitzero-tandem/continuations/20260914-cumulative-graph/tex/phase_graph_v2/PGS.tex`, equations PGS.3–PGS.10. Role: the actual finite monic presentation and the graph/quotient interface used in Section 6. Source blob `a8360763a065c8122814fc9e79fc1e3b8580ac58`. https://github.com/KokunoYumeto/zeta-function-research-reader/blob/42df8a2de002d5fc7090641fac46ea11be05fa71/workbenches/splitzero-tandem/continuations/20260914-cumulative-graph/tex/phase_graph_v2/PGS.tex

KokunoYumeto. (2026, September 13–14). *Recover mixed-support proofs and retain the full boundary socle* [Draft pull request #30]. Zeta Function Research Reader. Role: inspected algebraic BoundarySocle interface; the integer instance (2.8) is proved independently above. This draft is not recorded as merged into the pinned main. https://github.com/KokunoYumeto/zeta-function-research-reader/pull/30

The Clankers. (2026, September 12). *A global retraction of the original theta complex over the tau base* [Research note]. Same pinned repository, `workbenches/tau-global-retraction/RESEARCH_NOTE.md`. Role: inspected inverse/quotient/graph strategy; no analytic theta estimate is imported into the radix inverse proof. https://github.com/KokunoYumeto/zeta-function-research-reader/blob/42df8a2de002d5fc7090641fac46ea11be05fa71/workbenches/tau-global-retraction/RESEARCH_NOTE.md

Korsky, S. (2026). *Arithmetic progression-free subset-sum sets* (arXiv:2606.24139v1) [Preprint]. Role: the original general-k function, known general benchmarks and outstanding large-k scale. Theorems 1.2, 1.3 and Section 7 were inspected. https://arxiv.org/html/2606.24139v1

Anonymous/deleted Reddit contributor, & The Clankers. (2026, September 13). *The exponential rate for four-term-progression-free subset-sum sets* [Workbench manuscript]. Erdős Problem 817 Workbench, `paper/ep817_k4_rate.tex`, base `23c0110c95b5a2036bdc04a1f352b6e5e27742c8`. Role: original construction attribution and the earlier k=4 work, not a dependency for SX1–SX8. https://github.com/KokunoYumeto/erdos-problem-817-workbench

sneed-and-feed. (2026, September 13). *Formalize finite upper bound theorem and core helper lemmas in Extended.lean* [Pull request #1]. Same workbench. Role: prior checked Lean upper-bound formalization, with separate credit. https://github.com/KokunoYumeto/erdos-problem-817-workbench/pull/1

Karp, R. M. (1978). A characterization of the minimum cycle mean in a digraph. *Discrete Mathematics, 23*(3), 309–311. https://doi.org/10.1016/0012-365X(78)90011-0 . Role: classical finite graph optimization context; publisher metadata and abstract inspected. The specialized cycle proof used here is supplied in Section 7.
