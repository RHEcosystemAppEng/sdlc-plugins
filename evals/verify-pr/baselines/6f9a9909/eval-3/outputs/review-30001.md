# Review Comment 30001 — Classification

## Comment

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60

## Classification

**code change request**

## Reasoning

The reviewer uses directive language ("should run", "Wrap the three operations") and identifies a concrete correctness bug: the three UPDATE statements in `soft_delete` execute independently without transactional guarantees. If one fails after another succeeds, the database is left in an inconsistent state where some related rows are marked deleted but others are not. The reviewer provides a specific remediation — wrap the operations in `self.db.transaction(|txn| { ... })` and use the transaction handle for each exec call.

This is not a stylistic preference or optional improvement. It addresses a data integrity risk where partial failures produce inconsistent state. The language is imperative, the fix is concrete, and the issue is a correctness concern. This meets all criteria for a code change request and triggers sub-task creation.
