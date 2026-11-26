# Review Comment 30001 — Classification

- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/line:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60 (RIGHT)
- **Thread:** top-level (`in_reply_to_id: null`), no prior `[sdlc-workflow/verify-pr] Classified as` reply, so it is **unclassified** and goes to classification.

## Comment text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: **code change request**

## Reasoning

- The reviewer uses directive language ("should run", "Wrap the three operations ...", "use `txn` instead of `self.db`") and gives a concrete fix. This is a request to change code, not an optional alternative.
- The diff confirms the defect. `SbomService::soft_delete` runs three separate `update_many().exec(&self.db)` calls with no transaction. If the second or third statement fails, the `sbom` row stays marked deleted while some join-table rows do not. That is a correctness / data-integrity problem.
- It is in scope for TC-9103. The task's Implementation Notes ask for cascade updates of `sbom_package` and `sbom_advisory` using the same timestamp, so a partial cascade breaks the intent of acceptance criterion "Related `sbom_package` and `sbom_advisory` rows are cascade-updated".
- No convention upgrade is needed because the comment is already a code change request.

## Outcome

- Sub-task created: **subtask-1**, "Wrap SBOM soft-delete cascade updates in a single database transaction" (labels `ai-generated-jira`, `review-feedback`; linked with Blocks to TC-9103).
- Planned reply (not posted, eval mode):
  `[sdlc-workflow/verify-pr] Classified as **code change request** — sub-task [<SUB-TASK-KEY>](<sub-task-webUrl>) created to address this feedback.`
