# Review Comment Classification: 30001

**Comment ID:** 30001
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs
**Line:** 60
**Classification:** code change request

## Reasoning

The reviewer explicitly requests a specific code modification: wrapping the three `update_many` calls in the `soft_delete` method inside a single database transaction. The language is directive ("should run all three UPDATE statements inside a single database transaction") and prescribes a concrete change ("Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call").

This is a code change request because:
1. The reviewer identifies a correctness defect (inconsistent state if a partial failure occurs between the three sequential UPDATE operations).
2. The reviewer specifies the exact code change needed (use `self.db.transaction()`).
3. The request is not optional or suggestive -- it describes a requirement for data consistency.

The defect is valid: the current implementation executes three independent database operations without transactional guarantees. If `sbom_package` update succeeds but `sbom_advisory` update fails, the database is left in an inconsistent state where the SBOM and its packages are marked deleted but its advisories are not.

**Action:** Sub-task created to address this feedback.
