# Review Comment Classification: 30001

## Comment
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Content:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: code change request

## Reasoning

The reviewer explicitly asks for a code modification: wrapping the three UPDATE statements in a single database transaction. The language is directive ("should run", "Wrap the three operations") and identifies a concrete correctness issue (inconsistent state if a later update fails after an earlier one succeeds). The reviewer specifies the exact change needed (`self.db.transaction(|txn| { ... })`) and the rationale (atomicity to prevent partial cascade updates). This is a clear request for a code change, not a suggestion of an alternative approach or a question for clarification.

## Action
Sub-task created to address this feedback.
