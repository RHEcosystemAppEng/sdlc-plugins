# Review Comment Classification: 30001

## Comment

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Date**: 2026-04-20T14:32:00Z

## Classification: Code Change Request

## Reasoning

The reviewer uses directive language throughout this comment:

1. **"should run"** -- directs the author to change how the three UPDATE statements execute.
2. **"Wrap the three operations in `self.db.transaction(|txn| { ... })`"** -- provides an explicit instruction on what code change to make.
3. **"use `txn` instead of `self.db` for each exec call"** -- specifies exactly how to modify the existing code.

The comment identifies a correctness bug (partial failure leading to inconsistent state) and prescribes a specific fix. This is not a suggestion or a question -- it is a direct request to modify code. The language is imperative and the reviewer expects the change to be made before merge.

## Action

Create sub-task (subtask-30001.md) to implement the transaction wrapping.
