## Review Comment 30001 — Classification

**Reviewer:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

### Classification: Code change request

**Reasoning:** The reviewer uses directive language throughout: "should run all three UPDATE statements inside a single database transaction" is a clear requirement, not a suggestion. The reviewer identifies a concrete correctness issue (inconsistent state if a partial failure occurs) and prescribes the exact fix ("Wrap the three operations in `self.db.transaction(|txn| { ... })`"). The word "should" here is used in the directive/imperative sense (this must be done to avoid a bug), not the suggestive sense. The reviewer also provides specific implementation instructions, reinforcing that this is an expected code change, not an optional improvement.

**Action:** Creates sub-task (see subtask-30001.md).
