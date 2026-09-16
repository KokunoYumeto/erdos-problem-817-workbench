# Exact higher-arity images and retained boundary defects

This add-only continuation calculates the original higher-arity images of the existing base97, base93, and base1651 constructions. It preserves their generator sets, representation fibres, original quotient metrics, and finite/infinite observation maps.

[Complete theorem–proof note](notes/arity-and-boundary.md) · [Exact arithmetic receipt](certificates/arity_boundary_receipt.json) · [Independent audit](certificates/independent_audit.json) · [Claim inventory](polyclank/claims.json).

## Results

For every number m of blocks, the distinct ternary images have cardinalities

- `(68*97**m - 21*3**m)/47` for `{1,4,5,17,21,22}` in base97;
- `(68*93**m - 23*3**m)/45` for the same block in base93;
- `(1007*1651**m - 226*89**m)/781` for `{3,4,7,34,37,41,216,250,253,257}` in base1651.

The ten-generator four-valued image has the exact visible term `-(2*m/3)*3**m`, arising from an actual size-two primary block, not an assumed numerical fit. The arity-six image is an interval with exactly six retained semigroup boundary holes, at every positive block length. The six-generator image is already a full interval at arity four.

General finite theorems compute every distinct-image moment, interval-run merger, actual representation peak, and real-limit progression witness. The ternary added relation spaces are explicitly exponentially large. The original maximum ternary multiplicities are exactly `15**m` and `219**m`, so the original quotient-to-unit-value return norms are retained.

The associated real limits contain explicit rational progressions despite freeness of every finite integer stage. Each finite prefix retains the same nonzero integer second difference. A finite graph decides the real-limit question; the additional terminal observation records what a plain scaled limit forgets.

These results do not improve the unrestricted numerical record or evaluate the all-block extremal infimum. Their purpose is to calculate the higher-arity loss and boundary return precisely enough for subsequent uniform arithmetic arguments.

## Reproduce

From this directory:

```sh
python certificates/verify_arity_boundary.py --output /tmp/arity_receipt.json
python certificates/audit_arity_boundary.py --input /tmp/arity_receipt.json \
  --output /tmp/arity_audit.json
```

The programs use only the Python standard library. The second imports neither the producer nor its core implementation. Complete residue transitions, source multiplicities, recurrence certificates and boundary masks are in the generated receipt. The default and optimized executions agree byte-for-byte. See the enclosing contribution's integration record for the actual observed run scope.

## Evidence and provenance

All universal claims have written proofs. The supplied finite record certificates have been independently replayed by a different arithmetic implementation. No new Lean elaboration or external mathematical review is claimed. The predecessor canonical-isolation archive is retained unchanged in the cumulative delivery; its entire historical verification is not rerun by these programs.

The original k=4 construction remains attributed to the anonymous/deleted Reddit contributor. sneed-and-feed retains the separate finite-upper-bound Lean credit. The new notes do not change those attributions or existing source hashes. No private identity evidence or raw private transcript is included.
