# Review Comment Classification: 30001

**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Date**: 2026-04-20T14:32:00Z

## Comment Text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: Code Change Request

**Reasoning**: The reviewer explicitly requests a specific code modification: wrapping the three UPDATE statements inside a database transaction. The language is directive -- "should run" and "Wrap the three operations" are imperative instructions, not suggestions or questions. The reviewer provides an exact code pattern to follow (`self.db.transaction(|txn| { ... })`) and specifies the precise change needed (use `txn` instead of `self.db` for each exec call).

This is classified as a code change request because:

1. **Directive language**: "should run all three UPDATE statements inside a single database transaction" and "Wrap the three operations" are imperative statements that instruct the author to make a specific change, not optional recommendations.
2. **Concrete correctness defect identified**: The reviewer identifies a real atomicity bug -- if the `sbom_advisory` update fails after `sbom_package` succeeds, the database is left in an inconsistent state with partially soft-deleted records.
3. **Specific implementation prescribed**: The reviewer provides exact API details (`self.db.transaction(|txn| { ... })`) and tells the author to replace `self.db` with `txn` in each exec call. This level of specificity indicates a required change, not an open-ended suggestion.

The combination of imperative language, a concrete correctness issue, and a precisely specified fix clearly marks this as a code change request that triggers sub-task creation.

**Action**: Create sub-task (subtask-30001.md)
