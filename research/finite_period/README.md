# Finite-period control and exact finite-word minima

The full proof is in `notes/finite-period-control.md`. This contribution gives an
explicit finite-word approximation to the best image-growth rate of every finite
canonical arithmetic dictionary. It retains unequal generator rewards and gives
the additional closing-path cost for finite strongly connected controllers.

For q coefficient values, the exact cut has at most q-1 numerical pairs in a
receiving fibre. A length-m computation brackets the optimal rate with logarithmic
width at most log(q-1)/(m*n_min). No finite-period attainment is presumed for a
general dictionary. In the radix-ten example (10,{1,3}), (10,{2,4}), the exact
minimum at every finite length is proved and attained explicitly by BA and BAA
macro blocks. This retains the finite endpoint cost of a cyclic phase.

## Replay

From this directory:

```sh
python certificates/verify_finite_period.py
python certificates/audit_finite_period.py
```

Both programs use the standard library. The auditor imports neither the producer
nor its helper. The complete large word domains are accounted for by exact
row/column aggregation with literal word multiplicities. The receipts distinguish
this complete enumeration from direct evaluation of the stated smaller original
generator domains. This contribution has no new Lean elaboration, human-review
claim, or global numerical record.

The original anonymous/deleted contributor's k=4 credit and sneed-and-feed's
finite-upper-bound Lean credit remain separate. Existing sources and receipts
are not modified. The earlier local-flow infinite optimum is the predecessor;
the new finite-period bound and complete finite-length minima are stated with
their own proof and verification boundaries.
