# Canonical arithmetic factors and integral clique isolation

This additive contribution continues the Erdős Problem 817 / SplitZero research programme. It contains complete ordinary proofs, original-mask finite certificates, and a separately implemented arithmetic audit. All new claims remain outside current Lean coverage and are submitted for independent mathematical review.

## Results

The complete-graph source Sigma_m is universally (m+1)-isolating for every m>=2, with every collision class derived by at most floor(m^2/4) integral root steps in the same two-translate source. The triangular-prism source is universally five-isolating; its 314 distinct numerical values supply a new isolated core type. The K3,3 universal-observation theorem keeps three order-two first-round classes and two second-round free classes separately.

Every q-ary digit image has a unique finest original-generator partition, computed from the supports of bounded Graver elements. This use of conformal-minimal integer relations is grounded in the established Graver literature. Certified graph cores are whole binary components; they cannot partially overlap. The actual arity filtration and the additional 84-dimensional ternary receiving kernel in the seven-generator example are retained.

These are structural results. No new unrestricted numerical bound for lambda_5 or lambda_6 is asserted. The canonical remainder and growing higher-arity receiving kernels are not classified by this contribution.

## Files

`notes/canonical-isolation.md` contains all main proofs, exact local cases, quantitative bounds and source roles. `certificates/proof_data.json.gz` contains the complete local graph data and every finite witness. The independent auditor imports neither the producer nor the source library. The extra arity runner computes the full small one-row primitive domains and compares their filtration with direct numerical factorization.

Run from this directory:

```sh
python certificates/build_certificate.py
python certificates/audit_certificate.py
python certificates/verify_arity_filtration.py
```

Explicit checks stay enabled under `python -O`. The uncompressed proof data and input/source hashes are reported in the JSON summaries. Final observed cross-mode and patch/export checks belong to the outer integration receipt, not to an inferred claim from these commands.

## Provenance

The original k=4 construction remains credited to the anonymous/deleted Reddit contributor. sneed-and-feed retains credit for the checked finite upper-bound Lean extension. The preceding delivered `EP817_DEFECT_CLOSURE_20260915` archive is preserved unchanged in the cumulative package. No inherited mathematical file, publication index, Lean source or receipt is changed.

The receiving note `notes/splitzero-receiving-map.md` gives the exact original support/quotient interfaces, retained torsion and free receiving kernels, and metric transport. It imports no new analytic weight conclusion.
