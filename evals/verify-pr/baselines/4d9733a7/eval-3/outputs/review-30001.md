## Review Comment Classification: #30001

**Comment ID:** 30001
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` (line 60)
**Classification:** code change request

### Reviewer Text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

### Reasoning

The reviewer uses imperative language ("should run", "Wrap the three operations") and identifies a concrete correctness defect: the three UPDATE statements in `soft_delete` execute independently without transactional guarantees. If any one of them fails after a prior one succeeds, the database is left in an inconsistent state where some related rows are marked deleted while others are not. This is a direct request for a code modification with a specific fix prescribed (wrap in `self.db.transaction`).

This is not a suggestion or optional improvement -- it addresses a data integrity risk that constitutes a functional correctness issue. The reviewer explicitly states the failure mode ("If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state") and provides the exact fix.

### Action

Sub-task created: subtask-30001.md
