# Review Comment 30001 — Classification Reasoning

**Comment ID:** 30001
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs (line 60)
**Classification:** code change request

## Reviewer Language Analysis

The reviewer uses imperative language throughout:

- "should run all three UPDATE statements inside a single database transaction" — direct instruction, not a suggestion
- "Wrap the three operations in `self.db.transaction(|txn| { ... })`" — explicit directive with specific API call
- "use `txn` instead of `self.db` for each exec call" — precise implementation instruction

## Substance Analysis

The comment identifies a concrete correctness defect: if the `sbom_advisory` update fails after `sbom_package` succeeds, the database will be left in an inconsistent state where some related rows are marked deleted and others are not. This is a data integrity bug, not a style preference or optional improvement.

The reviewer provides a specific fix (transaction wrapping) and names the exact API to use (`self.db.transaction`). The fix is scoped to a single method in a single file.

## Classification Decision

**Code change request.** The reviewer identifies a real bug (inconsistent state on partial failure) and directs a specific code change (transaction wrapping). The language is imperative ("should run", "Wrap"), the issue affects correctness, and the fix is concrete.

## Action

Sub-task created to address this feedback.
