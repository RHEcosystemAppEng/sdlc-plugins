# Review Comment Classification: 30001

## Comment Details

- **ID:** 30001
- **Author:** reviewer-a
- **File:** modules/fundamental/src/sbom/service/sbom.rs
- **Line:** 60
- **Body:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: CODE CHANGE REQUEST

## Reasoning

The reviewer is making a direct, imperative request for a code change. Key language indicators:

1. **"should run"** -- directive language stating what the code must do, not a suggestion or optional improvement.
2. **"Wrap the three operations"** -- an explicit instruction to modify the code structure.
3. **"use `txn` instead of `self.db`"** -- specifies the exact code change required.

The reviewer identifies a concrete correctness issue: if one of the three UPDATE statements fails after another succeeds, the database will be left in an inconsistent state (some related records marked as deleted, others not). This is a data integrity bug, not a style preference or optional enhancement.

The comment prescribes a specific fix (wrapping in a transaction) and explains why the current code is incorrect (partial failure leads to inconsistent state). This fits the CODE CHANGE REQUEST classification because the reviewer asks for a code modification to fix a correctness issue.

## Action

Create a sub-task to wrap the three UPDATE operations in `soft_delete` inside a database transaction.
