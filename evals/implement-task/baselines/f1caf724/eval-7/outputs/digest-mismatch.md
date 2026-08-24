# Step 1.5 -- Description Integrity Verification: Digest Mismatch Handling

## Overview

This document describes how implement-task handles the description integrity verification in Step 1.5 for task TC-9201, given that a digest comment exists but does NOT match the current description content.

## Step 1 Recap (prerequisite)

After fetching the task TC-9201 via `jira.get_issue("TC-9201")`, the structured description was parsed successfully. All required sections are present (Repository, Target Branch, Description, Files to Modify, Files to Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements). The task description describes adding an advisory severity aggregation service and endpoint.

## Step 1.5 -- Verify Description Integrity

### 1. Retrieve Issue Comments

Fetch all comments on the Jira issue:

```
jira.get_issue_comments("TC-9201")
```

The API returns one comment posted by a previous plan-feature run.

### 2. Locate the Digest Comment

Search the returned comments for any whose body starts with the marker string defined in `shared/description-digest-protocol.md`:

```
[sdlc-workflow] Description digest:
```

One comment matches this marker. Its full body is:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches, it is selected as the digest comment. If multiple comments had matched, the most recent one by `created` timestamp would have been selected.

### 3. Check for Comment Editing

Compare the comment's `created` and `updated` timestamps. In this case, the `created` and `updated` timestamps are identical, meaning the comment has not been edited after initial posting. No warning is needed -- proceed with digest comparison.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the format-tagged format (not the legacy untagged `sha256:<hex>` format), so verification can proceed normally.

### 5. Compute the Current Digest

Extract the description field from the issue response. Write it to a temporary file and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs a tagged digest, e.g.:

```
sha256-md:e7f3a1b9c2d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e
```

(The exact hash above is illustrative -- the real output would be computed from the actual description content.)

### 6. Compare Format Tags

Compare the format tag from the stored digest (`sha256-md`) with the format tag from the computed digest (`sha256-md`).

**Result: Tags match.** Both are `sha256-md`, meaning both the producer (plan-feature) and consumer (implement-task) used the same Jira access method (MCP, which returns markdown). Proceed to hex digest comparison.

### 7. Compare Hex Digests

Compare the hex portion of the stored digest with the hex portion of the computed digest:

- **Expected (stored in comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `sha256-md:e7f3a1b9c2d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e` (different hash)

**Result: MISMATCH.** The format tags match (both `sha256-md`) but the hex hashes differ. This means the task description was modified after plan-feature originally created it.

### 8. Alert the User

The skill alerts the user about the integrity verification failure:

---

**Warning: Task description modified since plan-feature created it.**

The description integrity check detected that the task description for TC-9201 has been modified since plan-feature generated it. The content hash does not match the digest recorded at creation time.

- **Expected digest (from plan-feature comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual digest (computed from current description):** `sha256-md:e7f3a1b9c2d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e`

Someone (or an automated process) modified the task description after plan-feature created it. Implementing a modified description may lead to inconsistencies between the planned feature breakdown and the actual implementation.

**How would you like to proceed?**

1. **Proceed** -- Continue implementing with the current (modified) description as-is. I will use the description content as it exists now.
2. **Stop** -- Abort implementation so you can re-run plan-feature to regenerate the task description and ensure the plan is consistent.

Please choose (1 or 2):

---

### 9. Stop Execution

**Execution is stopped immediately.** The skill does not proceed to Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), Step 4 (Understand the Code), or any subsequent implementation steps. No branch is created, no code is inspected, and no changes are made.

This follows the same pause-and-ask pattern used when the structured description is incomplete (Step 1) -- the skill halts and waits for explicit user input before taking any further action. The user must respond with their choice before the skill continues.

- If the user chooses **option 1 (Proceed)**: the skill logs the user's decision and continues to Step 2 and beyond, treating the current description as the specification.
- If the user chooses **option 2 (Stop)**: the skill terminates execution. The user can re-run plan-feature to regenerate the task with an updated plan, which will post a new digest comment reflecting the new description content.
