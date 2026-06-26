# Review Comment Classification: 30001

**Comment ID:** 30001
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs
**Line:** 60

## Comment Text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: code change request

## Reasoning

The reviewer explicitly asks for a code modification: wrapping three UPDATE statements in a database transaction. The language is directive ("should run", "Wrap the three operations"), not suggestive or optional. The feedback identifies a concrete correctness bug -- partial failure of the cascade update operations would leave the database in an inconsistent state where the SBOM is marked deleted but some related join table rows are not. This is a functional correctness issue, not a style or preference matter. The fix is well-scoped and actionable.

## Action

Sub-task created to wrap the three `soft_delete` update operations in a single database transaction using `self.db.transaction(|txn| { ... })`.
