# Review Comment Classification: Comment 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: code change request

## Reasoning

The reviewer uses directive language throughout this comment:

1. **"should run"** -- states that the three UPDATE statements must be wrapped in a transaction, framing this as a requirement rather than an optional improvement.
2. **"Wrap the three operations"** -- imperative verb giving a direct instruction to make a specific code change.
3. **"use `txn` instead of `self.db`"** -- prescribes the exact implementation approach, specifying which variable to substitute.

The reviewer also provides a concrete justification for why the change is necessary: "If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state." This identifies a real correctness defect (partial failure leaves the database in an inconsistent state), reinforcing that this is a required fix, not an optional suggestion.

The language pattern matches the **code change request** classification: the reviewer asks for a code modification with directive language and provides the specific change to make.

## Action

Sub-task creation triggered. A Jira sub-task will be created to address this feedback.
