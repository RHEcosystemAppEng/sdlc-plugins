# Step 1.5 — Verify Description Integrity (Mismatch Scenario)

## Context

Task TC-9201 has been fetched and parsed in Step 1. The task description contains a structured plan for adding an advisory severity aggregation service and endpoint to the trustify-backend repository. Step 1.5 now verifies that this description has not been modified since plan-feature originally created the task.

## 1. Retrieve Issue Comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

This returns the list of comments on the issue. Among them is one comment with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

## 2. Locate the Digest Comment

Search through all returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:` (as defined in `shared/description-digest-protocol.md`). One comment matches.

If multiple comments matched (e.g., from plan-feature re-runs), the most recent one by `created` timestamp would be selected. In this case there is only one match, so it is used directly.

## 3. Check for Comment Editing

Compare the comment's `created` and `updated` timestamps. In this scenario, the timestamps are identical, meaning the comment has not been edited after initial posting. No warning is needed — proceed to digest comparison.

(If `updated` were later than `created`, a warning would be surfaced: "Digest comment was edited after initial posting — integrity cannot be fully guaranteed." The digest comparison would still proceed regardless.)

## 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- Full value: `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- Format tag: `sha256-md`
- Hex digest: `0000000000000000000000000000000000000000000000000000000000000000`

The tag is `sha256-md` (not the legacy untagged `sha256:` format), so the integrity check proceeds normally.

## 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (the markdown text of the task description). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as plain text (markdown) and outputs a tagged digest, for example:

```
sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

(This is an illustrative value — the actual hash would be computed from the current description content.)

The script exits with status 0, so the integrity check continues.

## 6. Compare Format Tags

- Stored tag: `sha256-md`
- Computed tag: `sha256-md`

The format tags match. Both the producer (plan-feature) and consumer (implement-task) used the same Jira access method (both received markdown). Proceed to hex digest comparison.

(If the tags differed — e.g., stored was `sha256-adf` but computed was `sha256-md` — a warning would be logged: "Digest format mismatch (stored: sha256-adf, current: sha256-md) — producer and consumer used different API access methods. Skipping integrity check." and execution would proceed normally without blocking.)

## 7. Compare Hex Digests — MISMATCH DETECTED

- **Expected** (from digest comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual** (computed from current description): `sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

The hex digests do not match. This means the task description was modified after plan-feature created the task.

## 8. Alert the User

The following alert is presented to the user:

> **Description integrity check: MISMATCH**
>
> The task description for TC-9201 was modified after plan-feature created it.
>
> - **Expected digest** (recorded by plan-feature): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from current description): `sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
>
> The description may have been edited manually in Jira after the planning phase. The implementation may not match the original plan.
>
> How would you like to proceed?
>
> 1. **Proceed** — implement using the current (modified) description as-is
> 2. **Stop** — halt so you can re-run plan-feature to regenerate tasks from the updated feature description
>
> Choose (1/2):

## 9. STOP — Await User Response

**Execution stops here.** The skill does NOT proceed to Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), or any subsequent implementation steps. No branch is created, no code is read or modified, no Jira transitions occur.

The skill waits for the user to respond with their choice:

- If the user chooses **1 (Proceed)**: execution continues to Step 2 with the current description, acknowledging that it differs from what plan-feature originally authored.
- If the user chooses **2 (Stop)**: execution terminates. The user is expected to re-run plan-feature to regenerate task descriptions that reflect the updated feature requirements, then re-invoke implement-task.

No further action is taken until the user explicitly responds.
