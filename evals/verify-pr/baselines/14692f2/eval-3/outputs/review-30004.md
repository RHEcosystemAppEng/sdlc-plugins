# Review Comment Classification: 30004

## Comment

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Review ID:** 20001

## Classification: Question

## Reasoning

The reviewer uses question language throughout:

1. **"Have you considered"** -- This is an open-ended question asking for the author's perspective, not a directive to change the code.
2. **"Is that intentional?"** -- This explicitly asks whether the current behavior is by design. The reviewer is seeking clarification, not asserting that a change is needed.

The reviewer identifies a potential behavioral gap (GET returning soft-deleted SBOMs without filtering) but frames it as a question rather than a request. The reviewer does not state that the behavior is wrong or ask for a specific fix -- they ask whether the author has thought about it and whether it is intentional.

Notably, looking at the task description, the acceptance criteria state: "GET /api/v2/sbom?include_deleted=true includes soft-deleted SBOMs" (for the list endpoint). The task description also specifies adding `include_deleted` parameter support to `get.rs`, but the diff does not show changes to `get.rs` for filtering. However, since the reviewer frames this as a question rather than a code change request, it is classified based on the reviewer's language, not the verifier's assessment.

No sub-task is created for questions.
