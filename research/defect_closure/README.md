# Defect closure and isolated graphical cores

This add-only continuation proves a general least receiving-relation closure for finite progression sources and an exact positive-distinct integer realization criterion. A complete K_{3,3} binary-switch certificate then gives an all-rank result: disjoint K_4 and K_{3,3} distance cores cannot have binary-value coupling with any remaining generators in a five-admissible set. Original generator values, source masks, relative relations, multiplicities and quotient metrics are retained.

[Full theorem--proof note](notes/closure-and-core-isolation.md). [Independent audit](certificates/independent_audit.json). [Direct reservoir replay](certificates/reservoir_receipt.json).

The numerical consequence for h K_{3,3} cores is

`41*(328^(2h)-1) <= 150*sum(a^2) - 3*sum(part_imbalance^2)`.

The source covariance is `(25/82)*graph_Laplacian - (1/164)*u*u^T`, with `u=(1,1,1,-1,-1,-1)`. This is the uniform distinct-score covariance, not the multiplicity-weighted binary covariance.

The certificate covers 512 orientations, all 5,298 nonzero score differences in 99 exact symmetry orbits, 200 K_4 difference packets, 35 actual multi-core integer witnesses, 592 small closure cases, and 5,285 direct singleton-reservoir extensions. The universal number of cores is handled by the written synchronized-witness proof. A separate standard-library auditor imports neither the producer nor its algebra library. All recorded normal and optimized outputs were byte-identical. No new Lean elaboration is claimed.

Run from the repository root:

```sh
python research/defect_closure/certificates/build_certificate.py
python research/defect_closure/certificates/audit_certificate.py
python research/defect_closure/certificates/verify_reservoir.py
```

The full deterministic certificate is stored losslessly as `proof_data.json.gz`; all values and original orientation masks are present. `gzip.decompress` from Python's standard library recovers its JSON text.

This contribution does not evaluate the unrestricted exponential rate, classify every admissible family into graphical cores, or claim a new global upper-bound record. Its finite-source positive realization bound is not an optimized height estimate. The original anonymous contributor's mathematical credit and sneed-and-feed's Lean credit remain separate. No inherited source or verification receipt is modified.
