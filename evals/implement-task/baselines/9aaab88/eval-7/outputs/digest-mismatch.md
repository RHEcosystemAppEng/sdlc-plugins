# Step 1.5 -- Verify Description Integrity: Digest Mismatch Handling

## Context

Task: TC-9201 (Add advisory severity aggregation service and endpoint)

The Jira issue has one comment posted by a previous plan-feature run. The skill must verify the description has not been modified since plan-feature created the task.

## Step 1.5 Execution

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

This returns the list of comments on the issue. In this scenario, one comment is present.

### 2. Locate the digest comment

Search through the returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:`. The marker string is defined in `shared/description-digest-protocol.md` and must be matched exactly.

The matching comment body is:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Only one comment matches the marker, so it is selected directly. If multiple comments had matched, the most recent one by `created` timestamp would be selected.

### 3. Check for comment editing (defense-in-depth)

Compare the comment's `created` and `updated` timestamps. In this scenario, the timestamps are identical, meaning the comment has not been edited after initial posting. No warning is needed for this check.

If `updated` were later than `created`, the skill would warn: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." and proceed with digest comparison regardless.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Full tagged digest**: `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Format tag**: `sha256-md` (indicates the description was hashed in markdown format)
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the current tagged format (not the legacy untagged `sha256:<hex>` format), so we proceed with the full comparison.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text of the task description). Write it to a temp file and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is in markdown (plain text), the script:
1. Strips leading and trailing whitespace from the content
2. Computes SHA-256 of the normalized content
3. Outputs a tagged digest: `sha256-md:<64-char-hex>`

Check the exit code -- if non-zero, warn and skip the integrity check. In this scenario the script succeeds and returns a digest such as:

```
sha256-md:abc123...actual64charhexdigest...789def
```

(The actual hex value would be the real SHA-256 of the current description content.)

### 6. Compare format tags

- Stored tag: `sha256-md`
- Computed tag: `sha256-md`

The format tags **match** (both are `sha256-md`), confirming that both the producer (plan-feature) and consumer (implement-task) used the same description format (markdown). Proceed to hex digest comparison.

If the tags had differed (e.g., stored was `sha256-adf` but computed was `sha256-md`), the skill would log a warning ("Digest format mismatch (stored: sha256-adf, current: sha256-md) -- producer and consumer used different API access methods. Skipping integrity check.") and proceed normally without blocking.

### 7. Compare hex digests -- MISMATCH DETECTED

- **Expected** (from digest comment): `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual** (computed from current description): `abc123...actual64charhexdigest...789def`

The hex digests **do not match**. This means the task description was modified after plan-feature created it.

### 8. Alert the user and halt execution

The skill presents the following alert to the user:

---

**Warning: Task description modified after planning**

The description of TC-9201 has been modified since plan-feature created it. The description digest does not match the value recorded at planning time.

- **Expected digest** (recorded by plan-feature): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual digest** (computed from current description): `sha256-md:abc123...actual64charhexdigest...789def`

This means someone (or an automated process) changed the task description after plan-feature generated it. The implementation plan may no longer match the current description.

**Options:**

1. **Proceed** -- implement using the current (modified) description as-is
2. **Stop** -- abort so you can re-run plan-feature to regenerate tasks from the updated description

Choose (1/2):

---

### 9. Stop execution

**Execution stops immediately.** The skill does NOT proceed to Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), Step 4 (Understand the Code), or any subsequent implementation steps. No branch is created, no code is modified, no plan is drafted, and no Jira transitions occur.

The skill waits for the user to respond with their choice before taking any further action:

- If the user chooses **Proceed (1)**: the skill continues from Step 2 onward, using the current description as the implementation specification.
- If the user chooses **Stop (2)**: the skill terminates entirely. The user should re-run plan-feature to regenerate tasks that reflect the updated description, then re-invoke implement-task.

## Summary of Protocol Steps Applied

| Step | Action | Result |
|---|---|---|
| Retrieve comments | `jira.get_issue_comments("TC-9201")` | 1 comment found |
| Locate digest comment | Search for marker `[sdlc-workflow] Description digest:` | Comment found |
| Comment edit detection | Compare `created` vs `updated` timestamps | Identical -- not edited |
| Extract stored digest | Parse `sha256-md:0000...` from comment body | Tag: `sha256-md`, Hex: `0000...` |
| Compute current digest | `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt` | Tag: `sha256-md`, Hex: `abc1...` |
| Compare format tags | `sha256-md` == `sha256-md` | Tags match -- proceed to hex comparison |
| Compare hex digests | `0000...` != `abc1...` | **MISMATCH** |
| Alert user | Display expected vs actual, offer proceed/stop choice | User must choose |
| Halt execution | Do not proceed to Step 2 or beyond | **STOPPED** |
