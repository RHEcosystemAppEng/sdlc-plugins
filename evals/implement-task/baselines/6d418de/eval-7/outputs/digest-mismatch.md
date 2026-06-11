# Step 1.5 -- Verify Description Integrity: TC-9201

## Overview

This document describes how the implement-task skill handles description integrity verification for task TC-9201, following the protocol defined in `shared/description-digest-protocol.md` and the procedure in Step 1.5 of `SKILL.md`.

## Procedure

### 1. Retrieve Issue Comments

After fetching the task description in Step 1, retrieve all comments on the Jira issue:

```
jira.get_issue_comments(<jira-issue-id-for-TC-9201>)
```

### 2. Locate the Digest Comment

Search all returned comments for those whose body starts with the exact marker string:

```
[sdlc-workflow] Description digest:
```

In this scenario, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected directly. (If multiple matched, the one with the latest `created` timestamp would be selected.)

### 3. Check for Comment Editing

Compare the comment's `created` and `updated` timestamps. In this scenario, the two timestamps are identical, meaning the comment was not edited after initial posting. No warning is emitted. Proceed to digest comparison.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest is not in legacy untagged format (`sha256:<hex>`), so no legacy-format warning applies.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (the markdown text fetched via MCP). Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as markdown text and outputs a tagged digest:

```
sha256-md:<actual-64-char-hex-digest-from-current-description>
```

### 6. Compare Format Tags

The stored tag is `sha256-md`. The computed tag is also `sha256-md`. The tags match, so we proceed to hex digest comparison. (If tags differed, e.g., `sha256-adf` vs `sha256-md`, we would log a warning about different API access methods and skip the integrity check.)

### 7. Compare Hex Digests -- MISMATCH DETECTED

The stored hex digest is:

```
0000000000000000000000000000000000000000000000000000000000000000
```

The computed hex digest from the current description is a different value (the actual SHA-256 of the current description content).

**The digests do not match.** This means the task description was modified after plan-feature originally created it.

## User Alert

The following alert is presented to the user:

---

**WARNING: Description integrity check failed for TC-9201.**

The task description has been modified since plan-feature created this task. The description digest recorded at planning time does not match the digest computed from the current description.

- **Expected digest (from plan-feature comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual digest (computed from current description):** `sha256-md:<computed-hex-digest>`

The description may have been edited manually in Jira, or another process may have modified it after the planning phase.

**Please choose how to proceed:**

1. **Proceed** -- accept the current description as-is and continue with implementation. The implementation will be based on the modified description, which may differ from what was originally planned.

2. **Stop** -- halt implementation so you can re-run plan-feature to regenerate tasks based on the current feature description. This ensures the implementation plan reflects the latest requirements.

---

## Execution State: STOPPED

Execution is halted at Step 1.5. No subsequent steps (Step 2 -- Verify Dependencies, Step 3 -- Transition to In Progress, or any implementation work) will proceed until the user responds with their choice.

- If the user chooses **option 1 (Proceed)**: continue to Step 2 (Verify Dependencies) using the current description as the basis for implementation.
- If the user chooses **option 2 (Stop)**: terminate the implement-task run entirely. The user should re-run plan-feature on the parent feature to regenerate task descriptions, then re-invoke implement-task on the updated task.
