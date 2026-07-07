# Review Comment Classification: 30001

## Comment Details

- **Comment ID:** 30001
- **Author:** reviewer-a
- **File:** modules/fundamental/src/sbom/service/sbom.rs
- **Line:** 60
- **Content:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: code change request

## Reasoning

The reviewer uses directive language ("should run", "Wrap the three operations") and provides a specific implementation instruction (use `self.db.transaction(|txn| { ... })` and substitute `txn` for `self.db`). This is not a suggestion or optional improvement -- the reviewer identifies a concrete correctness defect (partial cascade failure leading to inconsistent state) and prescribes a specific code modification to fix it. The language is imperative and the requested change addresses a data integrity issue.

## Action

Sub-task creation triggered. The code change request requires wrapping the three `update_many` operations in `soft_delete` inside a database transaction to ensure atomicity.
