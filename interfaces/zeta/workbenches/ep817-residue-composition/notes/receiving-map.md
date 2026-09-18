# Supported residue sections and composition-constrained arithmetic costs

This receiving note records the exact maps used in the 17 September 2026 Erdős Problem 817 continuation. It uses the original support-diagram reconstruction and internal quotient at Zeta revision `58626a62cd5648e8ae7450fb54d4a4aab2330981`, `workbenches/splitzero-tandem/tex/support_diagrams.tex`, equations D6--D8. It introduces no replacement scalar, source topology, or definition of homology. The main mathematical proofs and complete finite certificates are supplied in the same delivery under `research/residue_composition/`.

## 1. Original values, modular values, and their different kernels

Fix actual positive distinct weights A, coefficient arity three, and an integer radix b>sum(A). Use free abelian groups on the displayed bases:

$$
V=\mathbb Z[\{0,1,2\}^{A}],\quad
E=\mathbb Z[H_3(A)],\quad
\bar E=\mathbb Z[H_3(A)\bmod b].
$$

The original value map q and further observation pi are

$$
q(e_c)=e_{\sum c_a a},\qquad \pi(e_x)=e_{x\bmod b}.
$$

The exact relation comparison is

$$
0\longrightarrow\ker q\longrightarrow\ker(\pi q)
\xrightarrow{q}\ker\pi\longrightarrow0.
$$

Surjectivity at the right is obtained by lifting each actual value-basis coefficient to an original ternary word. The receiving residue-basis vector e_0 is present. Only its further amplitude in Z/bZ is zero. That amplitude map is Z-linear; no map from Q to a finite field is asserted.

For every occurring residue r, choose the smallest actual ternary value d_r with that residue. Then

$$
\sigma:\bar E\to E,\qquad \sigma(e_r)=e_{d_r},\qquad \pi\sigma=1.
$$

The choice is integral and fully specified. When the admitted original support is enlarged, the selected representative can change. Its defect is

$$
e_{d_r^{\rm old}}-e_{d_r^{\rm new}}\in\ker\pi_{\rm new}.
$$

It need not belong to the old numerical boundary module ker(q): the two actual values may differ by a nonzero multiple of b. The source and receiving kernels remain separated exactly as in the original internal-quotient square.

At each finite admitted support S, take its original word, value, and residue-image bases. Inclusion of supports commutes with q and pi. Their kernels are transport-stable, so the source reconstruction applies. A boundary has its original supported zero at S. An empty admitted word-set has a different label from a nonempty fibre with zero coefficient. The selected sections are not declared natural before their displayed receiving-boundary defects are accounted for.

## 2. A source injection that gives uniform numerical growth

For any actual numerical tail Y, the map

$$
\{d_r\}\times Y\longrightarrow H_3(A)+bY,
\qquad(d_r,y)\longmapsto d_r+by
$$

is injective. Reduction modulo b identifies r and hence the chosen actual value d_r. Subtraction and division by b recover y. The actual representatives are allowed to exceed b. Thus

$$
|H_3(A)+bY|\ge |H_3(A)\bmod b|\,|Y|.
$$

This estimate is an injection of selected original values, rather than an identification of the complete arithmetic quotient with a smaller residue group.

For canonical modular-five- or modular-six-free blocks of rank n<=4, the companion theorem proves that the residue count is at least 3,5,13,23. Kneser's classical stabilizer theorem supplies the all-height reduction. In the one-coset case it produces the exact isomorphism

$$
\mathbb Z/h\mathbb Z\longrightarrow H\subseteq\mathbb Z/b\mathbb Z,
\qquad[x]\longmapsto[(b/h)x].
$$

Every original generator is then divisible by b/h, and division of its actual representative is the inverse. The scale and original modulus remain in the data. Sources meeting several cosets are handled by the full coset counts, not assigned to this one-coset reduction.

The only remaining finite input consists of 490 explicitly listed canonical blocks with actual six-term subset-mask witnesses. The main note distinguishes that finite evidence from the general Kneser argument. No new Lean proof is claimed.

## 3. The original metric of residue observation

Let mu(x) be the number of original ternary words with actual value x. The original orthonormal word metric induces the diagonal quotient metric

$$
G_E=\operatorname{diag}_x(1/\mu(x)).
$$

Set mu_bar(r)=sum_{x mod b=r} mu(x). The least-norm residue section is

$$
s(e_r)=\sum_{x\bmod b=r}\frac{\mu(x)}{\bar\mu(r)}e_x,
\qquad G_{\bar E}=\operatorname{diag}_r(1/\bar\mu(r)).
$$

It has pi s=1 and is orthogonal to ker(pi). The integral section sigma in Section 1 need not be the least-norm section. Its actual boundary difference remains in ker(pi), and the complete Pythagoras equality is

$$
(\sigma v)^*G_E(\sigma v)
=v^*G_{\bar E}v+
((\sigma-s)v)^*G_E((\sigma-s)v).
$$

The cardinality injection does not set this boundary norm to zero or replace the original masses by unit value weights.

## 4. A general cost theorem independent of the arithmetic presentation

Let a finite alphabet have positive integer rewards n_i and a function F on finite words with F(empty)=1 and

$$
C^{-1}F(u)F(v)\le F(uv)\le F(u)F(v),\qquad C\ge1.
$$

Retain the alphabet and all of its labels even when a target frequency p_i is zero. For each probability profile p, the companion theorem constructs the constrained logarithmic cost C_F(p). Its finite-horizon LP is

$$
E_m(p)=\min\frac1m\sum_w\lambda_w\log F(w),
\qquad
\lambda_w\ge0,\quad\sum_w\lambda_w=1,
\quad\sum_w\lambda_w\mathbf n(w)=mp.
$$

The exact comparison is

$$
E_m(p)-\frac{\log C}{m}\le C_F(p)\le E_m(p).
$$

It follows by grouping every word into actual length-m pieces, retaining the factor C at every cut, and realizing the optimal finite word mixture by a deterministic concatenation. Uniform convergence gives a continuous convex profile function. Diagonal concatenation supplies an attaining infinite word. Dividing by the actual mean reward sum_i n_i p_i gives the per-generator cost; it does not change the frequency parameter to an unrecorded generator distribution.

The arithmetic instance has F(w)=|H_q(A_w)| and C=q-1 from the original cut quotient. Its finite logarithmic prices are an observation of complete numerical counts, not an action on the original word amplitudes or a reweighted arithmetic source.

The two-level example obtained by deleting the middle generators of ABA illustrates the difference. Keeping its active radix position gives {1,3,100,300} with 289 fifth values. Erasing that position gives {1,3,10,30} with 177 fifth values. The map on local values [0,16]^2 has an added 112-dimensional receiving kernel. The first retained zero position has a genuine arithmetic cost and is not global absence.

## 5. Scope of the return

The residue prices impose explicit all-rank generator-profile constraints on individually modular-safe block presentations. The radix-ten application computes the full constrained spectrum and proves that no finite period is optimal when the B-frequency is strictly between one half and one, even though a specified infinite schedule attains the value.

The return is algebraic and combinatorial. The theta source, its original relations, its infinite observation kernel, and its analytic metric estimates are not replaced by these finite examples. This contribution neither supplies the remaining all-rank Erdős lower bound nor asserts a result about zeta zeros.

## Sources

DeVos, M. (2013). *A short proof of Kneser's addition theorem for abelian groups* (arXiv:1303.3539v1). https://arxiv.org/abs/1303.3539 . Role: classical stabilizer theorem; the general source theorem is imported with attribution.

KokunoYumeto. (2026). *Reconstruction with changes of support index*. The original pinned source and equations are identified at the beginning of this note.

The Clankers. (2026, September 17). *Residue prices, constrained composition, and nonperiodic optimal schedules*. Supplied EP817 continuation, based on integrated commit `dbd0a93f2cf935103e88e5c2b2b71fe85ae7537b`.
