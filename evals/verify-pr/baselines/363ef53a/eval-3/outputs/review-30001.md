# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: code change request

## Reasoning

The reviewer uses directive language throughout the comment:

1. "should run all three UPDATE statements inside a single database transaction" -- a direct instruction to change the code behavior.
2. "Wrap the three operations in `self.db.transaction(|txn| { ... })`" -- a specific, imperative instruction with exact code to use.
3. "use `txn` instead of `self.db` for each exec call" -- another direct instruction specifying the implementation detail.

The reviewer is not proposing an alternative or asking a question. The language is imperative and prescriptive: "should", "Wrap", "use". The comment identifies a concrete correctness bug (inconsistent state on partial failure) and directs the developer to fix it with a specific approach. This is a clear code change request.

## Sub-task Required: Yes

A sub-task will be created to wrap the three UPDATE operations in `soft_delete` inside a database transaction to ensure atomicity.
