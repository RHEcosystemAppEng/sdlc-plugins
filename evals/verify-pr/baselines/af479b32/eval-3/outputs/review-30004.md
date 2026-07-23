# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: question

## Reasoning

The reviewer is asking for clarification, not requesting a code change:

1. "Have you considered" -- opens with a question, asking whether the author thought about a specific scenario.
2. "Is that intentional?" -- the closing question explicitly asks for the author's intent, indicating the reviewer is unsure whether this is a bug or deliberate behavior.
3. The reviewer observes a behavior ("direct GET still returns deleted SBOMs") and asks whether it was intended, rather than stating it should be changed.

Note: The task description says get.rs should be modified to "add `include_deleted` parameter support" and that "The SBOM ... remains accessible via direct GET with a `?include_deleted=true` parameter." This suggests get.rs modifications were planned but not implemented. However, the reviewer's language is inquisitive -- they are asking for clarification, not commanding a change. The scope containment check separately flags get.rs as an unimplemented file.

**Decision:** Classified as **question**. No sub-task created.
