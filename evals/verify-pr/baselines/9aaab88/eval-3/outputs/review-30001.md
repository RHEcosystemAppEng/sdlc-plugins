# Review Comment Classification: 30001

**Comment ID:** 30001
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs, line 60
**Classification:** code change request

## Reasoning

The reviewer uses directive, imperative language: "The `soft_delete` method **should** run all three UPDATE statements inside a single database transaction." This is followed by a concrete instruction: "**Wrap** the three operations in `self.db.transaction(|txn| { ... })` and **use** `txn` instead of `self.db` for each exec call."

The reviewer identifies a specific correctness issue (inconsistent state if the sbom_advisory update fails after sbom_package succeeds) and prescribes a concrete code change (wrap in a transaction). The language is not suggestive or optional -- it states what "should" happen and provides exact code changes required.

This is a **code change request** because:
- It identifies a real correctness bug (partial failure leaves inconsistent state)
- It uses directive language ("should run", "Wrap the three operations")
- It provides a specific code fix, not an alternative approach
- The reviewer's overall review state is CHANGES_REQUESTED, reinforcing that this requires action

A sub-task will be created to address this feedback.
