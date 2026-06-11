# Review Comment Classification: 30004

## Comment
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs
**Line:** 1
**Text:** Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` — so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: question

## Reasoning
The reviewer uses question-form language ("Have you considered", "Is that intentional?") and is asking for clarification about a design decision. The reviewer observes that `get.rs` does not filter by `deleted_at` and asks whether this is intentional behavior or an oversight.

Notably, the task description explicitly lists `modules/fundamental/src/sbom/endpoints/get.rs` as a file to modify with the note "add `include_deleted` parameter support," and the acceptance criteria include "GET /api/v2/sbom?include_deleted=true includes soft-deleted SBOMs." The PR diff does not show any changes to `get.rs`, suggesting this file was not modified as specified. However, the reviewer's comment is phrased as a question seeking clarification, not as a directive to make a change.

This gap is separately flagged by the Acceptance Criteria check (the task required `get.rs` modifications that are absent from the PR), but the review comment itself is classified based on the reviewer's language and intent, which is interrogative. No sub-task is created for question classifications.
