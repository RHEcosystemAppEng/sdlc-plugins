# Step 1.5 -- Description Integrity Verification for TC-9201

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201 using:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search all returned comments for those whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

This marker is defined in `shared/description-digest-protocol.md`. If multiple comments match (e.g., from plan-feature re-runs), select the most recent one by `created` timestamp.

In this case, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

### 3. Check for comment editing

Compare the comment's `created` and `updated` timestamps. In this scenario, the timestamps are identical, so the comment has not been edited after initial posting. No warning is needed -- proceed with digest comparison.

### 4. Extract the stored digest

Parse the tagged digest from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the format-tagged format (not legacy untagged `sha256:<hex>`), so normal comparison proceeds.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response, write it to a temporary file, and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs a tagged digest. Suppose the script outputs:

```
sha256-md:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890
```

### 6. Compare format tags

Both the stored digest and the computed digest use the same format tag: `sha256-md`. Since the tags match, proceed to compare the hex digests directly.

### 7. Compare hex digests -- MISMATCH DETECTED

| | Value |
|---|---|
| **Expected (from digest comment)** | `sha256-md:0000000000000000000000000000000000000000000000000000000000000000` |
| **Actual (computed from current description)** | `sha256-md:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890` |

The hex digests do not match. This means the task description for TC-9201 was modified after plan-feature originally created it.

## Alert to User

> **Warning: Task description integrity check failed.**
>
> The description for TC-9201 has been modified since plan-feature created this task. The stored digest (recorded by plan-feature at task creation time) does not match the digest computed from the current description.
>
> **Expected digest (stored by plan-feature):**
> `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
>
> **Actual digest (computed from current description):**
> `sha256-md:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890`
>
> The description may have been manually edited, updated by another process, or modified by a Jira workflow after plan-feature generated it.
>
> **Please choose how to proceed:**
>
> 1. **Proceed** -- continue implementing with the current (modified) description as-is
> 2. **Stop** -- abort implementation so you can re-run plan-feature to regenerate tasks from the updated feature specification
>
> Choose (1/2):

## Execution State

**STOPPED.** Execution is halted at Step 1.5. No subsequent steps (Step 2 -- Verify Dependencies, Step 3 -- Transition to In Progress, Step 4 -- Understand the Code, Step 5 -- Create Branch, Step 6 -- Implement Changes, etc.) will proceed until the user responds with their choice.

- If the user chooses **1 (Proceed)**: implementation continues with the current description, accepting that it differs from what plan-feature originally generated.
- If the user chooses **2 (Stop)**: execution terminates entirely. The user should re-run plan-feature to regenerate task descriptions that reflect the updated feature specification, then re-invoke implement-task.

No branch has been created, no code has been modified, no Jira transitions have been made.
