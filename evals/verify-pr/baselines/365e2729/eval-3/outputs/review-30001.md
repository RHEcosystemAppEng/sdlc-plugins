# Review Comment 30001 — Classification

- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/Line:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60 (RIGHT)
- **Prior classification reply:** none (unclassified, processed this run)

## Comment

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: **code change request**

## Reasoning

- The reviewer uses directive language ("should run", "Wrap the three operations ... and use `txn`") and asks for a concrete code change, not an optional alternative.
- It describes a real correctness defect in the diff. `SbomService::soft_delete` runs three separate `update_many().exec(&self.db)` calls (on `sbom`, `sbom_package` and `sbom_advisory`) with no transaction. If a later statement fails, the database is left partly soft-deleted: the SBOM is marked deleted while its join rows are not. Because a second DELETE then returns 409, the endpoint cannot recover from this state on its own.
- The fix is scoped to the current task. It changes only `soft_delete` in `modules/fundamental/src/sbom/service/sbom.rs`.

## Outcome

- Sub-task created: see `subtask-1.md` ("Wrap SBOM soft-delete cascade updates in a single database transaction"), labels `ai-generated-jira`, `review-feedback`, linked to TC-9103 with a "Blocks" link.
- Reply that would be posted (not posted, eval mode):
  `[sdlc-workflow/verify-pr] Classified as **code change request** — sub-task [<SUB-TASK-KEY>](<sub-task-webUrl>) created to address this feedback.`
