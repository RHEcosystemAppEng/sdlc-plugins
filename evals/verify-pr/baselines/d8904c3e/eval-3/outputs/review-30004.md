# Review Comment Classification: Comment 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: question

## Reasoning

The reviewer asks for clarification rather than requesting a code change:

1. **"Have you considered"** -- this phrasing invites the author to reflect on a potential gap, rather than directing them to make a change. It leaves open the possibility that the current behavior is intentional.
2. **"Is that intentional?"** -- this explicitly asks for confirmation of intent, which is the hallmark of a question classification. The reviewer is seeking understanding of the design decision, not asserting that a change is needed.
3. **No directive language** -- unlike comment 30001 which uses "should", "Wrap", and "use", this comment contains no imperative verbs or instructions to modify code.
4. **Observational framing** -- the reviewer describes what they observe ("it doesn't filter by `deleted_at`") and asks whether that observation represents a bug or a deliberate choice.

The reviewer has identified that `get.rs` was listed in the task's Files to Modify but was not changed in the PR. However, instead of directing a fix, they ask whether the current behavior (direct GET returning deleted SBOMs) is intentional. This matches the **question** classification: the reviewer asks for clarification, and no code change is implied as mandatory.

## Action

No sub-task created. Questions do not trigger sub-task creation; they require a human response from the PR author.
