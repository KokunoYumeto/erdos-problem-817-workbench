# Feasible observation cone and finite-facet arithmetic capacity

[Complete proof](notes/cone-and-dual.md) · [Producer](certificates/verify_cone_dual.py) · [Independent auditor](certificates/audit_cone_dual.py) · [Source and claim ledger](polyclank/source_and_claims.json)

The seven numerical-image coordinates have an exact feasible cone with nine facets and ten integral extreme rays. Every actual block matrix lifts to nonnegative integral ten-coordinate coefficients, with its rank-three kernel and composition defect retained. The full all-rank arithmetic dual admits a finite rational piecewise-linear certificate at every strict subcritical threshold; its denominator and piece-count bounds are explicit. The universal arithmetic block inequalities remain to be verified at a new useful numerical threshold.

The two actual five-admissible levels ({3,13},23) and ({1,4},23) have exact optimal switching image growth sqrt(285) per level, attained by alternation. A two-piece potential proves it. An exact positive identity excludes every strictly positive linear potential at 84/5. This is a mechanism and a complete two-letter result, not a new global numerical record.

## Reproduce

Run inside this directory with Python 3.10 or later; only the standard library is required:

```sh
python certificates/verify_cone_dual.py
python certificates/audit_cone_dual.py
```

The producer generates `certificates/cone_proof.json`, containing the complete original residue labels, cycles, matrices and finite cone certificates. The auditor reads that generated proof. Its SHA-256 is `751f89b55161ef32b19c148628e46e100255c2a58ffebaf71cb5e11e905aa1c8`. The full file is included in the downloadable cumulative archive; the repository contribution may regenerate it instead of duplicating the large JSON. The committed receipts bind both implementations and the generated data. No finite enumeration is substituted for the all-rank proofs.

The final producer and independent auditor pass normally and under `python -O` with byte-identical respective outputs. The auditor imports no producer or helper. Exact checks cover all 19 simple word cycles, the complete cone, 2,044 original symmetric sources, 1,191 actual block/radix instances, selected integral lifts and cocycles, and all 16,383 two-letter words through length thirteen. The separate audit reconstructs the cone and selected matrices from literal numerical sets; its precise domain is in its receipt.

## Boundaries and attribution

These are ordinary mathematical proofs and exact finite computations submitted for independent mathematical review. No new Lean elaboration is claimed. Nothing in this addition changes earlier accepted statements or receipts. The original k=4 construction remains credited to the anonymous/deleted Reddit contributor, and sneed-and-feed retains separate credit for the existing finite upper-bound Lean extension.

The source observation does not decide binary eligibility: ({1,3,4,7},31) and ({1,2,4,8},31) have the same seven-matrix and reward but different binary progression behavior. The original arithmetic certificate and word-fibre metrics remain attached. The unbounded block family has not been eliminated by the finite-facet theorem.
