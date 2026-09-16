# EP817 supported defects: relative cohomology and visibility

[Receiving map and full scope](notes/splitzero-receiving-map.md)

[Complete arithmetic deformation proof](notes/supported-defect-universality.md)

[Complete cut-filtration and graph-quotient proof](notes/graphic-visibility-filtration.md)

This is an additive receiving contribution using the original SplitZero support
reconstruction and internal quotient. It retains relative classes killed by
an absolute or numerical observation, their specialization detector, all
word-fibre masses and the original quotient metrics. No Riemann-hypothesis or
arithmetic theta-growth conclusion is claimed.

Both full companion proofs and all four standalone verification programs are
copied byte-identically from the EP817 payload. From this directory run
`python run_checks.py`, or `python run_checks.py --optimized`. The runner
rebuilds into a temporary directory and checks exact equality with stored
evidence; no existing workbench receipt is overwritten.

The inherited source is
`workbenches/splitzero-tandem/tex/support_diagrams.tex` at
`58626a62cd5648e8ae7450fb54d4a4aab2330981`, especially (D6)–(D8), with unchanged
blob `d3493f891291ee6e94dbf2c77649f7d85d240df2`. Its original scalar, existing
mathematics, publication and formal-verification statuses remain unchanged.
The new mathematics has written proofs and exact bounded computational checks;
independent mathematical review is pending and no new Lean elaboration occurred.
The original anonymous mathematical and sneed-and-feed formalization credits
are retained in the proof bodies and provenance record.
