# Review Comment 30004 — Classification

- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/Line:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1 (RIGHT)
- **Thread:** top-level (`in_reply_to_id: null`), no replies, no prior classification reply. Status: unclassified, so it is classified in this run.

## Comment text

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` — so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: **Question**

## Reasoning

- The comment is phrased as questions ("Have you considered...?", "Is that intentional?"). It asks the author to clarify intended behavior and does not ask for a specific code change.
- The question does point at a real gap, which is reported separately through the deterministic checks:
  - TC-9103 lists `modules/fundamental/src/sbom/endpoints/get.rs` under **Files to Modify** ("add `include_deleted` parameter support"). That file is **not** in the PR diff, so the Scope Containment check is **FAIL** (unimplemented file).
  - The task Description says deleted SBOMs remain accessible "via direct GET with a `?include_deleted=true` parameter". The PR does not add this parameter.
- Reclassifying a question as a code change request based on what it implies would go beyond the reviewer's own wording, which the skill uses for classification. The gap is tracked through the Scope Containment FAIL in the report and needs a human decision.

## Outcome

- No sub-task created from this comment. The missing `get.rs` change is reported as a Scope Containment FAIL.
- Reply (would be posted to the thread):
  `[sdlc-workflow/verify-pr] Classified as **question** — asks for clarification of intended behavior; no code change requested. Note: get.rs is listed in the task's Files to Modify (include_deleted support) but is not changed in this PR, which is reported as a Scope Containment FAIL in the verification report. No sub-task created.`
