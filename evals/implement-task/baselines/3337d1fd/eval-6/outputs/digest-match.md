# Step 1.5 -- Description Integrity Verification for TC-9201

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search returned comments for bodies starting with the marker string `[sdlc-workflow] Description digest:`.

One comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches the marker, it is selected (no need to pick the most recent among multiple matches).

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. They are identical, which means the comment has not been edited after initial posting. No warning is needed. Proceed with digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

This is not the legacy untagged format (`sha256:<hex>`) -- it uses the format-tagged format (`sha256-md:<hex>`), so no legacy warning is needed.

### 5. Compute the current digest

Extract the description field from the issue response, write it to a temporary file, and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs a tagged digest. Since the description is plain markdown, the script outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Check the exit code -- if non-zero, warn and skip the integrity check. In this case, exit code is 0.

### 6. Compare format tags

- Stored tag: `sha256-md`
- Computed tag: `sha256-md`

Tags match. No format mismatch warning needed. Proceed to hex digest comparison.

### 7. Compare hex digests

- Stored hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Computed hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Match.** The description has not been modified since plan-feature created it.

## Outcome

Proceed silently to Step 2. No user prompt, no warning, no added latency. The integrity check passes cleanly:

- The digest comment was found (not a pre-digest-tracking task)
- The comment was not edited after posting (created == updated)
- The digest uses the current format-tagged scheme (not legacy)
- The format tags match (both `sha256-md`, so producer and consumer used the same API access method)
- The hex digests match (description is unmodified)
