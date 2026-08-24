# Review Comment Classification: 30004

## Comment

- **ID:** 30004
- **Author:** reviewer-a
- **File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
- **Body:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: question

## Reasoning

The reviewer uses interrogative language throughout, asking for clarification rather than requesting a code change:

- "Have you considered" -- asks whether the author thought about a scenario, not demanding a change
- "Is that intentional?" -- directly asks for clarification on design intent
- The reviewer observes a behavior (get.rs does not filter by deleted_at) and asks whether it is by design

The reviewer does not state that get.rs *should* filter deleted SBOMs, nor does the reviewer instruct the author to add filtering. Instead, the reviewer asks whether the current behavior is intentional, which is a request for clarification.

Note: While this question highlights a real gap (get.rs was listed in "Files to Modify" but was not modified in the PR), the reviewer's framing is explicitly a question, not a directive. The missing get.rs modification is separately captured in the Scope Containment check of the verification report. No sub-task created.
