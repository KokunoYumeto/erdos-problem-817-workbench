# Residue prices and exact supported metrics

[Complete supplied paper](../notes/residue-and-composition.md) ·
[Original reading PDF](../continuation.pdf) ·
[Original LaTeX](../latex/main.tex) ·
[New complete metric proof](EXACT_SUPPORTED_METRIC_RETURN.tex) ·
[Result index](RESULTS.json)

The supplied continuation proves the sharp ternary residue prices 3, 5, 13 and
23 for individually modular-five- or modular-six-free blocks with one through
four generators, with unrestricted heights and radices. It also evaluates every
finite composition and every limiting letter frequency in the original
radix-ten dictionary A=(10,{1,3}), B=(10,{2,4}). For B-frequencies strictly
between one half and one, an explicit infinite schedule attains the constrained
optimum while every finite period has a strict excess.

The new metric note gives the original supported cochain complexes and their
receiving-kernel map. It evaluates the integral residue-section determinant
loss with every original word multiplicity, proves the exact source-enlargement
boundary norm and composition law, and derives the seven count matrices from
all literal residue-fibre maps for arbitrary finite numerical tails.
The full proofs are in the linked LaTeX; the result index gives their equation
locations and the precise receiver of each result.

Martin Kneser's addition theorem is used through
[Matt DeVos's primary proof](https://arxiv.org/abs/1303.3539v1).
The original anonymous/deleted contributor's construction credit and
sneed-and-feed's separate Lean-formalization credit remain in the full paper
and repository introduction.

## Verification and preservation

The producer and independently implemented arithmetic auditor passed in ordinary
and optimized Python. Their mathematical data agree with the supplied certificate:
490 exceptional modular blocks, 189 composition classes through length 18,
961 finite attainers, and 84 exact LP certificates. The supplementary verifier
retains all 140 original residue fibres and 58 weighted fibres in the six
displayed ternary sources. The new cochain and metric proofs were independently
read; their full algebraic arguments do not rely on finite testing.

The intake found that the original auditor did not reject deletion of a complete
length record. The supplied certificate contains the complete domain. The added
scope guard now requires all lengths 1 through 18 and every advertised composition
and LP case, and rejects a deliberately truncated copy. The original auditor and
all supplied source files remain byte-for-byte preserved. Source identities,
the exact portability changes, and checks are recorded in
[SOURCE_LINEAGE.json](SOURCE_LINEAGE.json) and [VERIFICATION.json](VERIFICATION.json).

From the repository root:

    python research/residue_composition/integration_20260919/scope_guard.py
    python -O research/residue_composition/integration_20260919/scope_guard.py
    python research/residue_composition/integration_20260919/verify_universal_interface.py

To rerun the original arithmetic programs without replacing historical evidence,
select output files outside the source tree:

    python research/residue_composition/certificates/verify_residue_composition.py --output PROOF_REPLAY.json
    python research/residue_composition/certificates/audit_residue_composition.py --proof PROOF_REPLAY.json --output AUDIT_REPLAY.json

The original 12-page PDF is preserved; no older edition was rebuilt.
No new Lean execution is claimed.

The unrestricted higher-rank arithmetic price remains uncomputed. The supported
finite quotient has an exact algebraic and metric realization; these results
establish no new analytic theta allocation coefficient or zeta-zero theorem.
