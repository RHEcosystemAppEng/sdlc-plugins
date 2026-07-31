# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: CODE CHANGE REQUEST

## Reasoning

The reviewer uses direct, imperative language requesting a specific code modification:

1. **"should run all three UPDATE statements inside a single database transaction"** -- this is an explicit instruction to change how the code executes database operations, not a suggestion or optional improvement.
2. **"Wrap the three operations in `self.db.transaction(|txn| { ... })`"** -- the reviewer provides the exact code pattern to implement, specifying the API call (`transaction`), the closure parameter (`txn`), and the substitution to make (`txn` instead of `self.db`).
3. **"you'll have inconsistent state"** -- the reviewer identifies a concrete correctness defect (partial updates on failure), not a stylistic preference. This is a bug that must be fixed, not an optional enhancement.

The language is prescriptive ("should run", "Wrap"), identifies a real defect (data inconsistency on partial failure), and provides specific implementation guidance. This clearly qualifies as a code change request that triggers sub-task creation.
