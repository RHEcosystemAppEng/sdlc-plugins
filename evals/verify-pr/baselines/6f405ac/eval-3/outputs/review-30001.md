# Review Comment Classification: 30001

## Comment

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

**File:** `modules/fundamental/src/sbom/service/sbom.rs` line 60
**Author:** reviewer-a

## Classification: CODE CHANGE REQUEST

## Reasoning

The reviewer uses direct imperative language: "should run all three UPDATE statements inside a single database transaction" and "Wrap the three operations in `self.db.transaction(|txn| { ... })`". This is not a suggestion or question -- it is a concrete request for a specific code change. The reviewer identifies a real correctness issue: without a transaction wrapping the three UPDATE statements, a failure in a later update (e.g., `sbom_advisory`) after an earlier one succeeds (e.g., `sbom_package`) would leave the database in an inconsistent state with partially-applied soft deletes. The reviewer provides the exact fix: use `self.db.transaction(|txn| { ... })` and replace `self.db` with `txn` in each exec call.

This is a code change request because:
1. The language is imperative ("should run", "Wrap the three operations")
2. It identifies a concrete correctness bug (partial failure leaves inconsistent state)
3. It specifies exactly what code change is needed (transaction wrapping)

## Action

Sub-task creation required to address the transaction wrapping fix.
