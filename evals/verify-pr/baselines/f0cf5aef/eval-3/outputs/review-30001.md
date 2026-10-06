# Review Comment Classification: 30001

**Comment ID:** 30001
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs
**Line:** 60
**Classification:** code change request

## Reasoning

The reviewer explicitly asks for a code modification: wrapping the three UPDATE statements in `soft_delete` inside a single database transaction using `self.db.transaction(|txn| { ... })`. The language is directive -- "should run all three UPDATE statements inside a single database transaction" -- and identifies a concrete correctness issue (inconsistent state if a later update fails after an earlier one succeeds). This is not a suggestion or optional improvement; it addresses a data integrity concern that requires a code change.

The reviewer specifies the exact fix: use `self.db.transaction(|txn| { ... })` and replace `self.db` with `txn` for each exec call. This is a direct code change request.

**Action:** Sub-task created to address this feedback.
