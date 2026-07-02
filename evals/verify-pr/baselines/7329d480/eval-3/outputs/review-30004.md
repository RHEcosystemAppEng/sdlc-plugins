# Review Comment Classification: 30004

**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Date**: 2026-04-20T14:40:00Z

## Comment Text

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: Question

**Reasoning**: The reviewer asks two explicit questions and does not request any code change. The comment is exploratory -- the reviewer is seeking clarification about a design decision rather than directing the author to modify code. Key indicators:

1. **"Have you considered"**: This is an inquiry about awareness and forethought, not a directive to change code. The reviewer is asking whether the author has thought about this scenario.
2. **"Is that intentional?"**: This closing question explicitly asks for clarification on whether the current behavior is by design. The reviewer is not asserting that the behavior is wrong -- they are asking the author to confirm their intent.
3. **No imperative language**: The comment contains no directive words such as "should", "must", "needs to", "fix", "change", or "wrap". It is entirely framed as inquiry.
4. **Observation plus question pattern**: The reviewer notes an observation about the GET endpoint behavior ("it doesn't filter by `deleted_at`") and then asks whether this was a deliberate design choice.

Looking at the task description, it states the SBOM "remains accessible via direct GET with a `?include_deleted=true` parameter", which implies `get.rs` should support the parameter. However, the current behavior -- GET-by-ID always returning the SBOM regardless of soft-delete status -- could be considered a valid interpretation where direct lookups are unrestricted. The reviewer is asking for this design clarification, not requesting a change. No code change is requested.

**Action**: No sub-task created. Questions ask for clarification and do not require code changes.
