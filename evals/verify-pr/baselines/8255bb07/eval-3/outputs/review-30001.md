# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: code change request

## Reasoning

The reviewer uses directive language ("should run", "Wrap the three operations") and identifies a concrete correctness defect: if one of the three UPDATE operations fails after another succeeds, the database is left in an inconsistent state. This is not a stylistic suggestion or optional improvement -- it is a request to fix a data integrity bug where partial updates can corrupt state.

The reviewer provides specific implementation guidance: use `self.db.transaction(|txn| { ... })` and replace `self.db` with `txn` in each exec call. This is a clear, actionable code change request.

## Action

Sub-task created to address this feedback. The three UPDATE statements in `soft_delete` must be wrapped in a database transaction to ensure atomicity.
