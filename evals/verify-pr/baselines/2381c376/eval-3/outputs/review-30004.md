# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Body:**
> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: Question

## Reasoning

1. **"Have you considered"** -- this is a question opener, asking whether the author thought about a specific scenario.
2. **"Is that intentional?"** -- the reviewer explicitly asks for clarification about whether the current behavior is by design or an oversight.
3. **No directive to change** -- the reviewer does not instruct the author to modify code. Instead, the reviewer asks whether the behavior is expected, leaving the determination to the author.
4. **Seeks clarification** -- the reviewer is asking the author to explain their design decision regarding GET endpoint behavior for soft-deleted SBOMs.

This matches the "question" classification: the reviewer asks for clarification rather than requesting a code change. Note that the reviewer raises a valid point -- the task's Files to Modify includes `get.rs` for adding `include_deleted` parameter support, but this change is not present in the diff. However, the reviewer frames this as a question about intent, not as a directive to change the code.

## Action

No sub-task created. Questions ask for clarification and do not trigger sub-task creation.
