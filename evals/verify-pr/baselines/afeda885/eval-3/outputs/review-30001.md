# Review Comment Classification: 30001

## Comment
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Content:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: code change request

## Reasoning

The reviewer uses imperative, directive language throughout: "should run", "Wrap the three operations", "use `txn` instead of `self.db`". This is not a suggestion or optional improvement -- the reviewer is identifying a concrete correctness bug (potential for inconsistent state if one UPDATE fails after another succeeds) and prescribing a specific code change to fix it. The reviewer names the exact method to wrap (`soft_delete`), the exact mechanism to use (`self.db.transaction(|txn| { ... })`), and the exact substitution to make (`txn` instead of `self.db`).

This meets the classification criteria for **code change request**: the reviewer asks for a code modification with specific instructions on what to change and why.

## Sub-task required: Yes

A sub-task will be created to wrap the three UPDATE statements in a database transaction within the `soft_delete` method.
