# Step 1.5 — Verify Description Integrity (Digest Mismatch Scenario)

## Overview

After fetching and parsing TC-9201 in Step 1, Step 1.5 verifies that the task description has not been modified since plan-feature created it, following the protocol defined in `shared/description-digest-protocol.md`. In this scenario, the hex digests do not match, indicating the description was changed after planning.

## Detailed Procedure

### 1. Retrieve Issue Comments

Fetch all comments on the Jira issue:

```
jira.get_issue_comments("TC-9201")
```

This returns the list of all comments on the issue, each with `body`, `created`, and `updated` fields.

### 2. Locate the Digest Comment

Search through the returned comments for any whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

This marker is defined in `shared/description-digest-protocol.md` and is fixed across all skills and invocations.

In this scenario, one comment matches:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

If multiple comments matched the marker (e.g., from plan-feature re-runs), I would select the most recent one by `created` timestamp to ensure deterministic behavior. In this case, there is only one matching comment.

### 3. Check for Comment Editing

Compare the comment's `created` and `updated` timestamps. In this scenario, the timestamps are identical, meaning the comment has not been edited after initial posting. No warning is needed for comment tampering.

(If `updated` were later than `created`, I would warn: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." and proceed with the digest comparison regardless. If timestamps were not available in the API response, I would skip this check silently.)

### 4. Parse the Format Tag and Hex Digest from the Comment

From the comment body `[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000`, extract:

- **Format tag**: `sha256-md`
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

The format tag `sha256-md` indicates the digest was computed from the markdown representation of the description.

### 5. Compute the Current Digest of the Description

Extract the description field from the issue response (the markdown content fetched in Step 1). Write it to a temporary file and compute the digest using the project's digest script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs a format-tagged digest. For this scenario, assume the script outputs:

```
sha256-md:a3f7b2c1d4e5f6089712345abcdef67890abcdef1234567890abcdef12345678
```

(The actual computed hash would depend on the current description content. The key point is that it differs from the stored hash.)

If the script exited non-zero, I would warn and skip the integrity check without blocking execution. In this scenario, the script succeeds.

### 6. Compare Format Tags

- **Stored tag** (from comment): `sha256-md`
- **Computed tag** (from script output): `sha256-md`

The format tags match -- both are `sha256-md`. This confirms both the producer (plan-feature) and consumer (implement-task) used the same Jira access method (both received markdown), so a direct hex digest comparison is valid.

(If the tags differed -- e.g., stored was `sha256-adf` but computed was `sha256-md` -- I would log a warning about format mismatch and skip the integrity check, proceeding normally.)

### 7. Compare Hex Digests -- MISMATCH Detected

- **Expected digest** (from comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual digest** (computed from current description): `sha256-md:a3f7b2c1d4e5f6089712345abcdef67890abcdef1234567890abcdef12345678`

The format tags match (`sha256-md`), but the hex hashes are **different**. This means the task description was modified after plan-feature created the task.

### 8. Alert the User

I would display the following alert to the user:

---

**WARNING: Task description integrity check FAILED**

The description of TC-9201 has been modified since plan-feature created this task. The recorded digest does not match the current description content.

- **Expected** (from plan-feature digest comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual** (computed from current description): `sha256-md:a3f7b2c1d4e5f6089712345abcdef67890abcdef1234567890abcdef12345678`

This means someone (or an automated process) changed the task description after the planning phase. The implementation may not match the original plan.

**How would you like to proceed?**

1. **Proceed** -- implement the task using the current (modified) description as-is
2. **Stop** -- halt implementation so you can re-run plan-feature to regenerate tasks with a consistent plan

---

### 9. Stop Execution -- Await User Response

**Execution is halted at Step 1.5.** I do NOT proceed to Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), or any subsequent implementation steps. No branch is created, no code is modified, no Jira transitions occur.

The skill waits for the user to choose one of the two options before taking any further action:

- If the user chooses **option 1 (Proceed)**: continue to Step 2 with the current description, acknowledging that it differs from what plan-feature originally created.
- If the user chooses **option 2 (Stop)**: terminate the skill execution entirely. The user can then re-run plan-feature to regenerate the task with updated planning, and subsequently re-run implement-task.
