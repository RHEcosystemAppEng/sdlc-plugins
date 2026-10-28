# Review Comment Classification: #30001

## Comment
"The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call."

## Classification: CODE CHANGE REQUEST

## Reasoning
The reviewer uses imperative language ("should run", "Wrap the three operations") that directly instructs the author to make a specific code modification. The comment identifies a concrete correctness defect -- the three UPDATE statements in `soft_delete` are not wrapped in a transaction, which can lead to inconsistent state if a later statement fails after an earlier one succeeds. The reviewer prescribes the exact fix: use `self.db.transaction(|txn| { ... })` and substitute `txn` for `self.db` in each exec call. This is not a suggestion or optional improvement; it addresses a data integrity risk that constitutes a required code change. A sub-task is created to track this fix.
