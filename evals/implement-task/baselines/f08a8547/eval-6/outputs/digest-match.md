# Description Integrity Verification -- Step 1.5

## Scenario

Task: TC-9201
Digest comment found: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
Comment created/updated timestamps: identical
Assumed outcome: digest MATCHES

## Verification Procedure

### 1. Retrieve Issue Comments

Fetch all comments on TC-9201 using:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the Digest Comment

Search all returned comments for bodies starting with the marker string `[sdlc-workflow] Description digest:`. In this scenario, exactly one comment matches:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If multiple comments matched the marker, we would select the most recent one by `created` timestamp to handle plan-feature re-run scenarios deterministically.

### 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the timestamps are identical, meaning the comment has not been edited after initial posting. This is the clean case -- no warning is needed.

If `updated` had been later than `created`, we would emit the warning: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." We would still proceed with the digest comparison, but the warning would be surfaced to the user alongside the match/mismatch result.

If the API response did not include `created`/`updated` fields (e.g., MCP tool omits them), we would skip this check silently.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- Format tag: `sha256-md`
- Hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag is `sha256-md`, not the legacy untagged format `sha256:<hex>`, so we proceed with the full comparison. (If it were the legacy untagged format, we would log "Legacy digest format detected -- skipping integrity check" and proceed without comparing.)

### 5. Compute the Current Digest

Extract the description field from the issue API response. Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown in this case since MCP returns markdown) and outputs a format-tagged digest. We check that the script exits with a zero status code before using the output.

Expected output (since we assume a match):
```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If the script had exited non-zero, we would warn and skip the integrity check without blocking execution.

### 6. Compare Format Tags

Stored tag: `sha256-md`
Computed tag: `sha256-md`

The tags match, so we proceed to hex digest comparison. If the tags had differed (e.g., stored `sha256-adf` vs computed `sha256-md`), this would indicate the producer and consumer used different Jira API access methods. We would log: "Digest format mismatch (stored: sha256-adf, current: sha256-md) -- producer and consumer used different API access methods. Skipping integrity check." and proceed normally without blocking.

### 7. Compare Hex Digests

Stored hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
Computed hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

Result: MATCH

### 8. Outcome

The digests match. The task description has not been modified since plan-feature created it. Proceed silently to Step 2 -- no additional user prompt, no added latency, no warning messages.

## Summary of Decision Tree

| Condition | Action |
|---|---|
| No digest comment found | Log warning, proceed (backward compatibility) |
| Legacy untagged format (`sha256:<hex>`) | Log warning, proceed without comparison |
| Comment was edited (`updated` > `created`) | Warn user, still proceed with comparison |
| Format tags differ (`sha256-md` vs `sha256-adf`) | Log format mismatch warning, skip comparison, proceed |
| Format tags match, hex digests match | Proceed silently (this scenario) |
| Format tags match, hex digests mismatch | Alert user, display expected vs actual, ask proceed/stop, halt until response |
| Script exits non-zero | Warn, skip integrity check, proceed |
