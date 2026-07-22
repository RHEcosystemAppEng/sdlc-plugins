## Review Comment 30001 -- Classification: Code Change Request

**Comment by:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs, line 60
**Comment text:** The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

### Classification Reasoning

This comment is classified as a **code change request** because:

1. **Directive language:** The reviewer uses imperative phrasing -- "should run all three UPDATE statements inside a single database transaction" and "Wrap the three operations in `self.db.transaction`." This is a direct instruction to change the code, not a suggestion or optional proposal.

2. **Identifies a concrete defect:** The reviewer identifies a real data consistency issue -- if one of the three UPDATE operations fails after another succeeds, the database will be left in an inconsistent state with some related rows marked as deleted and others not. This is a correctness problem, not a style preference.

3. **Specifies the exact fix:** The reviewer prescribes the specific code change needed -- use `self.db.transaction(|txn| { ... })` and replace `self.db` with `txn` in each exec call. This is a clear, actionable code modification request.

4. **No hedging or optional language:** The comment does not use suggestive phrases like "you might consider", "it would be nice", or "have you thought about". It states what the code should do and why the current approach is incorrect.

### Action

Sub-task created to address this feedback. The fix requires wrapping the three `update_many` operations in the `soft_delete` method inside a database transaction to ensure atomicity.
