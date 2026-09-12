# Erdős Problem 817: the `k = 4` exponential rate

This is a focused, reviewable workbench for a proof posted to
`r/LLMmathematics` by a contributor whose account was later deleted. The proof
establishes

$$
\lim_{n\to\infty} g_4(n)^{1/n}=19^{1/3},
$$

where `g_4(n)` is the least `N` for which some `n`-element subset of `[N]` has
a subset-sum set containing no nonconstant four-term arithmetic progression.

The construction and proof route belong to the anonymous/deleted Reddit
contributor. The Clankers independently reconstructed the argument, made its
compressed steps explicit, checked it computationally, and formalized its
central algebraic and base-19 components in Lean. This is a result about the
`k = 4` exponential-rate subproblem, not a solution of every part of Erdős
Problem 817 and not an Erdős-Straus artifact.

## Read first

- [Complete human-readable proof](output/pdf/ep817_k4_rate.pdf).
- [TeX source](paper/ep817_k4_rate.tex).
- [Verification status](STATUS.md) - exact ordinary-proof, Lean, computation, literature, and
  novelty status.
- [Checked Lean core](formal/lean/ErdosProblem817/Core.lean).
- [Deterministic finite checks](certificates/verify_ep817.py).
- [Public provenance records](sources/) - no private identity material.

## Credit claim

The moderators retain contemporaneous private mod-mail or notification
evidence of the original Reddit username. The contributor may request any
public attribution they prefer; that private record can be used to validate a
claimant without publishing the deleted username. A claimant can contact the
moderators of r/LLMmathematics by modmail. The proof is theirs.

## Reproduce

The Python certificate requires Python 3.10 or newer and uses only the standard
library. From the repository root:

```console
python certificates/verify_ep817.py --output certificates/certificate_fast.json
python certificates/verify_ep817.py --extended --output certificates/certificate_extended.json
python -O certificates/verify_ep817.py
```

The final command is intentionally expected to fail closed: the validator
checks that Python assertions are enabled. Lean is pinned in
`formal/lean/lean-toolchain` and
`formal/lean/lake-manifest.json`:

```console
cd formal/lean
lake exe cache get
lake env lean ErdosProblem817/Core.lean
```

To rebuild the paper with a TeX distribution containing `latexmk`:

```console
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error ep817_k4_rate.tex
```

The canonical checked copy is then placed at
`output/pdf/ep817_k4_rate.pdf`. Run the machine-state validator from the
repository root after rebuilding any artifact:

```console
python scripts/validate_workbench_state.py
```

## Review posture

The ordinary proof is complete and has been independently reconstructed and
adversarially rechecked; the checkable evidence is the paper, formal module,
and certificates above. Simone Costa's arXiv:2609.06303v1 separately answers
the historical `k = 3` lower-bound question negatively. This `k = 4` workbench
makes no novelty or priority claim. Community review, provenance corrections,
and a public credit claim from the contributor are welcome.
