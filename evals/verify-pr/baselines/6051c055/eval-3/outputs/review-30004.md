# Review Comment Classification: 30004

## Comment Details

- **Comment ID:** 30004
- **Author:** reviewer-a
- **File:** modules/fundamental/src/sbom/endpoints/get.rs
- **Line:** 1
- **Content:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: question

## Reasoning

The reviewer asks for clarification using question-form language:
- "Have you considered what happens when..." -- solicits the author's reasoning
- "Is that intentional?" -- asks whether the current behavior is by design

The comment does not direct a code change or propose a specific modification. It identifies a potential behavioral inconsistency between the list endpoint (which filters deleted SBOMs by default) and the single-resource GET endpoint (which does not), but frames it as a question rather than a change request. The reviewer is seeking the author's intent before deciding whether a change is needed.

Note: The Scope Containment check independently identified that `get.rs` is missing from the PR diff despite being listed in the task's Files to Modify. This is a separate verification finding, not driven by this review comment's classification.

## Action

No sub-task created. Questions ask for clarification and do not trigger sub-task creation.
