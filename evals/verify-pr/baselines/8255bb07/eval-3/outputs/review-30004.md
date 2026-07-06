# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: question

## Reasoning

The reviewer uses interrogative language throughout: "Have you considered", "Is that intentional?" These are questions asking for clarification about the design intent, not requests for a code change. The reviewer is probing whether the current behavior (GET by ID returns soft-deleted SBOMs without requiring `include_deleted=true`) is deliberate or an oversight.

While the question highlights a potential gap -- `get.rs` was listed in the task's "Files to Modify" but was not changed in the PR -- the reviewer frames this as a question about intent rather than a directive to fix it. The reviewer is seeking the author's reasoning before deciding whether a change is needed.

Note: The task description does state that `get.rs` should be modified to "add `include_deleted` parameter support," which suggests the reviewer's observation is valid. However, the reviewer chose to ask rather than request a change, so the classification reflects the reviewer's framing.

## Action

No sub-task created. This is a clarification question; no code change is directly requested.
