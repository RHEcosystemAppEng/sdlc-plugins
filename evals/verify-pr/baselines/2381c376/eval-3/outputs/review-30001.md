# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Body:**
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: Code Change Request

## Reasoning

The reviewer uses imperative, directive language that requires a code modification:

1. **"should run all three UPDATE statements inside a single database transaction"** -- a direct instruction to change the implementation, not a suggestion of an optional alternative.
2. **"Wrap the three operations in `self.db.transaction(|txn| { ... })`"** -- specifies the exact code change required.
3. **"use `txn` instead of `self.db` for each exec call"** -- prescribes the specific implementation detail.

The reviewer identifies a concrete correctness bug: without a transaction, a partial failure (e.g., sbom_advisory update fails after sbom_package succeeds) would leave the database in an inconsistent state. This is not a style preference or optional improvement -- it is a data integrity defect that the reviewer requires to be fixed.

This matches the "code change request" classification: the reviewer asks for a code modification.

## Action

Sub-task created: see `subtask-30001.md`
