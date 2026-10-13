# Review Comment Classification: 30001

## Comment

- **Author:** reviewer-a
- **File:** `modules/fundamental/src/sbom/service/sbom.rs`
- **Line:** 60
- **Body:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: Code Change Request

## Reasoning

The reviewer directly instructs a specific code modification using imperative language: "Wrap the three operations in `self.db.transaction(|txn| { ... })`". This is not a suggestion or question -- it identifies a concrete correctness defect (inconsistent state on partial failure) and prescribes the exact fix (transaction wrapping). The language "should run" and "Wrap the three operations" are directive, matching the code change request pattern ("this should validate input", "add error handling here").

The defect is a data integrity issue: if the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left in an inconsistent state where some join table rows are marked deleted and others are not. This is a correctness concern, not a stylistic preference.

## Action

Sub-task created (subtask-1) to wrap the three UPDATE statements in `soft_delete` inside a database transaction.
