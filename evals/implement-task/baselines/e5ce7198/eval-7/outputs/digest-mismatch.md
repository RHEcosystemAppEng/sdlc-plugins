# Step 1.5 -- Verify Description Integrity for TC-9201

## Overview

Step 1.5 verifies that the task description has not been modified since plan-feature
created it, using the description digest protocol defined in
`shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201 using `jira.get_issue_comments(<jira-issue-id>)`.

### 2. Locate the digest comment

Search all comments for bodies starting with the marker string:

```
[sdlc-workflow] Description digest:
```

One comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected as the digest comment.

### 3. Check for comment editing

Compare the comment's `created` and `updated` timestamps. In this case, the
timestamps are identical, which means the comment has not been edited after initial
posting. No warning is needed -- proceed to digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

The format tag is `sha256-md`, not the legacy untagged format `sha256:<hex>`, so
this is not a legacy digest. Proceed with comparison.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response. Write it to a
temporary file `/tmp/desc-TC-9201.txt` and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the description format. Since the description is markdown
text (not ADF JSON), the script outputs a tagged digest:

```
sha256-md:<computed-64-char-hex>
```

where `<computed-64-char-hex>` is the actual SHA-256 hash of the current description
content (after stripping leading/trailing whitespace).

### 6. Compare format tags

Both the stored digest and the computed digest use the `sha256-md` format tag. The
tags match, so we proceed to compare the hex digests directly.

### 7. Compare hex digests -- MISMATCH DETECTED

The stored hex digest is:
```
0000000000000000000000000000000000000000000000000000000000000000
```

The computed hex digest is a different value (the actual SHA-256 of the current
description content).

**The hex digests do not match.** This means the task description for TC-9201 was
modified after plan-feature originally created it.

## Action Taken: PAUSE EXECUTION

Per the skill specification (Step 1.5, item 4e), when format tags match but hex
digests differ, execution must stop immediately. The skill does NOT proceed to
Step 2 (Verify Dependencies) or any subsequent step.

The following alert is presented to the user:

---

**WARNING: Task description integrity check failed for TC-9201.**

The description of this task was modified after plan-feature created it.

- **Expected digest** (from plan-feature comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual digest** (computed from current description): `sha256-md:<computed-64-char-hex>`

The description content has changed since the planning phase. This may mean the
implementation plan, files to modify, acceptance criteria, or other task details
were altered outside the normal workflow.

**Please choose how to proceed:**

1. **Proceed** -- continue implementing with the current (modified) description as-is
2. **Stop** -- abort implementation so you can re-run plan-feature to regenerate tasks from the updated feature description

Awaiting your response before continuing.

---

## Why execution is paused

The digest mismatch indicates that someone (or some process) modified the Jira task
description after plan-feature wrote it. This is significant because:

- The implementation plan, file lists, API changes, and acceptance criteria in the
  description may no longer match what plan-feature intended.
- Proceeding with a silently modified description could lead to implementing
  something different from what was planned and reviewed.
- The user needs to make an informed decision about whether the modifications are
  intentional and acceptable, or whether re-planning is needed.

The skill will not take any further action -- no branch creation, no file
modifications, no status transitions -- until the user explicitly chooses option 1
(proceed) or option 2 (stop).
