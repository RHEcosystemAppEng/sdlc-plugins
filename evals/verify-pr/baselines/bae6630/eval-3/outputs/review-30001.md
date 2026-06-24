## Review Comment Classification: #30001

**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Comment**: The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

### Classification: Code Change Request

**Reasoning**: The reviewer is making a direct, imperative request for a code change. The language is prescriptive: "should run ... inside a single database transaction", "Wrap the three operations in ...", "use `txn` instead of `self.db`". The reviewer identifies a concrete correctness issue (inconsistent state if a partial failure occurs during the three sequential UPDATE statements) and provides a specific fix with exact code patterns to follow. This is not a suggestion or a question -- it is a clear directive that the code must be changed before merging, consistent with the review state of CHANGES_REQUESTED.

**Action**: Creates a sub-task to wrap the soft_delete operations in a database transaction.
