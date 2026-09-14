# SplitZero transfer and exact mixed-base capacity

This add-only research continuation applies the inspected Zeta workbench's original support, quotient, graph-completion and source-metric interfaces to Erdős Problem 817. It preserves the integer relation lattice and the actual subset-sum images.

[Full mathematical note](notes/splitzero-infinite-carry-control.md) · [Executable verifier](certificates/verify_splitzero_transfer.py) · [Claim and source inventory](polyclank/source_and_claims.json) · [Observed checks](polyclank/checks.json).

## Mathematical outcome

For every integer radix sequence bounded below by two, the original carry relation has an explicit inverse with uniform Hilbert bound 1/(beta-1), and weighted-sup bound one. Its integral quotient, additional terminal residue quotient, bounded section cocycle and boundary-socle maps are all retained. The actual arithmetic graph completion has a continuous contraction and keeps the quotient that the ordinary Hilbert completion erases.

The finite quotient metrics are exactly G/W and (1+1/W)G. Their full original-metric return cost is retained. The note gives a chain-homotopy equivalence to the Zeta source's literal finite monic presentation, without removing its full infinite observation kernel or claiming an arithmetic weight bound.

For every fixed generator block A and every k>=3, optimization over **all infinite canonical mixed-radix schedules** is an exactly computable finite-cycle problem. Every radix at least 2*sum(A)+2 has the same labeled transfer; the finite dictionary and its carry controller give the exact optimum, attained periodically when finite.

The block {1,4,8} has exact k=5 optimum 280^(1/6), attained by the period (14,20), strictly better than every constant radix for that block. A four-state controller and the integer potential (7,10) prove optimality. This does not improve the best global k=5 upper bound.

The six-generator block {1,4,5,17,21,22} has a complete all-radix classification for k=5 and k=6. Its exact mixed-radix optima are 97^(1/6) and 93^(1/6). All 27 and 81 carry-return primitives are explicit. Every disallowed radix has an actual two-level progression witness, independently of the following radix.

The global rate is the infimum of these exactly evaluated fixed-block capacities. The outer family of blocks is still unbounded. No complete solution of Problem 817 or proof of the Riemann hypothesis is claimed.

## Reproduce the exact checks

From the repository root:

```sh
python research/splitzero_transfer/certificates/verify_splitzero_transfer.py \
  --output research/splitzero_transfer/certificates/splitzero_transfer_receipt.json
```

The plain full receipt is in the downloadable contribution bundle. The repository also preserves it losslessly as `certificates/splitzero_transfer_receipt.json.gz`; Python's standard `gzip` module decompresses it. [Finite proof data](certificates/finite_proof_data.json) exposes the complete returning sections, safe-base lists, controller states and edge labels directly. `polyclank/checks.json` binds the verifier, note, proof data and full receipt by SHA-256.

Normal and optimized Python runs have byte-identical output; byte-compilation passes. The finite proofs include 395 radix sequences, 1,833 basis identities, 389 section secants, 30,940 addition pairs, 1,260 cocycle triples, 160 socle instances, 128 monic-division cases, 108 carry-return rows, 109 bad-base witnesses, 486 complete edge profiles, all 25 applied periodic cycles, and eight rejected false formulas. The note specifies the exact domains.

**Formalization boundary:** these are written proofs and exact finite computations, submitted for independent review. No new Lean elaboration was performed. The finite examples involving monic polynomials are calibration inputs, not certified arithmetic zero packets. No inherited Lean files or receipts are changed.

## Source and collaboration record

Erdős 817 main was inspected at `23c0110c95b5a2036bdc04a1f352b6e5e27742c8`. The Zeta workbench was inspected at `42df8a2de002d5fc7090641fac46ea11be05fa71`, including the original reconstruction/internal-quotient note, split-integration square, source-metric transfer, global retraction, and PGS graph source. Zeta PR #30 was read for its BoundarySocle interface; it is not represented as merged into that main source.

The earlier variance PR #2 and general-k PR #3 remain separate. The latest user-delivered local general-k package was also used to inspect its canonical carry implementation. The new verifier is standalone and imports none of those files. The necessary global rate interface is proved again in Section 10.

The original k=4 construction remains attributed to the anonymous/deleted Reddit contributor. `sneed-and-feed` retains the separate credit for the checked finite upper-bound Lean extension. No private identity inference or private transcript is included.

The mathematical continuation to prioritize is a uniform bound on the feasible digit images as the generator block varies. The inverse bounds now control the entire radix-length source, and the graph return formula identifies the metric cost that must survive that further argument. The exact controller supplies finite violating blocks and cycles when a proposed lower bound fails. Every recorded execution has finished; this record asserts no continuing process.
