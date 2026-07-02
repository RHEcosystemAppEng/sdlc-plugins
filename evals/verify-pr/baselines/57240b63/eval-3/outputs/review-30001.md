# Review Comment Classification: 30001

## Comment
**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text**: The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: Code Change Request

## Reasoning

The reviewer uses imperative language throughout:
- "should run all three UPDATE statements inside a single database transaction" -- direct instruction
- "Wrap the three operations in `self.db.transaction(|txn| { ... })`" -- specific implementation directive
- "use `txn` instead of `self.db` for each exec call" -- explicit code change instruction

The reviewer identifies a concrete correctness issue (inconsistent state on partial failure) and prescribes a specific fix. This is not a suggestion or open question -- it is a direct request to modify the code.

## Sub-task Required: YES

A sub-task will be created to wrap the three update operations in a database transaction.
