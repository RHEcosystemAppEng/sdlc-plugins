# Review Comment Classification: 30004

**Comment ID:** 30004
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs
**Line:** 1
**Classification:** question

## Reasoning

The reviewer asks a clarifying question: "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`?" and "Is that intentional?" This is phrased as a question seeking clarification on the design intent, not as a directive to change code.

The reviewer observes that `get.rs` does not filter by `deleted_at`, meaning direct GET requests still return soft-deleted SBOMs regardless of the `include_deleted` parameter. This is notable because the task description states the SBOM "remains accessible via direct GET with a `?include_deleted=true` parameter" -- implying GET should respect the parameter. The task also lists `get.rs` as a file to modify with "add `include_deleted` parameter support."

While this question highlights a potential gap in the implementation (the `get.rs` changes were listed in "Files to Modify" but are absent from the diff), the reviewer's language is interrogative rather than directive. They ask whether the current behavior is intentional rather than demanding a change. The missing `get.rs` modification is separately flagged in the scope containment and acceptance criteria analysis.

**Action:** No sub-task created for the question itself. The underlying gap (missing `get.rs` changes) is captured separately in the scope containment finding.
