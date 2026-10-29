# Review Comment Classification: Comment 30001

## Comment Details
- **Author:** reviewer-a
- **File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
- **Content:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: **Code Change Request**

## Reasoning

The reviewer uses directive language throughout:
- "should run all three UPDATE statements inside a single database transaction" — direct instruction, not a suggestion
- "Wrap the three operations in `self.db.transaction(|txn| { ... })`" — explicit code change instruction with specific API reference
- "use `txn` instead of `self.db` for each exec call" — prescriptive fix

The comment identifies a concrete correctness bug: without a transaction, partial failure of the cascade updates produces inconsistent state (sbom_package updated but sbom_advisory not). This is a data integrity issue, not a style preference.

The reviewer is requesting a specific code modification with clear implementation guidance. This is a code change request, not a suggestion.

## Action
Sub-task creation triggered. See subtask-30001.md.
