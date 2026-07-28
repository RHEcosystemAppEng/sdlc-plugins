# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`
**Line:** 60
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: CODE CHANGE REQUEST

## Reasoning

The reviewer uses imperative language that directs a specific code modification:

1. **"should run all three UPDATE statements inside a single database transaction"** -- this is a direct instruction to change the code structure, not a suggestion or optional improvement.
2. **"Wrap the three operations in `self.db.transaction(|txn| { ... })`"** -- the reviewer prescribes the exact code change, specifying the API to use.
3. **"use `txn` instead of `self.db` for each exec call"** -- further concrete implementation direction.

The reviewer identifies a real correctness issue: without a transaction, a failure in the `sbom_advisory` update after `sbom_package` succeeds would leave the database in an inconsistent state with partially applied soft-deletes. This is not a stylistic preference or optional improvement -- it is a necessary fix to prevent data corruption.

The language is directive ("should", "Wrap", "use ... instead of"), not suggestive ("could", "might consider", "would be nice"). This clearly falls into the **code change request** category.

## Action

Sub-task created: subtask-30001.md
