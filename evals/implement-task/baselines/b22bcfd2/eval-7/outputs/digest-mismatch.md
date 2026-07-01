# Step 1.5 -- Description Integrity Verification for TC-9201

## Procedure

After fetching the task TC-9201 in Step 1, I would proceed to verify description integrity as follows:

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search through all returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:`. This marker is defined in the shared description digest protocol (`shared/description-digest-protocol.md`).

In this case, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches, it is selected directly. If multiple comments had matched the marker, I would select the most recent one by `created` timestamp to handle plan-feature re-run scenarios deterministically.

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this case, the two timestamps are identical, meaning the comment has not been edited after initial posting. No warning is needed -- proceed with digest comparison.

(If `updated` were later than `created`, I would warn: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." and still proceed with the comparison.)

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the format-tagged scheme (not the legacy untagged `sha256:<hex>` format), so full verification can proceed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text describing the advisory severity aggregation service and endpoint). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as markdown text and outputs a tagged digest, for example:

```
sha256-md:b7e4a3f1c9d2e8b5a6f0c3d7e1b4a8f2c5d9e3b6a0f4c8d2e6b1a5f9c3d7e0a4
```

### 6. Compare format tags

The stored tag is `sha256-md` and the computed tag is `sha256-md` -- the tags match. Both the producer (plan-feature) and consumer (implement-task) used the same Jira access method (MCP, which returns markdown). Proceed to hex digest comparison.

### 7. Compare hex digests -- MISMATCH DETECTED

The hex digests do not match:

| | Value |
|---|---|
| **Expected** (from digest comment) | `sha256-md:0000000000000000000000000000000000000000000000000000000000000000` |
| **Actual** (computed from current description) | `sha256-md:b7e4a3f1c9d2e8b5a6f0c3d7e1b4a8f2c5d9e3b6a0f4c8d2e6b1a5f9c3d7e0a4` |

## Alert to User

I would present the following alert to the user:

---

**WARNING: Task description integrity check FAILED**

The description of TC-9201 was modified after plan-feature created this task. The stored digest (recorded by plan-feature at task creation time) does not match the digest computed from the current description.

**Expected digest (from plan-feature comment):**
`sha256-md:0000000000000000000000000000000000000000000000000000000000000000`

**Actual digest (computed from current description):**
`sha256-md:b7e4a3f1c9d2e8b5a6f0c3d7e1b4a8f2c5d9e3b6a0f4c8d2e6b1a5f9c3d7e0a4`

This means someone (or an automated process) edited the task description in Jira after plan-feature generated it. The implementation may no longer match what was originally planned.

**How would you like to proceed?**

1. **Proceed** -- implement using the current (modified) description as-is
2. **Stop** -- halt implementation so you can re-run plan-feature to regenerate tasks from the updated feature description

Please choose (1 or 2):

---

## Execution Halted

**Execution stops here.** I would NOT proceed to Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), or any subsequent implementation steps until the user responds with their choice.

- If the user chooses **1 (Proceed)**: continue to Step 2 using the current description content, acknowledging the integrity mismatch.
- If the user chooses **2 (Stop)**: terminate the implement-task skill entirely. The user would re-run plan-feature to regenerate task descriptions, which would post a new digest comment reflecting the updated content, and then re-invoke implement-task.
