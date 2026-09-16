# Erdős Problem 817 — complete source and LaTeX collection

This is the cumulative collection of the recovered session deliverables plus the
new finite-period continuation. It contains **29 complete unique mathematical
notes in editable LaTeX** and their **220-page compiled PDF**. All **465 original
non-ZIP members from 15 distinct earlier archives** remain byte-for-byte intact,
including the separate recurrence work and both early general-k developments.

It is not a full checkout of either GitHub workbench, and it does not claim that
all historical mathematics has acquired a new independent review or Lean proof.
The original source dependencies that were referenced but not delivered as archive
members remain cited, rather than falsely marked as included.

## Read and edit

- `latex/collected_notes.pdf`: the complete 220-page reader.
- `latex/collected_notes.tex`: master LaTeX document.
- `latex/chapters/`: all 29 complete chapter sources.
- `latex/individual/`: separately verified wrappers; the latest two PDFs are supplied.
- `NOTE_INDEX.md`: original Markdown and LaTeX source links, in chronological order.
- `history/`: all preserved source/evidence records, plus the new continuation.
- `repositories/ep817/` and `repositories/zeta/`: 347 flattened repository-relative
  payload files, ready for collision-checked additive staging.
- `provenance/`: archive member identities, alias maps, formula inventory, and checks.

No nested predecessor ZIP needs to be unpacked to locate a proof. Original scripts,
JSON, compressed proof records, and patches are retained. Original ZIP containers
are identified by SHA-256; this collection preserves their non-archive contents
rather than recursively embedding duplicate ZIP containers.

## New mathematics

`research/finite_period/` gives uniform finite-horizon enclosures for the optimal
image-growth rate of any finite canonical arithmetic dictionary. For arity q, the
logarithmic error is at most log(q-1)/(m*n_min). A finite strongly connected
positive-reward controller adds an explicit closing-path cost. The exact optimum
of every finite word length is evaluated in the earlier radix-ten example.

The new producer and independently implemented auditor passed normally and under
optimized Python with byte-identical receipts. They replayed from cleanly applied
patches; the independent auditor also runs from the Zeta payload. These are written
proofs and exact computational certificates, not new Lean elaboration. The original
inherited searches were not all rerun during this source collection.

## Safe local repository staging

The payload directories are additions, not replacement repositories. Do not
replace a checkout with them. First perform a dry run:

```sh
python tools/stage_payload.py ep817 /path/to/erdos-problem-817-workbench
python tools/stage_payload.py zeta /path/to/zeta-function-research-reader
```

After examining its report, add `--apply` to copy missing files. Identical existing
files are skipped. Any different existing file, symbolic-link destination, or
non-directory ancestor causes preflight failure before copying. Local changes
must be reviewed separately. The tool does not commit, push, or merge.

Historical root publication descriptors remain in `history/`; they are not staged
as current root status files. Original patch paths and historical reports are
preserved, not silently rewritten to assert a newer publication outcome.

EP817 main was inspected at `578564a5f0c6e3348f5bdc33fd2022b674899c41`.
It already contains many earlier additions. The new cone-dual note on that main
was read for the comparison but is an upstream-only source, not a historical ZIP
member. No remote write was performed by this contribution.

## Verification and attribution

Run `python verify_collection.py` for all manifest-bound hashes and all 465
preserved original member hashes. The new mathematical replay commands are:

```sh
cd repositories/ep817/research/finite_period
python certificates/verify_finite_period.py
python certificates/audit_finite_period.py
```

A PDF build certifies typesetting, not a mathematical theorem. Each original note
retains its original statement, assumptions, evidence scope and publication date.
The anonymous/deleted contributor retains credit for the four-term construction
and signed-block proof; sneed-and-feed retains separate credit for the existing
Lean finite-upper-bound extension. No global priority claim is introduced.
