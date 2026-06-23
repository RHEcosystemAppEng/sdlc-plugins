# Review Comment Classification: 30004

## Comment
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: Question

## Reasoning

The reviewer uses interrogative language throughout:
- "Have you considered..." -- asks whether the author thought about a scenario
- "Is that intentional?" -- explicitly asks for clarification of intent

The reviewer observes a behavior (GET endpoint returns deleted SBOMs without the `include_deleted` parameter) and asks whether this is by design or an oversight. The reviewer does not instruct the author to make a change -- they ask for an explanation.

Notably, the task description states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." This could be interpreted as the GET endpoint requiring `include_deleted=true` to return deleted SBOMs, or that the GET endpoint always returns deleted SBOMs (and `include_deleted=true` is only for list queries). The reviewer is seeking clarification on this ambiguity.

**Classification: question** -- no sub-task created.
