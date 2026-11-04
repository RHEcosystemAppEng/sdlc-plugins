# Review Comment 30001 — Classification

- **Comment ID:** 30001
- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **File/Line:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60 (RIGHT)
- **Thread:** top-level (no `in_reply_to_id`), no replies
- **Prior classification reply (`[sdlc-workflow/verify-pr] Classified as`):** none, so the comment is unclassified and goes through classification

## Original comment

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: **code change request**

## Reasoning

- **The language is directive.** The reviewer says the method "should run all three UPDATE statements inside a single database transaction". They then give imperative instructions: "**Wrap** the three operations in `self.db.transaction(...)` and **use** `txn` instead of `self.db`". They are asking for a specific code change, not floating an alternative.
- **The reviewer gives a correctness reason.** "If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state." The diff confirms it: `SbomService::soft_delete` runs three separate `update_many().exec(&self.db)` calls with no shared transaction.
- **The failure mode is worse than it first looks.** The Correctness sub-agent pointed this out. If the `sbom` row update succeeds and a later cascade update fails, the SBOM already has `deleted_at` set. A retry then hits the `sbom.deleted_at.is_some()` guard and returns 409 Conflict, so the cascade can never be completed through the API. That breaks the intent of acceptance criterion 7 ("Related `sbom_package` and `sbom_advisory` rows are cascade-updated") whenever a partial failure occurs.
- **The review state supports it.** Review 20001 is `CHANGES_REQUESTED`, which matches a required change.
- **The fix belongs to this task.** It changes only `soft_delete` in `modules/fundamental/src/sbom/service/sbom.rs`, a file listed under the task's Files to Modify. It is not a broader concern.

## Outcome

- **Sub-task created:** yes. See `subtask-30001.md`.
  - Jira call: `jira.create_issue` with **Issue Type: Sub-task** (issueTypeName `Sub-task`, not a standalone Task). Parent: TC-9103. Labels: `["ai-generated-jira", "review-feedback"]`.
  - Link: `jira.create_issue_link(type="Blocks", inwardIssue=<sub-task-id>, outwardIssue=TC-9103)`
- **Reply that would be posted to the thread** (eval mode, so not posted):

  ```
  gh api repos/trustify/trustify-backend/pulls/744/comments/30001/replies -f body="[sdlc-workflow/verify-pr] Classified as **code change request** — sub-task [<SUB-TASK-KEY>](<sub-task-webUrl>) created to address this feedback."
  ```
