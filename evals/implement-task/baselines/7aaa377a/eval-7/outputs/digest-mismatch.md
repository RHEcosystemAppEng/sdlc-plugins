# Step 1.5 -- Description Integrity Verification for TC-9201

## Scenario

The Jira issue TC-9201 has one comment with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

The comment's `created` and `updated` timestamps are identical. The format tags match between stored and computed digests (both `sha256-md`), but the hex hashes differ -- meaning the description was modified after plan-feature created the task.

## Step-by-Step Handling

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search through all returned comments for those whose body starts with the marker string `[sdlc-workflow] Description digest:`. One comment matches:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, select it. (If multiple matched, the most recent by `created` timestamp would be selected.)

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this scenario, they are identical -- the comment has not been edited after initial posting. No warning is needed. Proceed to digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

This is not the legacy untagged format (`sha256:<hex>`) -- it uses the current format-tagged convention (`sha256-md:<hex>`). No legacy warning needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text describing the advisory severity aggregation service and endpoint). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

Since the description is plain markdown text (not ADF JSON), the script auto-detects the format and outputs a tagged digest in the form:

```
sha256-md:<computed-64-char-hex>
```

The script exits zero, so the digest is valid.

### 6. Compare format tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The tags match. Both the producer (plan-feature) and consumer (implement-task) used the same API access method (both received markdown). Proceed to hex digest comparison.

### 7. Compare hex digests

- **Expected (from comment):** `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `<different-64-char-hex-value>`

**Result: MISMATCH.** The hex digests differ, meaning the task description was modified after plan-feature created it.

### 8. Alert the user and stop execution

Per the protocol, alert the user with the following message:

> **Warning: Task description integrity check failed.**
>
> The description for TC-9201 was modified after plan-feature created it.
>
> - **Expected digest (from plan-feature comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest (computed from current description):** `sha256-md:<computed-hash>`
>
> Please choose how to proceed:
> 1. **Proceed** -- implement using the current (modified) description as-is
> 2. **Stop** -- abort so you can re-run plan-feature to regenerate tasks with a fresh digest
>
> Choose (1/2):

**Execution stops immediately.** No subsequent steps (Step 2 through Step 11) are executed until the user responds. This means:

- No dependency verification (Step 2)
- No Jira transition to In Progress (Step 3)
- No code inspection (Step 4)
- No branch creation (Step 5)
- No implementation (Step 6)
- No tests (Step 7)
- No acceptance criteria verification (Step 8)
- No self-verification (Step 9)
- No commit/push/PR (Step 10)
- No Jira update (Step 11)

### 9. Handling the user's response

- **If the user chooses "Proceed" (option 1):** Resume execution at Step 2 (Verify Dependencies), using the current description as the specification. The mismatch warning has been acknowledged; no further digest checks are needed.

- **If the user chooses "Stop" (option 2):** Halt all execution. The user should re-run plan-feature on the parent feature to regenerate the task descriptions, which will post a new digest comment matching the updated description. After re-running plan-feature, the user can re-invoke implement-task on the updated task.

## Key Protocol Details Applied

1. **Format tag comparison before hex comparison:** The protocol requires comparing format tags first. If they differed (e.g., stored `sha256-adf` vs. computed `sha256-md`), the check would be skipped with a warning rather than reporting a false mismatch. In this scenario the tags match, so hex comparison proceeds.

2. **Comment edit detection:** The protocol checks whether the digest comment itself was tampered with by comparing `created` and `updated` timestamps. In this scenario the timestamps are identical, confirming the comment was not edited. If the comment had been edited, an additional warning ("Digest comment was edited after initial posting -- integrity cannot be fully guaranteed") would be surfaced alongside the mismatch result.

3. **Hard stop on mismatch:** The protocol mandates stopping execution immediately on a hex digest mismatch when tags match. This is not a soft warning -- implementation must not proceed without explicit user approval.

4. **Non-blocking for missing digests:** If no digest comment had been found at all, the protocol would log a warning and proceed. But since a digest comment IS present and its hex does not match, the stricter mismatch path applies.

5. **Legacy format bypass:** If the stored digest used the legacy untagged format `sha256:<hex>`, the protocol would skip the integrity check with a warning. But in this scenario the stored digest uses the current format-tagged convention, so full verification is performed.
