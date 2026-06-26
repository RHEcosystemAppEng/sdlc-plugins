# Review Comment 30001 — Classification

## Comment
> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

**File**: `modules/fundamental/src/sbom/service/sbom.rs`, line 60

## Classification: Code Change Request

### Reasoning

The reviewer uses directive language throughout:

- **"should run"** — directive, not suggestive. The reviewer is stating what the code must do, not offering an optional improvement.
- **"you'll have inconsistent state"** — identifies a concrete correctness bug (partial failure leaves data inconsistent), framing the change as necessary rather than optional.
- **"Wrap the three operations in..."** — imperative instruction telling the author exactly what to change and how.

The comment identifies a real data integrity risk: if one of the three UPDATE statements fails after the others succeed, the database is left in an inconsistent state with some join tables marked deleted and others not. This is a correctness concern, not a style preference.

The language is entirely directive — there are no hedging words like "could", "might", or "would be nice". The reviewer is requesting a specific code change to fix a correctness issue.

### Action
This comment triggers sub-task creation. The fix involves wrapping the three update operations in `soft_delete` inside a database transaction.
