# Review Comment Classification: #30001

**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Content:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: **Code Change Request**

### Reasoning

The reviewer uses directive language that requests a specific code modification:

1. **"should run all three UPDATE statements inside a single database transaction"** — prescriptive, not suggestive. The reviewer identifies a concrete correctness issue (inconsistent state on partial failure) and states what must change.
2. **"Wrap the three operations in `self.db.transaction(|txn| { ... })`"** — provides the exact code pattern to implement, leaving no ambiguity about what is requested.
3. **"use `txn` instead of `self.db` for each exec call"** — specific implementation instruction.

The comment identifies a real data consistency bug: without a transaction, a failure in the third UPDATE (sbom_advisory) leaves the first two UPDATEs (sbom, sbom_package) committed, producing an inconsistent database state. This is a correctness issue, not a stylistic preference.

### Sub-task Required: Yes

This code change request triggers sub-task creation. The sub-task will be created with **Issue Type: Sub-task** (under parent TC-9103) to wrap the three UPDATE operations in a database transaction.

See: `subtask-30001.md`
