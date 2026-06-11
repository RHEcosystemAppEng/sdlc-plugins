# Review Comment Classification: 30004

## Comment
**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text**: "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: QUESTION

## Reasoning

1. **Interrogative form**: The comment is phrased entirely as questions -- "Have you considered...?" and "Is that intentional?" The reviewer is asking for clarification about a design decision, not requesting a code change.

2. **Seeking intent, not prescribing a fix**: The reviewer observes that `get.rs` does not filter by `deleted_at`, but rather than directing the author to add filtering, they ask whether this behavior is intentional. This acknowledges that returning deleted SBOMs via direct GET may be a deliberate design choice (the task description does specify that SBOMs "remain accessible via direct GET with a `?include_deleted=true` parameter").

3. **No directive language**: Unlike comment 30001 ("Wrap the three operations..."), this comment does not tell the author what to change. It asks for an explanation.

4. **Design clarification context**: The task description states SBOMs should be "accessible via direct GET with a `?include_deleted=true` parameter", which implies the GET endpoint should support the parameter. However, whether a non-deleted-filtered GET is a bug or intentional simplification is a design question the reviewer wants answered.

## Result

Classification: **question** -- no sub-task created. Noted in the verification report as requiring a response from the PR author.
