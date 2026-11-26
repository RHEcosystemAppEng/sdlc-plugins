# Review Comment 30001 — Classification

- **Comment ID:** 30001
- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/Line:** `modules/fundamental/src/sbom/service/sbom.rs:60`
- **Thread:** top-level (`in_reply_to_id: null`), no replies. No existing `[sdlc-workflow/verify-pr] Classified as` reply, so the comment is **unclassified** and gets classified in this run.

## Comment text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: **code change request**

## Reasoning

- The reviewer asks directly for a code change: "should run ... inside a single database transaction", "Wrap the three operations ...", "use `txn` instead of `self.db`". That is not an optional alternative or a question.
- The comment points to a real correctness defect. In the diff, `soft_delete` runs three separate `update_many().exec(&self.db)` calls (sbom, sbom_package, sbom_advisory) with no transaction. If a later call fails, the SBOM stays marked deleted while its join rows do not. A retry then gets 409 Conflict (`deleted_at.is_some()`), so the cascade can never be finished through the API.
- It falls within TC-9103's scope. The task's Implementation Notes and the acceptance criterion "Related `sbom_package` and `sbom_advisory` rows are cascade-updated" cover this cascade logic. The Correctness sub-agent linked this comment to criterion 7 and gave Acceptance Criteria a WARN partly because of it.
- The convention upgrade check does not apply because the comment is already a code change request.

## Outcome

- **Sub-task:** yes. See `subtask-1.md` ("Wrap SBOM soft-delete cascade updates in a single database transaction"), labels `ai-generated-jira`, `review-feedback`, linked with **Blocks** to TC-9103.
- **Root-cause investigation:** triggered. The gap is universal and a method, so it is a skill gap that started in plan-feature, with implement-task contributing. See report.md.
- **Planned reply (not posted, fixture eval):**
  `[sdlc-workflow/verify-pr] Classified as **code change request** — sub-task [<SUB-TASK-KEY>](<sub-task-webUrl>) created to address this feedback.`
