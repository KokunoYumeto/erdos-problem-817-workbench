# Outer-control publication: verification-run clarification

The complete certificate replay succeeded in [run34891977899](https://github.com/KokunoYumeto/erdos-problem-817-workbench/actions/runs/34891977899), using input commit `68d64ed4fe050d51e4247cecae79e419a48bad63`. Its successful publication step produced commit `74ba7dcc4bd623b3555046feb6d45ccac38417a3`, containing the three compressed complete proof records and the replay receipt.

That automated commit triggered a second pull-request run, [34892226947](https://github.com/KokunoYumeto/erdos-problem-817-workbench/actions/runs/34892226947). GitHub reports: “This workflow run required approval but was not approved before it expired.” The second run has zero jobs and zero check runs: no verification program executed or reported a mathematical failure.

The failed badge therefore records an expired approval for the publication's self-triggered follow-up, not a failed certificate replay. It is not counted as a successful check. The successful original run, its exact source/output hashes, and the separately recorded bounded integration audit remain the verification evidence. No mathematical payload or workflow was changed by this clarification.
