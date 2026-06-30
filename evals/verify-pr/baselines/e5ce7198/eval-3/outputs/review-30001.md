# Review Comment Classification: 30001

**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Date**: 2026-04-20T14:32:00Z

## Comment Text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: Code Change Request

**Reasoning**: The reviewer uses directive language throughout the comment. "Should run" is a directive instruction, not a suggestion. "Wrap the three operations" is an imperative command specifying exactly what code modification to make. The reviewer provides both the rationale (preventing inconsistent state on partial failure) and the exact implementation pattern to follow (`self.db.transaction(|txn| { ... })` with `txn` replacing `self.db`).

This is not suggestive or exploratory language. There is no hedging ("might want to", "could consider", "would be nice"). The reviewer identifies a concrete correctness bug -- three independent UPDATE statements without transactional wrapping means a failure in the second or third statement leaves the database in an inconsistent partially-deleted state -- and prescribes the specific fix.

The combination of directive phrasing, specificity of the requested change (exact API call, parameter names, and usage pattern), and the correctness impact (data inconsistency on partial failure) clearly marks this as a code change request.

**Action**: Create sub-task (subtask-30001.md)
