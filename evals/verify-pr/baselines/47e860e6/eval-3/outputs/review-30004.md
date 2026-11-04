# Review Comment 30004 — Classification

- **Comment ID:** 30004
- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/Line:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1 (RIGHT)
- **Thread:** top-level (no `in_reply_to_id`), no replies
- **Prior classification reply:** none, so the comment is unclassified and goes through classification

## Original comment

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` — so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: **question**

## Reasoning

- **The comment is phrased as questions.** It opens with "Have you considered...?" and ends with "Is that intentional?". The reviewer wants to know whether the current behaviour of direct GET is a deliberate design choice. They do not prescribe a change.
- **It asks for clarification, not a modification.** The reviewer neither asks for a filter on `deleted_at` in `get.rs` nor proposes an implementation. Either answer ("yes, intentional" or "no, let's change it") is possible.
- **Context from the verification.** The question points at a real spec gap. The task's Files to Modify lists `modules/fundamental/src/sbom/endpoints/get.rs` ("add `include_deleted` parameter support"), and the Description says soft-deleted SBOMs remain accessible via direct GET with `?include_deleted=true`. The PR does not modify `get.rs`. The report already flags this independently as a **Scope Containment FAIL** from the Intent Alignment sub-agent. That finding stands on its own. It does not turn the reviewer's question into a code change request: the classification follows the reviewer's language, and only code change requests trigger sub-task creation.

## Outcome

- **Sub-task created:** no. Questions do not trigger sub-task creation.
- **Reply that would be posted to the thread** (eval mode, so not posted):

  ```
  gh api repos/trustify/trustify-backend/pulls/744/comments/30004/replies -f body="[sdlc-workflow/verify-pr] Classified as **question** — asks for clarification on whether direct GET returning soft-deleted SBOMs is intentional; no code change requested. Note: the verification report independently flags that get.rs (listed in the task's Files to Modify for include_deleted support) is not modified in this PR. No sub-task created."
  ```
