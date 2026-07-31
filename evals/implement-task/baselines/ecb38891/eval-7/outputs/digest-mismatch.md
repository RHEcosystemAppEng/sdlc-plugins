# Step 1.5 — Description Integrity Verification for TC-9201

## Overview

This document describes how the implement-task skill handles the description integrity verification in Step 1.5 for task TC-9201, where a digest mismatch is detected between the stored digest and the current description.

## Step 1.5 Procedure

### 1. Retrieve Issue Comments

Fetch all comments on the Jira issue TC-9201:

```
jira.get_issue_comments(TC-9201)
```

### 2. Locate the Digest Comment

Search all returned comments for those whose body starts with the marker string defined in `shared/description-digest-protocol.md`:

```
[sdlc-workflow] Description digest:
```

One matching comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected as the digest comment. If multiple comments had matched, the most recent one by `created` timestamp would be selected.

### 3. Comment Edit Detection

The comment's `created` and `updated` timestamps are compared. In this case, they are identical, meaning the comment has not been edited after initial posting. No edit warning is raised. Proceed with digest comparison.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

The format is not the legacy untagged format (`sha256:<hex>`), so we proceed with full verification rather than skipping with a legacy warning.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response, write it to a temp file, and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs a tagged digest. The computed result is:

```
sha256-md:<actual-64-char-hex-digest>
```

(The exact hex value depends on the current description content.)

### 6. Compare Format Tags

The stored format tag is `sha256-md`. The computed format tag is also `sha256-md`. The tags match, so we proceed to compare the hex digests directly. (If the tags had differed, we would log a format mismatch warning and skip the integrity check.)

### 7. Compare Hex Digests — MISMATCH DETECTED

The stored hex digest (`0000000000000000000000000000000000000000000000000000000000000000`) does NOT match the computed hex digest of the current description. The format tags match (both `sha256-md`) but the hex hashes differ. This means the task description was modified after plan-feature created it.

## Alert to User

**WARNING: Description integrity check failed — digest mismatch detected.**

The task description for TC-9201 has been modified since plan-feature originally created it. This means someone (or something) changed the description after the planning phase completed.

**Expected digest** (from plan-feature comment):
```
sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

**Actual digest** (computed from current description):
```
sha256-md:<computed-digest-of-current-description>
```

The format tags match (`sha256-md`), confirming both the producer and consumer used the same API access method. The difference is in the content itself — the description text was altered.

## Execution Paused — User Decision Required

Implementation has been stopped. The description modification could indicate:
- Legitimate edits by a team member to clarify or update requirements
- Unintentional changes made during Jira editing
- Potential tampering that could cause the implementation to deviate from the original plan

**Please choose how to proceed:**

1. **Proceed** — Continue implementing with the current (modified) description as-is. The implementation will use the description as it exists now, regardless of what plan-feature originally created.

2. **Stop** — Halt implementation so you can re-run plan-feature to regenerate tasks based on the current feature requirements. This ensures the implementation plan and task descriptions are consistent.

**Awaiting your response before continuing. No subsequent steps (Step 2 or beyond) will be executed until you confirm.**
