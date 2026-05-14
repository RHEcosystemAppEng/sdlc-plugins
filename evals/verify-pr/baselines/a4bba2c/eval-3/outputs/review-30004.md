# Review Comment Classification: 30004

## Comment
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs` line 1
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: question

## Reasoning
The reviewer is asking for clarification about the design intent, not requesting a code change. The key phrases are "Have you considered" and "Is that intentional?" which are interrogative, seeking the author's reasoning. The task description states that GET with `include_deleted=true` should return deleted SBOMs, and the current behavior where direct GET returns deleted SBOMs (without filtering) may be intentional by design. The reviewer is seeking confirmation of this design decision, not mandating a change.

## Action
No sub-task created. This asks for clarification; no code change is requested.
