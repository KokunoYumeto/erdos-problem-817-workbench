# Erdős Problem 817: cumulative research notes

[Read the corrected collection](latex/collected_notes.pdf) · [Twenty-nine-note index](NOTE_INDEX.md) · [Editable master](latex/collected_notes.tex) · [Original source delivery](https://github.com/KokunoYumeto/erdos-problem-817-workbench/releases/tag/cumulative-2026-09-16)

The collection follows the work from the ternary-variance and general-k constructions through arithmetic carry control, supported relations, graphical and recurrence methods, and exact image-count optimization. Each chapter contains a complete mathematical note. The original k=4 argument and the contributor's attribution remain in the [main workbench](../../README.md).

## New continuation

[Uniform finite-period approximation and exact finite-word switching minima](../../research/finite_period/notes/finite-period-control.md) proves a finite approximation theorem for every specified finite canonical dictionary. For arity q≥2 and positive generator rewards, the logarithmic error after inspecting all length-m words is at most log(q−1)/(m n_min). A minimizing word supplies an explicit periodically repeated approximation. The proof retains the original numerical image and its cut fibres, with no assumption that an optimum must have an exactly realizing finite period.

The same note determines all finite-word minima for the radix-ten two-letter example and gives bounds for finite controllers with their actual closing-path cost. The [companion](../../interfaces/zeta/workbenches/ep817-finite-period/notes/splitzero-receiving-map.md) retains original word-to-value kernels and source masses. A uniformly bounded numerical fibre count does not remove growth in representation multiplicity or the associated metric cost.

The general unbounded family of admissible blocks remains a separate question: the theorem specifies the horizon needed for a given finite dictionary, not how many block ranks suffice for the unrestricted infimum.

## Evidence and source history

The new producer and its separately implemented auditor were rerun in ordinary and optimized Python, with identical ordinary/optimized receipts. Their exact finite domains remain in the published certificates. Earlier notes keep their own source-time proof and verification status; gathering them into a volume does not give them new Lean certificates or a new independent peer review.

The supplied archive contains the original session files and their preservation manifests. The current reader repairs mis-typeset inline powers and incorporates the already-published seven-observation correction L>3Q with its gap argument. [Publication notes](PUBLICATION_NOTES.md) record the distinction. The original delivery remains a separate release download; it is not the preferred reading edition.

The research continuation is attributed in its sources to **The Clankers**, within the public **Kokuno Yumeto** workbench. Existing source authors and the outside Lean contributor retain their separate attribution. The collection is intended to support further mathematical reading, verification, and contributions without requiring the original conversations.
