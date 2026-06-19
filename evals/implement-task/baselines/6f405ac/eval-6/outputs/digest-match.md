# Step 1.5 -- Verify Description Integrity

## Scenario

- Jira issue: TC-9201
- Digest comment found: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Comment `created` and `updated` timestamps: identical (comment was not edited)
- Format tag: `sha256-md`
- Computed digest (from current description via `scripts/sha256-digest.py`): `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Result: format tags match, hex digests match

## Verification Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201 using `jira.get_issue_comments("TC-9201")`.

### 2. Locate the digest comment

Search all comments for bodies starting with the marker string `[sdlc-workflow] Description digest:`. One comment matches:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If multiple comments matched, we would select the most recent one by `created` timestamp. In this case only one comment matches.

### 3. Check for comment editing

Compare the comment's `created` and `updated` timestamps. They are identical, confirming the comment was not edited after initial posting. No warning is needed. Proceed to digest comparison.

(If `updated` were later than `created`, we would warn: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." but still proceed with the comparison.)

### 4. Extract the stored digest

Parse the comment body to extract:
- Format tag: `sha256-md` (indicates the description was hashed as markdown text)
- Hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

This is a format-tagged digest (not legacy `sha256:<hex>` format), so we proceed with verification.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response. Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

### 6. Compare format tags

Stored tag: `sha256-md`
Computed tag: `sha256-md`

Tags match -- proceed to hex digest comparison.

(If tags differed, e.g. stored `sha256-adf` vs computed `sha256-md`, we would log: "Digest format mismatch (stored: sha256-adf, current: sha256-md) -- producer and consumer used different API access methods. Skipping integrity check." and proceed normally without blocking.)

### 7. Compare hex digests

Stored hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
Computed hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Match.** The description has not been modified since plan-feature created it.

## Outcome

**Proceed silently.** Per the protocol, when digests match: no additional user prompt, no added latency. Continue directly to Step 2 (Verify Dependencies) and subsequent implementation steps.

No warnings, no user interaction, no delay -- the integrity check passes cleanly and implementation proceeds immediately.
