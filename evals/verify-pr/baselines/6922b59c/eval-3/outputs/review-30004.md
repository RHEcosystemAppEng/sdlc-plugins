# Review Comment Classification: #30004

## Author: reviewer-a
## File: modules/fundamental/src/sbom/endpoints/get.rs
## Line: 1

## Comment Text
Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: question

## Reasoning
The reviewer asks two explicit questions: "Have you considered..." and "Is that intentional?" This is inquiry-seeking language that requests clarification about a design decision rather than directing a code change. The reviewer observes that `get.rs` does not filter by `deleted_at`, but instead of instructing the author to add filtering, they ask whether the current behavior is intentional. This leaves the decision to the PR author -- the reviewer is flagging a potential concern for discussion, not demanding a modification.

The observation is valid: the task description lists `get.rs` in Files to Modify with "add `include_deleted` parameter support", but the diff shows no changes to `get.rs`. However, the acceptance criteria for TC-9103 do not explicitly require `GET /api/v2/sbom/{id}` to filter by `deleted_at` (criteria 5 and 6 reference the list endpoint `GET /api/v2/sbom`, not the individual resource endpoint). This may represent an implementation gap or an intentional design choice.

No sub-task is created for questions.
