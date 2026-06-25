# Review Comment Classification: 30001

## Comment

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Review ID:** 20001

## Classification: Code Change Request

## Reasoning

The reviewer uses directive language throughout this comment:

1. **"should run"** -- This is a direct instruction, not a suggestion or question. The reviewer states what the code must do, not what it could or might do.
2. **"Wrap the three operations in..."** -- This is an imperative directive giving explicit instructions on what code change to make, specifying the exact API to use (`self.db.transaction(|txn| { ... })`).
3. **"use `txn` instead of `self.db` for each exec call"** -- Another imperative instruction specifying exactly how to implement the fix.
4. The reviewer explains the consequence of not making the change ("you'll have inconsistent state"), framing this as a correctness issue that must be addressed, not an optional improvement.

The language is consistently directive -- the reviewer is requesting a specific code modification, not proposing an optional alternative. This is a code change request that will trigger sub-task creation.
