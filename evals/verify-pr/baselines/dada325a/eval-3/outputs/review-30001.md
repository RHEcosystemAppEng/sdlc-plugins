# Review Comment 30001 — Classification

- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/Line:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60 (RIGHT)
- **Thread:** top-level (`in_reply_to_id: null`), no replies, no prior `[sdlc-workflow/verify-pr] Classified as` reply. Status: unclassified, so it is classified in this run.

## Comment text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: **Code change request**

## Reasoning

- The reviewer uses directive language: "should run ... inside a single database transaction" and "Wrap the three operations ... and use `txn` instead of `self.db`". That asks for a specific code change. It is not phrased as an optional alternative.
- The comment points to a real correctness defect in the diff. `SbomService::soft_delete` runs three separate `update_many().exec(&self.db)` calls (sbom, sbom_package, sbom_advisory) with no transaction. If a later statement fails, the earlier updates are already committed and the data is left partly deleted. For example, the SBOM could be marked deleted while its advisory rows are not.
- This affects the acceptance criterion "Related `sbom_package` and `sbom_advisory` rows are cascade-updated". The cascade works on the happy path, but it is not atomic.
- The convention-upgrade check does not apply because the comment is already a code change request.

## Outcome

- A sub-task is created (see `subtask-1.md`) with labels `["ai-generated-jira", "review-feedback"]` and a "Blocks" link to TC-9103.
- Reply (would be posted to the thread):
  `[sdlc-workflow/verify-pr] Classified as **code change request** — sub-task [<SUB-TASK-KEY>](<sub-task-webUrl>) created to address this feedback.`
