# Step 1.5 -- Description Integrity Verification

## Procedure

### 1. Retrieve issue comments

Fetch all comments on Jira issue TC-9201 using:

```
jira.get_issue_comments(TC-9201)
```

This returns all comments posted on the issue, including any digest comments left by plan-feature.

### 2. Locate the digest comment

Search all returned comments for those whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

This marker string is defined in `shared/description-digest-protocol.md` and is fixed across all skills. One matching comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches the marker, it is selected directly. (If multiple comments had matched, the most recent one by `created` timestamp would be selected, per the protocol's "Multiple Digest Comments" rule.)

### 3. Parse the format-tagged digest

From the comment body, extract the tagged digest value after the marker prefix:

- **Full tagged digest**: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Format tag**: `sha256-md` (indicates the digest was computed from the markdown representation of the description)
- **Hex hash**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

This is not the legacy untagged format (`sha256:<hex>`) -- it includes a format tag (`md`), so we proceed with full verification rather than skipping.

### 4. Check comment timestamps (edit detection)

The digest comment's `created` and `updated` timestamps are compared:

- **Result**: `created` == `updated` -- the timestamps are identical.
- **Conclusion**: The comment was NOT edited after initial posting. No tampering warning is needed. Proceed with digest comparison.

### 5. Compute current digest

Extract the description field from the TC-9201 issue response (the markdown text fetched via the Jira API). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs a format-tagged digest:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The script exits with status 0 (success), so the computed digest is valid.

### 6. Compare format tags

- **Stored tag**: `sha256-md`
- **Computed tag**: `sha256-md`
- **Result**: Tags MATCH. Both the producer (plan-feature) and consumer (implement-task) used the same Jira access method (markdown via MCP), so the digests are directly comparable. Proceed to hex hash comparison.

### 7. Compare hex hashes

- **Stored hash**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed hash**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Result**: Hashes MATCH.

## Conclusion

Digests match. The task description has not been modified since plan-feature created it. The description integrity is verified.

**Action**: Proceed silently to Step 2. No user prompt, no pause, no alert, no additional latency. The integrity check passed -- continue with implementation planning immediately.
