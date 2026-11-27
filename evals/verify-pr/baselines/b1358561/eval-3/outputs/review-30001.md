# Review Comment 30001 — Classification

- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/Line:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60 (RIGHT)
- **Thread:** top-level (`in_reply_to_id: null`), no replies, no prior `[sdlc-workflow/verify-pr] Classified as` reply → **unclassified**, processed this run

## Comment text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: **Code change request**

## Reasoning

- The reviewer uses directive language ("should run", "Wrap the three operations ...", "use `txn` instead of `self.db`") and prescribes a concrete modification. It is not framed as optional.
- It points to a real correctness defect visible in the diff. `SbomService::soft_delete` runs three separate `update_many().exec(&self.db)` calls against `sbom`, `sbom_package` and `sbom_advisory` with no transaction. If the second or third statement fails, the `sbom` row stays marked deleted while some join rows do not. That partial state also breaks the cascade acceptance criterion ("Related `sbom_package` and `sbom_advisory` rows are cascade-updated").
- The fix belongs to the current task: the method was introduced by this PR.

## Outcome

- Sub-task created: see `subtask-1.md` ("Wrap SBOM soft-delete cascade updates in a single database transaction").
- Labels: `ai-generated-jira`, `review-feedback`; link: sub-task **Blocks** TC-9103.
- Reply that would be posted (inline thread reply):
  `[sdlc-workflow/verify-pr] Classified as **code change request** — sub-task [<SUB-TASK-KEY>](<sub-task-webUrl>) created to address this feedback.`
