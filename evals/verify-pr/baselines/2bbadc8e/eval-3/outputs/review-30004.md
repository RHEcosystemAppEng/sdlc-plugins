# Review Comment Classification: Comment 30004

## Comment Details
- **Author:** reviewer-a
- **File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
- **Content:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` — so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: **Question**

## Reasoning

The reviewer is asking for clarification about the current behavior, not requesting a change:

- "Have you considered" — opens a question, not a directive
- "Is that intentional?" — directly asks whether the current behavior is by design
- The comment does not instruct the author to change anything
- The reviewer is seeking to understand the design decision — whether returning soft-deleted SBOMs via direct GET (without `include_deleted=true`) is the intended behavior

Per the task description, the requirement states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." The current behavior (GET returns deleted SBOMs without the parameter) may or may not align with the task spec, but the reviewer is asking about intent, not requesting a fix.

## Action
No sub-task created. Questions do not trigger sub-task creation.
