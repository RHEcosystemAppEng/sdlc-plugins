# Review Comment Classification: 30001

## Comment
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs
**Line:** 60
**Text:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: code change request

## Reasoning
The reviewer uses directive language ("should run", "Wrap the three operations") and identifies a concrete correctness defect: if any of the three cascading UPDATE statements fails after one succeeds, the database will be left in an inconsistent state. This is not a stylistic preference or optional improvement — it is a request for a specific code modification to ensure data integrity. The reviewer provides the exact fix approach (use `self.db.transaction(|txn| { ... })`) making this an unambiguous code change request.

This feedback points to a genuine atomicity bug where partial failure of the cascade operations would leave orphaned or inconsistently-marked join table rows, violating the soft-delete contract.
