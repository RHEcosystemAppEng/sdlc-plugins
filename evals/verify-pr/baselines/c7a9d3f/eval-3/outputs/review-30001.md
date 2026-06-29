# Review Comment Classification: 30001

**Comment ID:** 30001
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs
**Line:** 60
**Content:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: code change request

## Reasoning

The reviewer explicitly asks for a specific code modification: wrapping the three UPDATE statements in a database transaction. This is not a suggestion of an alternative approach -- it identifies a concrete correctness bug (partial failure leading to inconsistent state) and prescribes a specific fix (use `self.db.transaction()`). The language is directive ("should run", "Wrap the three operations") and the justification is a concrete failure scenario ("If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state").

This is a valid correctness concern. The `soft_delete` method currently executes three independent `update_many` calls against `sbom`, `sbom_package`, and `sbom_advisory` without transactional guarantees. If any intermediate update fails (e.g., due to a database constraint violation or connection drop), the SBOM record would be marked as deleted while related join table rows remain active, creating an inconsistent data state.

**Action:** Sub-task created to address this feedback.
