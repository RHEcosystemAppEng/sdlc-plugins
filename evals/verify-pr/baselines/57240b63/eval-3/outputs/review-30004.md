# Review Comment Classification: 30004

## Comment
**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text**: Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: Question

## Reasoning

The reviewer asks for clarification using question-form language:
- "Have you considered what happens when..." -- inquiry about the author's intent
- "Is that intentional?" -- explicitly asks whether the current behavior is by design

The reviewer does not request a code change or suggest an alternative. They observe a behavior (direct GET returns deleted SBOMs without filtering) and ask the author to clarify whether this is the intended design. Notably, the task description states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." This suggests the current GET behavior may actually be a gap, but the reviewer frames it as a question rather than a change request.

The classification is based on the reviewer's language, not on whether the behavior is correct.

## Sub-task Required: NO

Questions do not trigger sub-task creation. They require a response from the PR author.
