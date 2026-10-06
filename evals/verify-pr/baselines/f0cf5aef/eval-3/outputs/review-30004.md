# Review Comment Classification: 30004

**Comment ID:** 30004
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs
**Line:** 1
**Classification:** question

## Reasoning

The reviewer asks for clarification about the behavior of the GET endpoint for soft-deleted SBOMs: "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`?" followed by "Is that intentional?" This is phrased as a question seeking the author's intent, not as a directive to change the code.

The reviewer observes that `get.rs` does not filter by `deleted_at`, meaning direct GET requests still return deleted SBOMs. While this observation relates to a potential implementation gap (the task specifies modifying `get.rs` to add `include_deleted` parameter support, but no changes appear in the PR diff), the reviewer is asking whether this omission is deliberate rather than directing a fix.

Note: The missing `get.rs` modification is independently flagged by the Scope Containment check (FAIL) since `get.rs` is listed in the task's Files to Modify but has no changes in the PR.

**Action:** No sub-task created. Question-classified feedback does not trigger sub-task creation.
