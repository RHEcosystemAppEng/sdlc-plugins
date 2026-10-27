# Review Comment Classification: #30001

## Comment Details
- **Author:** reviewer-a
- **File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
- **Content:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: **Code Change Request**

## Reasoning

The reviewer uses directive language throughout:

1. **"should run all three UPDATE statements inside a single database transaction"** — This is an explicit directive telling the author what must be done, not a suggestion or alternative approach.
2. **"Wrap the three operations in `self.db.transaction(|txn| { ... })`"** — A specific, prescriptive instruction on how to implement the fix.
3. **"use `txn` instead of `self.db` for each exec call"** — Further concrete implementation direction.

The reviewer identifies a real correctness issue: without a transaction, a failure in one UPDATE leaves the database in an inconsistent state (e.g., `sbom_package.deleted_at` is set but `sbom_advisory.deleted_at` is not). This is not a style preference or optional improvement — it is a data integrity concern that requires a code change.

**Language analysis:** The comment contains no hedging language (no "could", "might consider", "you may want to"). The tone is imperative: "should run", "Wrap", "use". This is a clear code change request.

## Action
- **Sub-task creation:** YES
- **Issue Type:** Sub-task (parent: TC-9103)
- **Sub-task file:** subtask-30001.md
