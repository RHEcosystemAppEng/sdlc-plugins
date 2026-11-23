# Review Comment 30004 — Classification

- **Comment ID:** 30004
- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/Line:** `modules/fundamental/src/sbom/endpoints/get.rs:1`
- **Thread:** top-level (`in_reply_to_id: null`), no replies. No existing classification reply, so it is **unclassified**.

## Comment text

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` — so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: **question**

## Reasoning

- The comment is written entirely as questions ("Have you considered ...?", "Is that intentional?"). It asks the author to explain the intended behavior and does not request a specific code change.
- The reviewer leaves both answers open. If direct GET is meant to return deleted SBOMs, no change is needed. If not, a change would be needed. Under Step 4c's language-based rules, that makes it a **question**.

## Related verification finding (separate from classification)

The question touches a real gap that the verification checks found independently:

- **Scope Containment = FAIL** (Intent Alignment): `modules/fundamental/src/sbom/endpoints/get.rs` is in the task's **Files to Modify** ("add `include_deleted` parameter support"), but the PR does not touch it. The task Description says a soft-deleted SBOM "remains accessible via direct GET with a `?include_deleted=true` parameter", which implies direct GET should hide deleted SBOMs unless the flag is set.
- The Intent Alignment sub-agent listed 30004 as the related review comment for that FAIL.

The FAIL is reported in the Scope Containment row of report.md. Reclassifying the reviewer's question to manufacture a sub-task would not be appropriate. The author's answer, together with the Scope Containment FAIL, should drive the follow-up.

## Outcome

- **Sub-task:** none from this comment, because questions do not trigger sub-tasks. The missing `get.rs` work appears in the report as a Scope Containment FAIL that needs attention.
- **Planned reply (not posted, fixture eval):**
  `[sdlc-workflow/verify-pr] Classified as **question** — asks for clarification of intended direct-GET behavior for soft-deleted SBOMs; no code change requested. Note: verification separately found that get.rs (listed in the task's Files to Modify for include_deleted support) is unchanged in this PR — see Scope Containment in the verification report. No sub-task created.`
