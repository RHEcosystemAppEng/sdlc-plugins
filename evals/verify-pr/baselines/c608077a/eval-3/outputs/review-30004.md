# Review Comment 30004 — Classification

- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **Location:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1 (RIGHT)
- **Thread:** top-level comment with no replies. No earlier classification reply exists, so the comment is **unclassified**.

## Comment

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` — so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: **Question**

## Reasoning

- **The reviewer asks a question.** It is phrased as questions ("Have you considered …?", "Is that intentional?"). The reviewer wants clarification on intent and does not prescribe a change.
- Under Step 4c, a request for clarification is a Question, so no review-feedback sub-task comes from the comment itself.
- **The question does point at a real gap, which verification raises separately.** TC-9103 lists `modules/fundamental/src/sbom/endpoints/get.rs` under Files to Modify ("add `include_deleted` parameter support"). The Description says a deleted SBOM "remains accessible via direct GET with a `?include_deleted=true` parameter". The PR does not touch `get.rs`.
  - The Intent Alignment sub-agent's Scope Containment check reported this as FAIL (a required file was not changed) and recommended a sub-task.
  - That sub-task (`subtask-2.md`) comes from the task-specification gap, not from reclassifying this comment. The planned reply links to it for transparency.

## Outcome

- **Sub-task created from this comment:** no. The related scope-gap sub-task `subtask-2.md` was created by the Intent Alignment finding.
- **Planned reply (not posted):**
  `[sdlc-workflow/verify-pr] Classified as **question** — asks for clarification about direct-GET behavior for soft-deleted SBOMs; no code change requested by the comment itself. Note: verification independently found that get.rs (listed in TC-9103's Files to Modify) was not changed, and sub-task <SUB-TASK-KEY> tracks adding include_deleted support to GET /api/v2/sbom/{id}. No sub-task created for this comment.`
