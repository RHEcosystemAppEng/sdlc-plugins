# Review Comment Classification: 30001

## Comment
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs` line 60
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: code change request

## Reasoning
The reviewer uses directive language ("should run", "Wrap the three operations") and identifies a concrete correctness issue: without a transaction, a failure partway through the cascade updates would leave the database in an inconsistent state. This is not a suggestion of an alternative approach -- it is a direct request to fix a correctness bug in the implementation. The reviewer specifies exactly what code change is needed (wrap in `self.db.transaction()` and use `txn` for each exec call).

## Action
Sub-task created to address this feedback.
