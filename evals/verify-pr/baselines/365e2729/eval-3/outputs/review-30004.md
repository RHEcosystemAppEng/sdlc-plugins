# Review Comment 30004 — Classification

- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/Line:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1 (RIGHT)
- **Prior classification reply:** none (unclassified, processed this run)

## Comment

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` — so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: **question**

## Reasoning

- The comment is phrased as a question ("Have you considered ...?", "Is that intentional?"). It asks the author to clarify intended behavior and does not ask for a specific code change.
- No sub-task is created from this comment. The behavior it asks about does, however, match a separate deterministic finding. The task lists `modules/fundamental/src/sbom/endpoints/get.rs` under **Files to Modify** ("add `include_deleted` parameter support"), and the task Description says deleted SBOMs stay reachable "via direct GET with a `?include_deleted=true` parameter". The PR diff does not touch `get.rs`. The Intent Alignment sub-agent reports this as an unimplemented file (Scope Containment = FAIL), and the verification report covers it there. It is not turned into a review-feedback sub-task, because the reviewer did not request a change.

## Outcome

- No sub-task created.
- Reply that would be posted (not posted, eval mode):
  `[sdlc-workflow/verify-pr] Classified as **question** — asks for clarification of intended GET-by-id behavior for soft-deleted SBOMs; no code change requested. Note: get.rs is listed in the task's Files to Modify but is not changed in this PR (reported as Scope Containment FAIL in the verification report). No sub-task created.`
