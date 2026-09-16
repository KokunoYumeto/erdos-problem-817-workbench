# Supported recurrence control: receiving contribution

This additive continuation proves a uniform positive-gap exclusion theorem, its exact recurrence extremizer, the complete integral short-relation presentation, and an infinite relation inverse with explicit delay dependence. The Pell specialization has no five-term arithmetic progression at any length, while its four-term progression counts have an exact rational generating function. A six-generator motif proves failure of every proposed longer-delay recurrence for progression lengths five through seven.

The source and target maps, including the extra arithmetic-zero directions in Z[1+sqrt(2)], remain explicit. The graph completion retains its arithmetic observation and full original-metric return cost. A nonzero coefficient space is required only for the inverse-norm lower/equality statements; the zero fibre is recorded separately.

**Status:** ordinary mathematical proofs with exact finite certificates; independent mathematical review pending. No new Lean elaboration, global best-rate claim, or literature-priority claim. The general extremal rate remains unevaluated. The original anonymous/deleted contributor's construction and sneed-and-feed's Lean upper-bound formalization retain their distinct attribution.

## Contents

`notes/splitzero-receiving-map.md` is the receiving proof in the original support-diagram and quotient interfaces. The complete EP817 proof and executable evidence are included locally; this directory has no code dependency on the EP817 repository.


The complete proofs are in `notes/recurrence-control.md`. The standard-library producer is `certificates/verify_recurrence_control.py`; the separate auditor is `certificates/audit_recurrence_control.py`. Their stored outputs are `recurrence_receipt.json` and `independent_audit.json`. The auditor imports no producer module. `CHECKS.json` binds their observed output and source identities. `polyclank/source_and_claims.json` gives exact claim scopes and source roles.

## Reproduce

Run from this folder, with Python 3.10 or later:

```sh
python certificates/verify_recurrence_control.py --output certificates/recurrence_receipt.json
python certificates/audit_recurrence_control.py --receipt certificates/recurrence_receipt.json --output certificates/independent_audit.json
```

The same commands with `python -O` retain all checks and reproduce the same respective JSON bytes. The producer does not rely on Python assertions. The source changes required by an edit will change the bound hashes; do not preserve a stale receipt.

The producer's bounded domains include four full algebraic carry graphs, direct arithmetic progression counts through thirteen Pell weights, 2,186 positive-gap sequences, 3,240 triangular basis identities through length eighty, 560 exact finite coercivity vectors, 79 section comparisons, 690 general-delay operator cases, 90 motif applications, and 97,655 literal coefficient words across delays two through six with independently checked scalar-zero prefixes. The separately implemented auditor checks complete labeled graph closure, the correct scalar terminal kernel, arithmetic pairs, 175 finite relation matrices, and eight corruptions. These finite checks corroborate the stated general proofs; they do not replace them.

## Scope of the contribution

No inherited repository source, receipt, Lean dependency, or accepted-status file is changed. This directory is usable independently of unmerged branches. The source-metric comparison to the Zeta workbench is provided in the accompanying receiving payload; its source pointer is recorded here, not treated as a new certification of the Zeta arithmetic estimates.

The new obstruction has a concrete mathematical consequence: a lower-bound method must retain the feasible binary incidence and actual observation, since arbitrary-length five-admissible sources already have a rank-one saturated short-relation quotient and inverse norm 1/2. The seven-term motif supplies an explicit forbidden incidence pattern for faster delay candidates.
