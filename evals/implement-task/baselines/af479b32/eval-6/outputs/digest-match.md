# Step 1.5 -- Description Integrity Verification for TC-9201

## Scenario

The Jira issue TC-9201 has one comment posted by a previous plan-feature run:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The comment's `created` and `updated` timestamps are identical. The computed digest from the current task description matches the stored digest (same format tag `sha256-md` and same hex hash).

## Verification Procedure

### 1. Retrieve Issue Comments

Fetch all comments on TC-9201 using:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the Digest Comment

Search all returned comments for bodies starting with the marker string `[sdlc-workflow] Description digest:`. In this case, exactly one comment matches. If multiple had matched, the most recent one by `created` timestamp would be selected.

### 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the timestamps are identical, meaning the comment has not been edited after initial posting. No warning is emitted. Proceed to digest comparison.

If `updated` had been later than `created`, the following warning would be surfaced to the user: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." The digest comparison would still proceed regardless.

### 4. Extract the Stored Digest

Parse the comment body to extract:
- **Format tag**: `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The digest uses the current format-tagged syntax (not the legacy untagged `sha256:<hex>` format), so no legacy warning is needed.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response, write it to a temporary file, and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs a tagged digest: `sha256-md:<64-char-hex>`.

### 6. Compare Format Tags

The stored tag is `sha256-md` and the computed tag is also `sha256-md`. The tags match, so the hex digests can be compared directly.

If the tags had differed (e.g., stored `sha256-adf` vs. computed `sha256-md`), a warning would be logged: "Digest format mismatch (stored: sha256-adf, current: sha256-md) -- producer and consumer used different API access methods. Skipping integrity check." Execution would proceed normally without blocking.

### 7. Compare Hex Digests

The stored hex digest matches the computed hex digest. This confirms the task description has not been modified since plan-feature created it.

**Result: Proceed silently.** No user prompt is needed, no warning is emitted, and no additional latency is introduced. Implementation continues to Step 2.

### Alternative Outcome: Digest Mismatch

If the hex digests had not matched, the following would occur:
- Alert the user that the task description was modified after plan-feature created it.
- Display the expected digest (from the comment) and the actual digest (computed from the current description).
- Ask the user whether to:
  1. **Proceed** with the current description as-is.
  2. **Stop** so they can re-run plan-feature to regenerate tasks.
- Execution would halt immediately until the user responds.
