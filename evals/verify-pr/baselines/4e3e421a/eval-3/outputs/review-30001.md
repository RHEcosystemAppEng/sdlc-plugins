# Review Comment 30001 — Classification

- **Comment ID:** 30001
- **Review ID:** 20001
- **Author:** reviewer-a
- **File/Line:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60 (RIGHT)
- **Thread:** top-level (`in_reply_to_id: null`), no replies, no prior `[sdlc-workflow/verify-pr] Classified as` reply → **unclassified**, processed this run

## Comment text

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: **code change request**

## Reasoning

- The language is directive: "should run ... inside a single database transaction", "Wrap the three operations ...", "use `txn` instead of `self.db`". The reviewer is asking for a specific code modification, not offering an optional alternative.
- It identifies a real correctness defect in the diff. `SbomService::soft_delete` issues three independent `update_many().exec(&self.db)` calls (sbom, sbom_package, sbom_advisory). If the second or third call fails, the earlier updates are already committed. That leaves an SBOM marked deleted while its join rows are not, which breaks the cascade requirement (Acceptance Criterion 7: "Related `sbom_package` and `sbom_advisory` rows are cascade-updated").
- The review that holds this comment has state `CHANGES_REQUESTED` ("A few things to address before we can merge"), which confirms that the reviewer expects a change.
- The fix belongs to the current task. It only touches the soft-delete logic this PR adds, so it does not raise a wider concern.

## Action

- A sub-task is created to address this feedback (see `subtask-1.md`), labels `["ai-generated-jira", "review-feedback"]`, with a "Blocks" link to TC-9103.
- Planned reply (not posted; eval mode):
  `[sdlc-workflow/verify-pr] Classified as **code change request** — sub-task [<SUB-TASK-KEY>](<sub-task-webUrl>) created to address this feedback.`
