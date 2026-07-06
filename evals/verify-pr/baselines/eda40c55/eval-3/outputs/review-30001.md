# Review Comment Classification: Comment 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: CODE CHANGE REQUEST

## Reasoning

The reviewer uses direct imperative language: "should run", "Wrap the three operations". This is not a suggestion or a question -- it is a specific instruction to change the code in a particular way. The reviewer identifies a concrete correctness issue (inconsistent state if one of the three UPDATE statements fails after another succeeds) and prescribes the exact fix (wrapping in a database transaction using `self.db.transaction(|txn| { ... })`).

Key indicators supporting code change request classification:
1. **Imperative language**: "should run... inside a single database transaction" and "Wrap the three operations"
2. **Identifies a bug/correctness issue**: partial failure leaves inconsistent state between `sbom`, `sbom_package`, and `sbom_advisory` tables
3. **Prescribes a specific fix**: use `self.db.transaction()` and pass `txn` to each exec call
4. **Not optional**: the reviewer is not proposing an alternative approach -- they are identifying a real data integrity issue that must be fixed

## Action

Sub-task creation required. The three sequential UPDATE statements in `soft_delete` must be wrapped in a database transaction to ensure atomicity.
