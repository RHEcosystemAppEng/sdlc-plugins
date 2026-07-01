# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: Code Change Request

## Reasoning

The reviewer uses imperative language ("should run", "Wrap the three operations") and identifies a concrete correctness defect: the three UPDATE statements in `soft_delete` are not wrapped in a transaction, which can lead to inconsistent state if a later update fails after an earlier one succeeds. This is not a suggestion or optional improvement -- it is a direct request for a specific code change to prevent data corruption.

The reviewer prescribes the exact fix: wrap in `self.db.transaction(|txn| { ... })` and replace `self.db` with `txn` for each exec call. The language is directive, not suggestive (no hedging like "could", "might want to", "would be nice").

**Action:** Sub-task created to address this feedback.
