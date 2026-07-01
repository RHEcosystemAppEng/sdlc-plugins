# Step 1.5 -- Description Integrity Verification for TC-9201

## Context

The Jira issue TC-9201 has one comment posted by a previous plan-feature run with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

## Step-by-Step Verification Process

### 1. Retrieve issue comments

Fetch all comments on TC-9201 using:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search through the returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:`. In this case, exactly one comment matches the marker. If multiple comments had matched, we would select the most recent one by `created` timestamp.

The matching comment body is:
```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 3. Check for comment editing (Comment Edit Detection)

Compare the comment's `created` and `updated` timestamps. In this scenario, the `created` and `updated` timestamps are identical. This means the comment has not been edited after initial posting -- no warning is needed. Proceed with the digest comparison.

If `updated` had been later than `created`, we would warn: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." We would still proceed with digest comparison regardless.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Full tagged digest**: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Format tag**: `md` (indicates the description was hashed as markdown text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The digest uses the format-tagged format (`sha256-md:<hex>`), not the legacy untagged format (`sha256:<hex>`), so we proceed with normal comparison rather than logging a legacy format warning.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response. Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the format (in this case, markdown text since we fetched via MCP) and outputs a tagged digest. Per the eval scenario, the script outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If the script had exited non-zero, we would warn and skip the integrity check without blocking execution.

### 6. Compare format tags

- **Stored tag**: `sha256-md`
- **Computed tag**: `sha256-md`

The tags match (both are `sha256-md`). Proceed to hex digest comparison.

If the tags had differed (e.g., stored was `sha256-adf` but computed was `sha256-md`), we would log a warning: "Digest format mismatch (stored: adf, current: md) -- producer and consumer used different API access methods. Skipping integrity check." and proceed normally.

### 7. Compare hex digests

- **Stored hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The digests **match**. This confirms the task description has not been modified since plan-feature created it.

## Outcome

**Digests match -- proceed silently.** No user prompt is needed, no warning is displayed, and no additional latency is added. The skill continues directly to Step 2 (Verify Dependencies).

Per the SKILL.md specification (Step 1.5, item 4e): when the hex digests match, "proceed silently -- no additional user prompt, no added latency."

## Alternative Outcomes (not applicable here, documented for completeness)

- **Digest mismatch**: If the hex digests had not matched, the skill would alert the user that the task description was modified after plan-feature created it. It would display the expected digest (from the comment) and the actual digest (computed from the current description), and ask the user whether to (1) Proceed with the current description as-is, or (2) Stop so they can re-run plan-feature to regenerate tasks. Execution would stop immediately until the user responds.

- **No digest comment found**: If no comment matching the marker string had been found, the skill would log a warning: "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced." and proceed normally without blocking.

- **Legacy digest format**: If the digest had used the untagged format `sha256:<hex>`, the skill would log: "Legacy digest format detected -- skipping integrity check" and proceed normally.
