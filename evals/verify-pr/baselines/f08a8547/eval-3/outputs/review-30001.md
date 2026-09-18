# Review Comment Classification: 30001

## Comment

- **ID:** 30001
- **Author:** reviewer-a
- **File:** modules/fundamental/src/sbom/service/sbom.rs
- **Line:** 60
- **Body:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: code change request

## Reasoning

The reviewer directly requests a code modification: wrapping the three UPDATE statements in a database transaction. The language is imperative ("should run", "Wrap the three operations") and identifies a concrete correctness issue (inconsistent state if a partial failure occurs). This is not a suggestion of an alternative approach or a stylistic preference -- it identifies a functional gap where partial failures can leave the database in an inconsistent state, and prescribes the specific fix (use `self.db.transaction`).

This comment unambiguously qualifies as a **code change request** because:
1. The reviewer identifies a specific defect (no transactional guarantee across three dependent writes)
2. The reviewer prescribes the exact fix (wrap in `self.db.transaction(|txn| { ... })`)
3. The language is directive, not suggestive

## Action

Sub-task created to address this feedback. The soft_delete method must be updated to wrap all three UPDATE operations in a single database transaction to prevent inconsistent state on partial failure.
