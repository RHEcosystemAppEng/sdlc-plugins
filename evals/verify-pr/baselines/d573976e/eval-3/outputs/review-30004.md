# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: Question

## Reasoning

The reviewer is asking for clarification about design intent, not requesting a code change. Key language indicators:

- "Have you considered" -- interrogative framing, asking whether the author thought about this scenario
- "Is that intentional?" -- explicitly asking whether the current behavior is by design

The comment raises a valid observation (direct GET by ID does not filter soft-deleted SBOMs), but frames it as a question about whether this is the intended behavior rather than asserting it needs to change. The task description actually specifies that the GET endpoint should support `include_deleted=true`, and the current behavior of returning soft-deleted SBOMs on direct GET may be intentional (the task says "remains accessible via direct GET with a `?include_deleted=true` parameter" which could be interpreted as the parameter being additive to already-accessible direct GETs).

Since the reviewer is seeking clarification rather than requesting a change, this is classified as a question.

**Action:** No sub-task created.
