# Residue prices and composition-constrained capacity

New research based on integrated EP817 revision
`dbd0a93f2cf935103e88e5c2b2b71fe85ae7537b`.

[Full proofs](notes/residue-and-composition.md) · [Current state](RESEARCH_STATE.md) ·
[Claim inventory](polyclank/claims.json) · [Complete data](certificates/proof_data.json) ·
[Separate audit](certificates/independent_audit.json).

The all-height residue theorem gives the sharp prices 3,5,13,23 for individually
modular-five- or modular-six-free blocks of ranks one through four. Its exact
residue-section injection gives an all-rank generator-profile lower bound.
The finite-composition theorem solves the original radix-ten dictionary at every
letter count and limiting profile, including a regime with an attaining infinite
schedule but no optimal finite period. A general composition LP has uniform
logarithmic error log(q-1)/m per level.

Run the standard-library checks from the repository root:

```sh
python research/residue_composition/certificates/verify_residue_composition.py
python research/residue_composition/certificates/audit_residue_composition.py
```

The second program imports neither the producer nor its helper. Both retain
checks under Python -O. The complete finite domains and proof boundaries are
stated in the note. The included LaTeX is buildable with
`python research/residue_composition/tools/build_reader.py --output continuation.pdf`.

No inherited source is changed. These are ordinary proofs with exact finite
certificates; independent mathematical review remains pending. No new Lean
elaboration, global numerical record, or solution of the unrestricted all-rank
problem is claimed. Original mathematical and formalization credits are retained.
