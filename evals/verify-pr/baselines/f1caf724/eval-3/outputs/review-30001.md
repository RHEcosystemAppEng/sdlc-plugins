# Review Comment Classification: 30001

## Comment

- **ID:** 30001
- **Author:** reviewer-a
- **File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
- **Body:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: code change request

## Reasoning

The reviewer uses imperative language throughout: "should run all three UPDATE statements inside a single database transaction", "Wrap the three operations", "use `txn` instead of `self.db`". This is a direct instruction to modify code, not a tentative suggestion or a question. The reviewer identifies a concrete correctness defect (inconsistent state on partial failure) and prescribes the exact fix (wrap in `self.db.transaction()`).

Key language signals:
- "should run" -- directive, not suggestive
- "Wrap the three operations" -- imperative verb form, commanding a specific action
- "use `txn` instead of `self.db`" -- prescribes exact implementation detail
- Identifies a concrete failure scenario (sbom_advisory update fails after sbom_package succeeds) that would cause data corruption

This is not a suggestion (no hedging language like "could", "might want to", "would help"), not a nit (affects correctness, not style), and not a question (no interrogative form). It is a clear code change request.

## Action

Create sub-task to wrap the three UPDATE statements in a database transaction.
