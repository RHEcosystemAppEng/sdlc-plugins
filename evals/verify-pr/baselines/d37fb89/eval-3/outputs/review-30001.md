# Review Comment Classification: 30001

## Comment
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: Code Change Request

## Reasoning

The reviewer uses imperative, directive language throughout:
- "should run all three UPDATE statements inside a single database transaction" -- a direct instruction to change the code
- "Wrap the three operations in `self.db.transaction(|txn| { ... })`" -- prescribes the exact code modification
- "use `txn` instead of `self.db` for each exec call" -- specifies what to change

The reviewer identifies a concrete correctness bug (partial failure leading to inconsistent state) and instructs the author to fix it. This is not suggestive or optional -- it describes a defect that must be addressed. The language is unambiguously a request for a code modification.

**Classification: code change request** -- triggers sub-task creation.
