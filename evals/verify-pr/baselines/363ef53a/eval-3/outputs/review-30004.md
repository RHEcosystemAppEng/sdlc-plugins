# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: question

## Reasoning

The reviewer uses interrogative language throughout, asking for clarification rather than directing a change:

1. "Have you considered" -- opens with a question about the developer's reasoning, not a directive to change behavior.
2. "Is that intentional?" -- the closing question explicitly asks whether the current behavior was a deliberate design choice. The reviewer does not assert that it is wrong; they ask whether the omission was intended.
3. The reviewer observes a behavior (direct GET returns deleted SBOMs) and seeks clarification on whether it was a conscious decision. This is information-seeking, not action-requesting.

The comment does not ask for a code modification. It raises a potential concern but defers judgment to the developer by asking whether the behavior is intentional. If the developer confirms it is intentional, no change is needed. This is a question seeking clarification, not a code change request.

## Sub-task Required: No
