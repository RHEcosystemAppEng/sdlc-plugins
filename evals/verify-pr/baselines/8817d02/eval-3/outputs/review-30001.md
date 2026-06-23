# Review Comment Classification: 30001

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60
**Text:** "The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: code change request

## Reasoning

The reviewer uses directive language throughout the comment:

1. **"should run"** -- prescriptive directive indicating the reviewer considers this a required change, not an optional improvement.
2. **"Wrap the three operations in..."** -- explicit instruction specifying the exact code change expected.
3. **"use `txn` instead of `self.db`"** -- concrete implementation guidance that leaves no ambiguity about what must change.

The reviewer also provides a clear justification for why the change is necessary: without a transaction wrapper, a partial failure (e.g., `sbom_advisory` update fails after `sbom_package` succeeds) would leave the database in an inconsistent state. This is a correctness concern, not a stylistic preference.

The language pattern matches "code change request" classification: the reviewer is asking for a specific code modification with a rationale grounded in data integrity. This is not suggestive ("could", "might consider") or interrogative ("have you considered?") -- it is imperative.

## Action

Sub-task creation required. The fix is scoped to `modules/fundamental/src/sbom/service/sbom.rs` -- wrapping the three `update_many` calls in `self.db.transaction()`.
