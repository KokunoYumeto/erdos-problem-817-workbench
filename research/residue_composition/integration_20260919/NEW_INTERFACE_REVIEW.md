# Bounded independent review of the new supported-metric interface

**Result: PASS.** Read the complete `EXACT_SUPPORTED_METRIC_RETURN.tex` and `verify_universal_interface.py`. No defect requiring a mathematical correction was found. This review did not compile the note, rerun the supplied certificates, or modify either reviewed file.

## E6 and support diagrams

For the displayed surjections `q_S: Z[S] -> Z[X_S]` and `p_S = pi_S q_S`, the two complexes have injective differentials, so their degree-minus-one cohomologies vanish. Their degree-zero cohomologies are respectively `V_S/B_S` and `V_S/B'_S`. The explicit least-word lift of each actual value proves that `q_S: B'_S -> ker(pi_S)` is onto, and its kernel is exactly `B_S`. Thus the final isomorphism in E6 follows with the stated integral source and target; no saturation, divisibility, or field assumption is used.

For inclusions of supports, the basis inclusions commute with both evaluations, including newly present actual values and residue classes. Therefore the inclusions of the two kernels and the cochain maps are well-defined. The separate bottom label and the empty support remain distinct labels despite both having zero amplitude group. The all-label zero-amplitude preimage in E8 is precisely the disjoint union of the fibre kernels, while the preimage of the global zero has the bottom label. These are the actual maps asserted in the note, not an identification of a residue class with a zero-amplitude vector. The integral residue-amplitude map sends the basis vector indexed by the residue zero to the zero residue, as stated.

## E11: the original minimum and integral-section determinant

In one residue fibre write `mu_x > 0`, `M = sum_x mu_x`. The quotient minimum of `sum_x |u_x|^2/mu_x` under `sum_x u_x = t` is attained at `u_x = mu_x t/M`. Its orthogonal complement is the coefficient-sum-zero kernel. Subtracting this minimum from the selected integral basis section gives squared defect `1/mu_d - 1/M`; distinct residues have disjoint support. Consequently the diagonal Gram matrices, their determinant quotient, and the squared generalized singular values in E10–E11 are exactly as printed. Empty support causes no inverse of a zero mass and gives the stated empty determinant one.

## E14 and E15: source change

For a fixed old residue set `s_x = mu_S(x)`, `t_x = mu_T(x)`, `a = sum_x s_x > 0`, `b = sum_x t_x > 0`, with zero extension of `s_x` on new values. The difference column is `s_x/a - t_x/b`. Expanding its squared norm in the **new** quotient metric gives

`sum_x (s_x/a - t_x/b)^2/t_x = a^(-2) sum_x s_x^2/t_x - 2/b + 1/b`.

This is E14. Since `0 <= s_x <= t_x`, the remaining sum is at most `a`, giving the stated upper bound `1/a - 1/b`. It is nonnegative because it is the displayed squared norm. Disjoint residue supports prove orthogonality of the columns. The composition law E15 follows by expanding both defects and cancelling the two occurrences of `i_TU s_T bar_i_ST`; every summand has source `bar E_S` and target `ker(pi_U)`. Thus the nonnaturality of the minimum-norm sections is retained quantitatively, rather than ignored. The two-basis-vector integral defect E16 and its norm are also correct.

## Original universal arithmetic maps

E17 follows directly from the original coefficient digits: the unions of the intervals `[3j,3j+4]` and `[2j,2j+4]` produce exactly the displayed original value sets. For each residue, E19 records the actual quotient integer; E20 and its printed inverse are mutually inverse on the full translated tail sets. This holds for arbitrary finite `Y`, including the empty set and tails containing negative integers. The residue fibres are disjoint, so the matrix row counts establish E22 for every such tail, without a symmetry assumption on `Y` and without replacing word multiplicities by distinct-value counts in the metric part.

The independent verifier enumerates all 14 rows and all 140 residue fibres, recording their original quotient values and integer shifts. It checks that every translated support is one of the seven displayed states and that the row counts equal E21. Its checks are explicit and survive optimized Python. E23 follows by multiplying the displayed matrices. The two active-position maps in E24 have image cardinalities 289 and 177, with the explicit fibre-difference basis yielding the free kernel rank 112. The least-norm formula is applied with the retained product word masses.

The verifier's metric checks cover the six displayed ternary blocks and E10–E12. It does not purport to establish E14–E15 by finite testing; those identities have the full general algebraic proofs reviewed above. This evidence scope should remain unchanged.

## Scope of the accepted return

The note gives a concrete supported finite quotient and its exact metrics. It states explicitly that no identifying matrix between this finite residue source and the analytic theta source was supplied or proved. It enters no analytic allocation coefficient or zeta-zero conclusion. The unused larger-rank arithmetic price remains uncomputed. No unsupported RH claim was found. The citations are explicit; this review did not duplicate the parent's separate primary-source check of the Kneser input.
