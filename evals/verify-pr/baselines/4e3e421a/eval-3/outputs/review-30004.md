# Review Comment 30004 — Classification

- **Comment ID:** 30004
- **Review ID:** 20001
- **Author:** reviewer-a
- **File/Line:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1 (RIGHT)
- **Thread:** top-level (`in_reply_to_id: null`), no replies, no prior classification reply → **unclassified**, processed this run

## Comment text

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` — so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: **question**

## Reasoning

- The comment is phrased as questions ("Have you considered ...?", "Is that intentional?"). The reviewer wants to know whether the behavior is intended and does not ask for a specific code change.
- Under Step 4c, a question is a request for clarification and does not trigger a sub-task.

## Related verification finding (orchestrator note)

The question points at a real gap that the Intent Alignment check detects independently:

- The task lists `modules/fundamental/src/sbom/endpoints/get.rs` under **Files to Modify** ("add `include_deleted` parameter support"). The Description says deleted SBOMs remain accessible via direct GET **with** `?include_deleted=true`, which means they should be hidden without it.
- The PR diff does not touch `get.rs`. As a result, **Scope Containment = FAIL** (an unimplemented task file), and comment 30004 is listed in that finding's related review comments.
- The classification stays **question** because the reviewer's wording asks for clarification. The gap is reported through Scope Containment in the verification report and is not turned into a review-feedback sub-task. The PR author should answer the question and implement the `get.rs` change that the task requires.

## Action

- No sub-task created.
- Planned reply (not posted; eval mode):
  `[sdlc-workflow/verify-pr] Classified as **question** — asks for clarification; no code change requested. Note: the task lists get.rs (include_deleted support) under Files to Modify and the PR does not modify it, so this is flagged in the verification report under Scope Containment. No sub-task created.`
