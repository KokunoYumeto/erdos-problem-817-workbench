# Review of the finite upper-bound formalization

Reviewed 13 September 2026. Contribution:
[PR #1](https://github.com/KokunoYumeto/erdos-problem-817-workbench/pull/1),
by [sneed-and-feed](https://github.com/sneed-and-feed), at commit
`155523c57cf7576ae86304af02bc073f2567b8d0`.
The comparison base was `682b5f4fa4eed7345d3c28b881294fae03eb04f0`.

## Mathematical reading

An independent source review read the complete `Extended.lean` and `Core.lean`
modules, together with the build configuration and existing verification
records. No mathematical defect was found in the submitted argument. This
source review was followed by independent Lean elaboration and the full
axiom audit described below; all checks passed.

The theorem `erdos_problem_817_upper_bound` concerns the actual finite set of
positive integer generators, not merely a separately defined digit language.
For `m = (n + 2) / 3`, there are `3m` distinct generators
`19^j * w`, with `0 <= j < m` and `w` in `{1,7,8}`. Generator injectivity is
proved before cardinality is used. A subset of generators determines one
binary triple at each level, and the sum of that subset equals the base-19
evaluation of the resulting list. This proves that every actual subset sum
lies in the digit language certified by Core. Finally an `n`-element
subcollection inherits both the coordinate bound and 4-AP-freeness.

The exact statement retains all of the following:

- `B : Finset Z` and `B.card = n`: distinct generators, not an indexed family
  with repeated values.
- `1 <= b <= 8 * 19 ^ ((n + 2) / 3 - 1)` for every member of `B`.
- Every finite subset is allowed, including the empty subset.
- Every contained four-term arithmetic progression has difference zero.

Distinct subset sums are not required. In particular `1 + 7 = 8` is an
intentional collision, already present in the construction. The finite upper
theorem does not formalize the signed-block lower-bound proof or the real
asymptotic squeeze.

## Exact source locations

All line references in this section are to the reviewed commit, not a moving
branch.

| File | Lines | Content |
|---|---|---|
| `formal/lean/ErdosProblem817/Core.lean` | 78–121 | All-length digit-language lifting |
| `formal/lean/ErdosProblem817/Core.lean` | 171–173 | Definition of `FourAPFree` |
| `formal/lean/ErdosProblem817/Extended.lean` | 301–312 | Subset sums and heredity |
| `formal/lean/ErdosProblem817/Extended.lean` | 351–373 | Positivity and coordinate bound |
| `formal/lean/ErdosProblem817/Extended.lean` | 396–426 | Generator injectivity and cardinality |
| `formal/lean/ErdosProblem817/Extended.lean` | 432–514 | Exact subset-sum/evaluated-block bridge |
| `formal/lean/ErdosProblem817/Extended.lean` | 523–537 | Finite upper-bound theorem |

No `sorry`, custom axiom, `native_decide`, or unsafe declaration was added in
the contribution. The finite enumerations use `decide`; the remaining proof
is symbolic. Independent elaboration confirmed that every one of the 44 new
theorem declarations depends only on subsets of `propext`, `Classical.choice`,
and `Quot.sound`. The full output is preserved in
`certificates/lean_extended_axioms.txt`.

## Integration and reproducibility

The contributed library glob includes the extension in the library build.
The earlier README command, however, checked Core alone, and `Main.lean`
imported Core alone. The integration changes the import to Extended and
documents sequential builds of both modules followed by `Audit.lean`.

The old Core receipt remains a record of its exact checked source. It does
not certify Extended. The workbench therefore declares separate module and
receipt lists, preserving the Core entrypoint for compatibility. A separate
`certificates/lean_extended_receipt.json`, axiom report, and successful
source-hash validation are required before the extension is described as
independently Lean-checked.

The claim catalogue now records the finite upper theorem explicitly and
routes the actual subset-sum lifting claim through
`Extended:generators_fourAPFree`. The prior Core theorem remains recorded as
the digit-language helper it supplies.

## Attribution

The construction and mathematical proof remain attributed to the
anonymous/deleted Reddit contributor. The additional Lean formalization is
credited to sneed-and-feed. No identity is inferred between those two credits,
and no private attribution material is included.

## Check status

- Independent mathematical/source review: complete; no defect found.
- Independent Core, Extended, Main, and Audit elaboration: passed, serially.
- Printed axiom report: all 44 declarations checked; only standard axioms.
- Source-hashed Extended receipt and machine-state validation: passed.
- Finite extended certificate: rerun successfully, including 747 admissible
  sets in the stated lower-bound stress-test domain and 75 deletion choices.

The local checks used a fresh output directory for project oleans and the
existing dependency cache. All nine dependency checkout revisions matched
the manifest; the dependency libraries themselves were not rebuilt. The
resource watcher sampled physical process-tree working set and preempted at
4.7 billion bytes against a five-billion-byte limit. The highest observed
value was 3,475,734,528 bytes. Private-byte diagnostics are recorded separately;
they are not measurements of resident physical memory. This is a sampled
watcher, not a kernel-enforced memory ceiling.
