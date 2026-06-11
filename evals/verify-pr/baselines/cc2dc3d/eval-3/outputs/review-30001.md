# Review Comment Classification: 30001

## Comment
**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text**: "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: CODE CHANGE REQUEST

## Reasoning

1. **Directive language**: The reviewer uses imperative language -- "should run", "Wrap the three operations", "use `txn` instead of `self.db`". These are direct instructions to change specific code, not suggestions or questions.

2. **Correctness concern**: The comment identifies a real correctness bug -- the three UPDATE statements in `soft_delete` execute independently without transaction wrapping. If any intermediate statement fails, the database is left in an inconsistent state with some related records marked deleted and others not.

3. **Specific fix provided**: The reviewer specifies exactly what to do: wrap the operations in `self.db.transaction(|txn| { ... })` and use `txn` for each exec call. This is an actionable, concrete code change.

4. **Part of CHANGES_REQUESTED review**: This comment is part of a review with state "CHANGES_REQUESTED", reinforcing that the reviewer expects this to be addressed before merge.

## Result

Classification: **code change request** -- triggers sub-task creation (see subtask-30001.md).
