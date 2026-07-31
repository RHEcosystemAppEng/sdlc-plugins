# Review Comment Classification: #30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: CODE CHANGE REQUEST

## Reasoning

The reviewer is identifying a correctness defect and requesting a specific code modification. Key indicators:

1. **Imperative language requesting a code change:** "should run all three UPDATE statements inside a single database transaction" and "Wrap the three operations in `self.db.transaction(|txn| { ... })`" are direct instructions to change the code, not optional suggestions.

2. **Identifies a concrete failure mode:** "If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state." The reviewer describes a specific bug scenario where partial execution leads to data inconsistency.

3. **Prescribes the exact fix:** The reviewer provides the specific API call (`self.db.transaction(|txn| { ... })`) and the change required (`use txn instead of self.db`), leaving no ambiguity about what needs to happen.

This is not a suggestion (no optional language like "you might consider" or "it would be nice"), not a nit (it affects correctness, not style), and not a question (no request for clarification). The reviewer is requiring a code change to prevent a data consistency bug.

## Action

Sub-task creation required. The three sequential UPDATE statements in `soft_delete` must be wrapped in a database transaction to ensure atomicity of the cascade operation.
