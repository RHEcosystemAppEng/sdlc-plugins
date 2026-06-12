# Review Comment Classification: 30004

**Comment ID:** 30004
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs
**Line:** 1
**Classification:** question

## Reasoning

The reviewer asks "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`?" and follows with "Is that intentional?" This is a question seeking clarification about the intended behavior of the GET endpoint for deleted SBOMs.

This is classified as a question because:
1. The reviewer uses interrogative language ("Have you considered...?", "Is that intentional?").
2. The reviewer is not requesting a code change -- they are asking whether the current behavior (GET by ID still returns soft-deleted SBOMs without filtering) is deliberate.
3. The task description does specify that `get.rs` should "add `include_deleted` parameter support," but the diff shows no changes to `get.rs`. However, the reviewer frames this as a design question, not a change request.
4. The question raises a valid point: the task's Files to Modify list includes `get.rs` for `include_deleted` support, yet the PR diff shows no changes to that file. This could be an oversight or a deliberate design choice (e.g., allowing direct GET by ID to always return the SBOM regardless of deletion status).

Note: The Scope Containment check records `get.rs` as present in PR files (it appears in the diff header) but shows 0 additions/0 deletions, meaning the file was not actually modified. The task specification required changes to `get.rs`, which may indicate an incomplete implementation. However, this review comment is a question, not a change request, so it does not trigger sub-task creation on its own. The acceptance criteria gap (missing `include_deleted` support in GET) is captured separately in the Acceptance Criteria check.

**Action:** No sub-task created.
