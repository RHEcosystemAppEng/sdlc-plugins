# Review Comment Classification: 30001

**Comment ID:** 30001
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs
**Line:** 60

## Comment Text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: code change request

## Reasoning

The reviewer uses imperative language ("should run", "Wrap the three operations") and identifies a concrete correctness bug: the three UPDATE statements in `soft_delete` execute independently without transactional guarantees, meaning a failure partway through would leave the database in an inconsistent state. The reviewer provides a specific code change to make (wrapping in `self.db.transaction(|txn| { ... })` and switching from `self.db` to `txn`). This is a direct request to modify code to fix a correctness issue, not a suggestion or optional improvement.

## Action

Sub-task created to address this feedback.
