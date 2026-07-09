## Review Comment Classification: #30004

**Comment ID:** 30004
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs` (line 1)
**Classification:** question

### Reviewer Text

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

### Reasoning

The reviewer asks two explicit questions: "Have you considered..." and "Is that intentional?" The comment does not request a change -- it asks the PR author to clarify whether the current behavior (direct GET returning soft-deleted SBOMs without filtering) is intentional or an oversight.

The reviewer's observation is valid: `get.rs` is listed in the task's Files to Modify with the note "add `include_deleted` parameter support," but the PR diff does not include changes to `get.rs`. However, the reviewer frames this as a question seeking clarification rather than a directive to change the code.

This relates to the Scope Containment finding: `get.rs` is listed in the task specification's Files to Modify but is absent from the PR diff.

### Action

No sub-task created. Questions do not trigger sub-task creation -- they require the PR author's response to determine whether a code change is needed.
