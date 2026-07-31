# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: QUESTION

## Reasoning

The reviewer is asking for clarification about the intended behavior, not requesting a code change:

1. **"Have you considered"** -- this is a question opener that asks whether the author thought about a particular scenario. It invites explanation, not action.
2. **"Is that intentional?"** -- the closing question explicitly asks the author to clarify their intent. The reviewer is uncertain whether the current behavior (GET returning soft-deleted SBOMs) is a design decision or an oversight, and seeks clarification before forming an opinion.
3. **No directive language** -- unlike comment 30001 ("should run", "Wrap the three operations"), this comment contains no imperative instructions. The reviewer observes the current behavior and asks about it rather than prescribing a fix.
4. **Exploratory tone** -- "Looking at `get.rs`, it doesn't filter by `deleted_at`" is an observation shared to frame the question, not a statement that filtering must be added.

The reviewer is seeking clarification about a design decision. The task description does state that the SBOM "remains accessible via direct GET with a `?include_deleted=true` parameter," which implies the GET endpoint should have filtering -- but this comment asks about the behavior rather than requesting a change. No sub-task is created for questions; the appropriate response is to provide clarification.
