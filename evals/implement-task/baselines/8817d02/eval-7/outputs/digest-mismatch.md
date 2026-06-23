# Step 1.5 -- Verify Description Integrity: Digest Mismatch Handling

## Context

Task: TC-9201 (Add advisory severity aggregation service and endpoint)

The Jira issue has one comment posted by a previous plan-feature run. The stored digest comment uses the `sha256-md` format tag but contains a zeroed-out hex hash that does not match the digest computed from the current task description.

## Procedure

### 1. Locate the Digest Comment

After fetching the task in Step 1, retrieve all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

Search through the returned comments for any whose body starts with the marker string defined in `shared/description-digest-protocol.md`:

```
[sdlc-workflow] Description digest:
```

One comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

If multiple comments matched the marker, the protocol requires selecting the most recent one by `created` timestamp. In this case only one comment matches, so it is selected directly.

### 2. Check for Comment Editing

The protocol requires comparing the comment's `created` and `updated` timestamps to detect post-hoc editing. In this scenario, the `created` and `updated` timestamps are identical, meaning the comment has not been edited since it was posted. No edit-related warning is needed. Proceed to digest comparison.

### 3. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the modern format-tagged format (not the legacy untagged `sha256:<hex>` format), so the integrity check proceeds normally.

### 4. Compute the Current Digest

Extract the description field from the TC-9201 issue response (the markdown text of the Description section). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as markdown text and outputs a tagged digest, for example:

```
sha256-md:7f3a1b9c4e2d5f8a6b0c9d1e3f5a7b2c4d6e8f0a1b3c5d7e9f0a2b4c6d8e0f1a
```

(The exact hex value would be computed from the actual current description content.)

### 5. Compare Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md` -- the tags match. This means the producer and consumer used the same API access method (both markdown), so a direct hex digest comparison is valid. Proceed to hex comparison.

### 6. Compare Hex Digests -- MISMATCH DETECTED

- **Expected digest** (from comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual digest** (computed from current description): `sha256-md:7f3a1b9c4e2d5f8a6b0c9d1e3f5a7b2c4d6e8f0a1b3c5d7e9f0a2b4c6d8e0f1a`

The hex digests do NOT match. This means the task description was modified after plan-feature created the task.

### 7. Alert the User and Stop

Per Step 1.5(e) of the implement-task SKILL.md, when a digest mismatch is detected, the skill must alert the user and stop execution immediately. The following message is presented:

> **Warning: Task description integrity check failed.**
>
> The description for TC-9201 was modified after plan-feature created it.
>
> - **Expected digest** (recorded by plan-feature): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from current description): `sha256-md:7f3a1b9c4e2d5f8a6b0c9d1e3f5a7b2c4d6e8f0a1b3c5d7e9f0a2b4c6d8e0f1a`
>
> The task description has changed since planning. This could mean someone edited the requirements after the plan was generated.
>
> How would you like to proceed?
>
> 1. **Proceed** -- implement the task using the current (modified) description as-is
> 2. **Stop** -- halt implementation so you can re-run plan-feature to regenerate tasks with an updated plan
>
> Please choose (1 or 2):

### 8. Execution Halted

**Execution stops here.** The skill does NOT proceed to Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), Step 4 (Understand the Code), or any subsequent implementation step. No branch is created, no code is modified, no Jira transitions are made.

The skill waits for the user's explicit response before taking any further action:

- If the user chooses **option 1 (Proceed)**: the skill continues from Step 2 onward using the current description content, accepting that it differs from what plan-feature originally generated.
- If the user chooses **option 2 (Stop)**: the skill terminates entirely. The user can re-run plan-feature to regenerate tasks based on the updated description, then re-invoke implement-task on the newly created task.

## Summary

The digest mismatch flow follows the description-digest-protocol and Step 1.5 of the implement-task SKILL.md exactly:

1. Located the digest comment by searching for the `[sdlc-workflow] Description digest:` marker string
2. Verified the comment was not edited (created == updated timestamps)
3. Extracted the stored tagged digest (`sha256-md:0000...0000`)
4. Computed the current digest from the live task description using `scripts/sha256-digest.py`
5. Confirmed format tags match (both `sha256-md`), enabling direct hex comparison
6. Detected hex digest mismatch -- the description was modified after plan-feature created the task
7. Alerted the user with expected vs. actual digest values
8. Offered the user two choices: proceed with the current description, or stop to re-run plan-feature
9. **Stopped execution immediately** -- no further steps are taken until the user responds
