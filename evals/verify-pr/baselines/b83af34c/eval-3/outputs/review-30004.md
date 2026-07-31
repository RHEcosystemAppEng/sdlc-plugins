# Review Comment Classification: #30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: QUESTION

## Reasoning

The reviewer is asking for clarification about design intent, not requesting a code change. Key indicators:

1. **Interrogative framing:** The comment uses two explicit questions: "Have you considered what happens when..." and "Is that intentional?" Both seek to understand the author's reasoning rather than prescribing a change.

2. **Exploratory language:** "Have you considered" is a clarification probe, not an instruction. The reviewer is checking whether the current behavior is a deliberate design choice or an oversight.

3. **No directive to change code:** Unlike comment #30001 which says "Wrap the three operations in...", this comment does not instruct the author to modify `get.rs`. It asks whether the current behavior is intentional.

4. **Observation followed by question:** The reviewer observes a behavior ("it doesn't filter by `deleted_at`") and then asks whether that behavior is by design. This is a request for information, not a request for a code change.

Note: This comment does relate to a scope containment finding -- `get.rs` is listed in the task's Files to Modify but was not changed in the PR. The task description says "remains accessible via direct GET with a `?include_deleted=true` parameter", suggesting `get.rs` should have been modified. However, the reviewer's comment is phrased as a question, so it is classified as such. The scope containment gap is captured separately in the verification report.

## Action

No sub-task created. This is a request for clarification; no code change is implied by the classification.
