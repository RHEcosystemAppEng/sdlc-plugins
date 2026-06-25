# Step 1.5 -- Description Integrity Verification for TC-9201

## Overview

This document describes how implement-task would handle the description integrity
verification in Step 1.5 for task TC-9201, given the following scenario:

- The Jira issue has one comment with the body:
  `[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- The digest computed from the current task description using `scripts/sha256-digest.py`
  produces a DIFFERENT hex hash, but with the same format tag (`sha256-md`).
- The comment's `created` and `updated` timestamps are identical (comment was not edited).

## Step-by-Step Verification Process

### 1. Retrieve Issue Comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the Digest Comment

Search all returned comments for those whose body starts with the marker string
`[sdlc-workflow] Description digest:`. In this scenario, exactly one comment matches:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches, it is selected directly (no need for most-recent
tiebreaking by `created` timestamp).

### 3. Check for Comment Editing

Compare the comment's `created` and `updated` timestamps. In this scenario, they are
identical -- the comment has not been edited after initial posting. No warning is needed.
Proceed with digest comparison.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

This is not a legacy untagged format (`sha256:<hex>`) -- it uses the current format-tagged
scheme (`sha256-md:<hex>`), so proceed with the full verification.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (fetched in Step 1). Write
it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is in markdown format
(obtained via MCP), the script outputs a tagged digest like:

```
sha256-md:abc123...actual64charhexdigest...
```

(where the hex portion differs from the stored value).

### 6. Compare Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md` -- the tags match.
This means the producer and consumer used the same API access method (both markdown),
so a direct hex digest comparison is valid. Proceed to hex comparison.

### 7. Compare Hex Digests -- MISMATCH DETECTED

The stored hex digest:
```
0000000000000000000000000000000000000000000000000000000000000000
```

The computed hex digest (from current description):
```
<actual computed 64-char hex from current description content>
```

These do NOT match. This means the task description was modified after plan-feature
originally created it.

## Action Taken: Alert User and STOP Execution

Upon detecting the digest mismatch, the following message is displayed to the user:

> **Warning: Task description integrity check failed.**
>
> The description for TC-9201 was modified after plan-feature created it.
>
> - **Expected digest** (from plan-feature comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from current description): `sha256-md:<actual computed hex digest>`
>
> The description may have been manually edited since planning. Please choose how to proceed:
>
> 1. **Proceed** -- implement using the current (modified) description as-is
> 2. **Stop** -- abort so you can re-run plan-feature to regenerate tasks from the updated feature description
>
> Choose (1/2):

**Execution stops immediately.** No subsequent steps are taken -- Step 2 (Verify
Dependencies), Step 3 (Transition to In Progress), Step 4 (Understand the Code),
and all later steps are NOT executed until the user responds.

## Rationale

This behavior follows the description-digest-protocol.md specification and SKILL.md
Step 1.5(e):

- When format tags match and hex digests differ, it indicates the task description was
  modified after plan-feature created it.
- The user must be alerted with both the expected and actual digests so they can make an
  informed decision.
- The skill must NOT silently continue -- the user explicitly chooses whether to proceed
  with the modified description or stop to re-plan.
- This guards against silent tampering or unintentional description edits between the
  planning and implementation phases of the SDLC workflow.
