# Review Comment Classification: 30004

**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Date**: 2026-04-20T14:40:00Z

## Comment Text

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: Question

**Reasoning**: The reviewer is asking for clarification, not requesting a code change. The language is entirely interrogative:

1. **"Have you considered"** -- This is an open-ended question seeking to understand the author's thought process, not a directive to change behavior.
2. **"Is that intentional?"** -- This explicitly asks whether the current behavior is by design, indicating the reviewer does not know whether a change is needed and is deferring to the author's judgment.

The reviewer observes that `get.rs` does not filter by `deleted_at`, meaning a direct GET request for a soft-deleted SBOM will still return it without requiring `include_deleted=true`. The reviewer wants to know if this is the intended design before forming an opinion on whether a change is needed.

Looking at the task description, the specification states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." This implies `get.rs` should support the `include_deleted` parameter, and indeed `get.rs` is listed in the task's "Files to Modify" section. However, the reviewer is asking a question, not requesting a change -- they want the author to confirm intent. The resolution of this question (whether `get.rs` needs modification) requires author or team input, not an autonomous sub-task.

**Action**: No sub-task created. Questions require author/team clarification, not autonomous code changes.
