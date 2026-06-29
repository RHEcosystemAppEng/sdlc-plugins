# Description Integrity Verification -- Step 1.5

## Context

Task TC-9201 has one comment posted by a previous plan-feature run with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The comment's `created` and `updated` timestamps are identical.

## Step-by-Step Verification Process

### 1. Retrieve Issue Comments

Fetch all comments on TC-9201 using `jira.get_issue_comments("TC-9201")`. This returns an array of comment objects, each with a body, `created` timestamp, and `updated` timestamp.

### 2. Locate the Digest Comment

Search through all returned comments for those whose body starts with the marker string `[sdlc-workflow] Description digest:`. In this case, exactly one comment matches. If multiple comments had matched, I would select the most recent one by `created` timestamp to handle plan-feature re-runs deterministically.

The matching comment body is:
```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this case, the timestamps are identical, meaning the comment has not been edited after initial posting. No warning is needed -- proceed with digest comparison.

If `updated` had been later than `created`, I would warn: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." I would still proceed with the digest comparison but surface the warning to the user.

If the timestamps were not available in the API response, I would skip this check silently.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body after the marker prefix:

- **Full tagged digest**: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Format tag**: `md` (meaning the description was hashed as markdown text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The digest uses the current format-tagged scheme (not the legacy untagged `sha256:<hex>` format), so no legacy warning is needed.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response. Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case, since the description was fetched via MCP which returns markdown) and outputs a tagged digest. If the script exits non-zero, I would warn and skip the integrity check without blocking execution.

Per the eval instructions, the computed digest matches the stored one -- the script would output:
```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 6. Compare Format Tags

The stored format tag is `md`. The computed format tag is also `md`. The tags match, so I proceed to hex digest comparison.

If the tags had differed (e.g., stored was `sha256-adf` but computed was `sha256-md`), I would log a warning: "Digest format mismatch (stored: `adf`, current: `md`) -- producer and consumer used different API access methods. Skipping integrity check." and proceed normally without blocking.

### 7. Compare Hex Digests

The stored hex digest is `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.
The computed hex digest is `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.

**Result: MATCH.** The digests are identical, confirming that the task description has not been modified since plan-feature created it.

### 8. Outcome

Proceed silently to Step 2. No user prompt is needed, no warning is displayed, and no additional latency is introduced. The description integrity is verified.

## What Would Happen on Mismatch

If the hex digests had not matched, I would:

1. Alert the user that the task description was modified after plan-feature created it.
2. Display the expected digest (from the comment) and the actual digest (computed from the current description).
3. Ask the user whether to:
   - **Proceed** with the current description as-is
   - **Stop** so they can re-run plan-feature to regenerate tasks
4. Stop execution immediately and wait for the user's response before proceeding with any subsequent steps.
