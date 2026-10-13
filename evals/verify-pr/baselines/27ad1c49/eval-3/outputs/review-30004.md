# Review Comment Classification: 30004

## Comment

- **Author:** reviewer-a
- **File:** `modules/fundamental/src/sbom/endpoints/get.rs`
- **Line:** 1
- **Body:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: Question

## Reasoning

The reviewer asks for clarification about a design decision using question-form language: "Have you considered..." and "Is that intentional?" These are not directives or requests for code changes -- they are seeking the author's reasoning about the current behavior.

While the comment implicitly identifies a potential gap (get.rs not filtering by `deleted_at`), the reviewer frames it as a question about intent rather than a request to change the code. The reviewer is asking whether the current behavior (direct GET returning deleted SBOMs without filtering) is a deliberate design choice or an oversight.

Key language indicators:
- "Have you considered" -- asks for reflection, not action
- "Is that intentional?" -- seeks clarification about design intent
- No imperative language (no "should", "must", "add", "change")

Note: The Scope Containment check independently identifies `get.rs` as an unimplemented file (listed in the task's Files to Modify but absent from the PR diff), which produces a FAIL verdict. This is a separate finding from the review comment classification.

## Action

No sub-task created. The reviewer is asking for clarification, not requesting a code change. The scope containment finding addresses the same gap through a different mechanism.
