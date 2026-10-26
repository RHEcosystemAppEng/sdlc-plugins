# Review Comment Classification: #30001

## Author: reviewer-a
## File: modules/fundamental/src/sbom/service/sbom.rs
## Line: 60

## Comment Text
The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: code change request

## Reasoning
The reviewer uses directive language throughout this comment. "should run all three UPDATE statements inside a single database transaction" is a clear directive stating what the code must do. "Wrap the three operations in `self.db.transaction(|txn| { ... })`" is an explicit instruction to make a specific code change, with the exact API call and variable name specified. The reviewer also identifies a concrete correctness issue (inconsistent state if a later UPDATE fails after an earlier one succeeds), which makes this a required fix rather than an optional improvement. The imperative tone ("Wrap", "use `txn` instead of") leaves no ambiguity that this is a required change, not a suggestion.

This comment creates a sub-task (subtask-30001.md).
