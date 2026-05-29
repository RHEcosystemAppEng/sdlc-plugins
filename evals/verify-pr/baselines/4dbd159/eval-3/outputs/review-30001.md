# Review Comment Classification: 30001

**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Date**: 2026-04-20T14:32:00Z

## Comment Text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: Code Change Request

**Reasoning**: The reviewer makes a direct, imperative request to change the code. The phrasing is directive ("should run", "Wrap the three operations") and the reviewer specifies the exact code pattern to use (`self.db.transaction(|txn| { ... })` with `txn` replacing `self.db`). This is not a question or suggestion -- it is a concrete demand to modify the implementation.

The underlying concern is a correctness issue. The `soft_delete` method currently runs three independent UPDATE statements in sequence against `sbom`, `sbom_package`, and `sbom_advisory` without any transactional boundary. If the second or third UPDATE fails after earlier ones succeed, the database is left in an inconsistent partially-deleted state. This is a data integrity bug, not a stylistic preference.

The directive language, the specificity of the requested change (exact API and parameter names), and the correctness severity all unambiguously classify this as a code change request.

**Action**: Create sub-task (subtask-30001.md)
