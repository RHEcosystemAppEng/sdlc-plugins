# Review Comment Classification: 30004

## Comment

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Date**: 2026-04-20T14:40:00Z

## Classification: Question

## Reasoning

The reviewer asks two explicit questions:

1. **"Have you considered what happens when..."** -- this is a clarifying question seeking understanding of the author's intent, not a directive to change code.
2. **"Is that intentional?"** -- this directly asks whether the current behavior is by design.

The comment does not instruct the author to make any change. It raises a potential concern about the GET endpoint's behavior for soft-deleted SBOMs, but frames it entirely as questions for the author to respond to. The reviewer is seeking clarification, not prescribing a fix.

Note: The task description does state that `GET /api/v2/sbom/{id}` should support `include_deleted` parameter and `get.rs` is listed as a file to modify. However, the reviewer's comment is phrased as a question, not a code change request. The reviewer may be pointing toward a gap, but the classification is based on the language used.

## Action

No sub-task created. This is a question for the PR author to answer in the review thread.
