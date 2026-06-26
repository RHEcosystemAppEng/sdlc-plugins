# Review Comment Classification: 30004

**Comment ID:** 30004
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs
**Line:** 1

## Comment Text

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: question

## Reasoning

The reviewer asks a clarifying question ("Have you considered...", "Is that intentional?") rather than directly requesting a code change. The question surfaces a potential gap: the GET-by-ID endpoint does not filter by `deleted_at`, meaning soft-deleted SBOMs remain accessible via direct GET requests. However, the phrasing is deliberately open-ended -- the reviewer is asking whether this behavior is intentional, not asserting that it must be changed.

That said, the task description explicitly lists `modules/fundamental/src/sbom/endpoints/get.rs` under "Files to Modify" with the note "add `include_deleted` parameter support." The PR diff does not include any changes to `get.rs`. This means the gap the reviewer identifies is actually an unimplemented acceptance criterion from the task specification. The Correctness sub-agent independently flagged this as an Acceptance Criteria FAIL.

While the review comment itself is classified as a question (based on the reviewer's language), the underlying issue -- missing `include_deleted` support in the GET endpoint -- is captured as an acceptance criteria failure and will be addressed through that mechanism rather than through a review-feedback sub-task.

## Action

No sub-task created for this question. The underlying issue (missing `include_deleted` support in `get.rs`) is captured as an acceptance criteria failure by the Correctness check and does not need a separate review-feedback sub-task.
