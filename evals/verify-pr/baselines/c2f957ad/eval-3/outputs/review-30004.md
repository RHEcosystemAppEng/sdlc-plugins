# Review Comment 30004 — Classification

- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/line:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1 (RIGHT)
- **Thread:** top-level, no prior classification reply, so it is **unclassified**.

## Comment text

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` — so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: **question**

## Reasoning

- The comment is phrased as questions ("Have you considered ...?", "Is that intentional?") and asks the author to clarify intent. It does not ask for a specific change.
- Per the classification rules, a question asks for clarification and does not trigger a sub-task.

## Related verification finding (not a reclassification)

The question points at a real gap that the verification checks found independently:
- TC-9103 lists `modules/fundamental/src/sbom/endpoints/get.rs` under **Files to Modify** ("add `include_deleted` parameter support"). The task Description says deleted SBOMs stay accessible via direct GET **with** `?include_deleted=true`.
- `get.rs` does not appear in the PR diff. The Intent Alignment **Scope Containment** check therefore reports **FAIL** because a task-required file is unimplemented. That is where the gap is tracked in the report. The comment itself stays a question.
- No acceptance criterion explicitly covers single-SBOM GET behavior, so Acceptance Criteria is not affected.

## Outcome

- No sub-task created from this comment (classification: question).
- Planned reply (not posted, eval mode):
  `[sdlc-workflow/verify-pr] Classified as **question** — asks for clarification on direct-GET behavior for soft-deleted SBOMs; no code change requested. Note: verification separately flags that get.rs (listed in the task's Files to Modify) is not changed in this PR. No sub-task created.`
