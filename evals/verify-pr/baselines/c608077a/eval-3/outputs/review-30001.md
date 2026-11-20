# Review Comment 30001 — Classification

- **Author:** reviewer-a
- **Review:** 20001 (CHANGES_REQUESTED)
- **Location:** `modules/fundamental/src/sbom/service/sbom.rs`, line 60 (RIGHT)
- **Thread:** top-level comment with no replies. No earlier `[sdlc-workflow/verify-pr] Classified as` reply exists, so the comment is **unclassified** and goes to classification.

## Comment

> The `soft_delete` method should run all three UPDATE statements inside a single database transaction. If the sbom_advisory update fails after sbom_package succeeds, you'll have inconsistent state. Wrap the three operations in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db` for each exec call.

## Classification: **Code change request**

## Reasoning

- **The reviewer asks for a specific change.** The wording is direct: "should run … inside a single database transaction", "Wrap the three operations in …", "use `txn` instead of `self.db`". The reviewer also names the exact fix.
- **The diff confirms the defect.** In `SbomService::soft_delete`, three `update_many()` calls each run `.exec(&self.db)` separately, on the `sbom`, `sbom_package` and `sbom_advisory` tables. If the second or third call fails, the earlier updates are already committed. The SBOM would then be soft-deleted while its join rows are not, or only partly.
- **This is a correctness issue, not a preference.** It affects the acceptance criterion "Related `sbom_package` and `sbom_advisory` rows are cascade-updated". A partial failure leaves that criterion violated in the database.
- The review state is CHANGES_REQUESTED, and the summary says "a few things to address before we can merge". That supports treating this as required work.

## Outcome

- **Sub-task created:** yes, see `subtask-1.md` ("Wrap SBOM soft-delete cascade in a single database transaction").
- **Labels:** `ai-generated-jira`, `review-feedback`. **Link:** Blocks TC-9103.
- **Planned reply (not posted; offline eval):**
  `[sdlc-workflow/verify-pr] Classified as **code change request** — sub-task [<SUB-TASK-KEY>](<sub-task-webUrl>) created to address this feedback.`
