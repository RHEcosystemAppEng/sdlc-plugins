# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: code change request

## Reasoning

The reviewer uses imperative language ("should run", "Wrap the three operations") directing a specific code modification. This is not a suggestion of an alternative approach -- it is a direct instruction to fix a correctness issue (potential inconsistent state from non-atomic multi-table updates). The reviewer identifies a concrete bug scenario (sbom_advisory update failing after sbom_package succeeds) and prescribes the exact fix (wrapping in a database transaction). This clearly meets the "code change request" classification: the reviewer asks for a code modification.

## Convention Analysis

Not applicable -- this is classified directly as a code change request based on reviewer language. No convention upgrade evaluation needed.
