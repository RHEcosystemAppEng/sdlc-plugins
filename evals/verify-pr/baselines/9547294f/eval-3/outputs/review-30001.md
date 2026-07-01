# Review Comment Classification: 30001

## Comment

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**PR:** #744

## Classification: Code Change Request

## Reasoning

The reviewer uses imperative, directive language throughout the comment:

- "should run all three UPDATE statements inside a single database transaction" -- a direct instruction to change the code behavior
- "Wrap the three operations in `self.db.transaction(|txn| { ... })`" -- a specific code change instruction with exact API usage
- "use `txn` instead of `self.db` for each exec call" -- a concrete modification to apply

The reviewer identifies a correctness defect: the three UPDATE statements in `soft_delete` are not wrapped in a transaction, meaning a failure partway through would leave the database in an inconsistent state (e.g., `sbom_package` rows marked deleted but `sbom_advisory` rows not). This is not a stylistic preference or optional suggestion -- it describes a data integrity bug that must be fixed.

The language is unambiguously directive (imperative "should", "wrap", "use"), identifies a concrete failure scenario ("inconsistent state"), and prescribes a specific fix. This meets the criteria for a **code change request**.

## Action

Sub-task creation required. This code change request triggers a Jira sub-task to wrap the three UPDATE operations in a database transaction.
