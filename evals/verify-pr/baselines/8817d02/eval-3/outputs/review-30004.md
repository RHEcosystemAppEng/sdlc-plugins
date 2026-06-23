# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: question

## Reasoning

The reviewer uses interrogative language throughout:

1. **"Have you considered..."** -- opens with a question, asking the author to reflect on a specific scenario rather than demanding a change.
2. **"Is that intentional?"** -- closes with another question, explicitly seeking clarification about whether the observed behavior is by design.

The reviewer identifies an apparent gap (GET endpoint returns soft-deleted SBOMs without filtering) but does not assert whether this is a bug or a feature. Notably, the task description itself states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." This means the task description does describe GET behavior with `include_deleted=true`, and the reviewer is asking whether the current implementation (which returns deleted SBOMs on GET without the parameter) matches the author's intent.

The reviewer is seeking clarification rather than requesting a code change. If the author responds that the behavior is intentional (or that the task description permits it), no code change would be needed. This distinguishes it from a code change request, where the reviewer would assert that the behavior is wrong and specify what to change.

## Action

No sub-task created. Question-class feedback requires a response from the PR author, not a tracked code change.
