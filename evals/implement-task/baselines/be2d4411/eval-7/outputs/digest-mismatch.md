# Step 1.5 -- Description Integrity Verification for TC-9201

## 1. Retrieve Issue Comments

After fetching the task in Step 1, retrieve all comments on the Jira issue:

```
jira.get_issue_comments(TC-9201)
```

## 2. Locate the Digest Comment

Search through all returned comments for any whose body starts with the marker string defined in `shared/description-digest-protocol.md`:

```
[sdlc-workflow] Description digest:
```

In this case, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

If multiple comments matched this marker prefix, the most recent one by `created` timestamp would be selected, per the protocol's "Multiple Digest Comments" section. Here only one comment matches.

## 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the `created` and `updated` timestamps are identical, which means the comment was not edited after initial posting. No warning is needed -- proceed with digest comparison.

(If `updated` were later than `created`, a warning would be surfaced: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." The digest comparison would still proceed regardless.)

## 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`
- **Full stored digest:** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`

The format tag `sha256-md` indicates the digest was computed from the markdown representation of the description.

## 5. Compute the Current Digest

Extract the description field from the issue response (the markdown text of TC-9201's description), write it to a temp file, and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (plain text / markdown in this case) and outputs a format-tagged digest. Suppose the output is:

```
sha256-md:b7e4a9f3c1d2e8f0a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8
```

(This is an example computed digest representing the actual current description content.)

## 6. Compare Format Tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match (both `sha256-md`), so we proceed to compare the hex digests directly.

(If the tags differed -- e.g., stored was `sha256-adf` but computed was `sha256-md` -- a warning would be logged: "Digest format mismatch (stored: sha256-adf, current: sha256-md) -- producer and consumer used different API access methods. Skipping integrity check." and execution would proceed normally without blocking.)

## 7. Compare Hex Digests -- MISMATCH DETECTED

- **Expected (from comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `sha256-md:b7e4a9f3c1d2e8f0a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8`

The hex digests do NOT match. This means the task description was modified after plan-feature created it.

## 8. Alert the User

The following alert would be presented to the user:

---

**WARNING: Task description integrity check failed for TC-9201.**

The task description has been modified since plan-feature created this task. The description digest recorded at planning time does not match the current description content.

- **Expected digest (from plan-feature):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual digest (from current description):** `sha256-md:b7e4a9f3c1d2e8f0a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8`

Someone (or an automated process) modified the Jira task description after plan-feature generated it. This could mean the implementation plan is out of date with the current description, or the description was tampered with.

**Please choose how to proceed:**

1. **Proceed** -- Accept the current description as-is and continue with implementation. Use this if the changes were intentional and you are satisfied with the current description.
2. **Stop** -- Halt implementation so you can re-run plan-feature to regenerate tasks from the updated feature description. Use this if the description changes may affect the implementation plan.

Choose (1/2):

---

## 9. STOP Execution

**Execution is halted at this point.** No subsequent steps (Step 2 -- Verify Dependencies, Step 3 -- Transition to In Progress, Step 4 -- Understand the Code, or any implementation work) are performed until the user responds to the prompt above.

- If the user chooses **1 (Proceed)**: implementation continues with Step 2 using the current description content as the specification, despite the digest mismatch.
- If the user chooses **2 (Stop)**: the skill exits immediately. The user is expected to re-run plan-feature to regenerate tasks that reflect the updated feature description, then re-invoke implement-task on the newly created tasks.
