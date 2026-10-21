# Step 1.5 -- Description Integrity Verification for TC-9201

## Procedure

### 1. Retrieve Issue Comments

After fetching the task in Step 1, retrieve all comments on the Jira issue:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the Digest Comment

Search all returned comments for those whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

In this case, exactly one comment matches. Its full body is:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since there is only one matching comment, it is selected directly (no need to resolve multiple matches by timestamp).

### 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this case, the two timestamps are identical -- the comment has not been edited after initial posting. No warning is needed. Proceed with digest comparison.

### 4. Extract the Stored Digest

Parse the tagged digest from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The tag is not the legacy untagged format (`sha256:<hex>`), so no legacy-format warning is needed.

### 5. Compute the Current Digest

Extract the description field from the issue response (the markdown text of TC-9201's description). Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (plain markdown text in this case) and outputs a format-tagged digest. For example:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If the script exits non-zero, log a warning and skip the integrity check without blocking execution.

### 6. Compare Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md` -- they match. Proceed to hex digest comparison. (If they differed, e.g., stored was `sha256-adf` but computed was `sha256-md`, a format mismatch warning would be logged and the integrity check would be skipped.)

### 7. Compare Hex Digests

The stored hex digest and the computed hex digest are identical:

- **Stored:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Result: MATCH.**

### 8. Outcome

The digests match. The description has not been modified since plan-feature created the task. Per the protocol, proceed silently -- no user prompt, no warning, no additional latency. Continue directly to Step 2 (Verify Dependencies).

## Summary of Decision Logic

| Condition | Outcome |
|---|---|
| Digest comment found? | Yes -- one comment with marker `[sdlc-workflow] Description digest:` |
| Comment edited? | No -- `created` equals `updated` |
| Legacy format? | No -- uses format-tagged `sha256-md:` prefix |
| Format tags match? | Yes -- both `sha256-md` |
| Hex digests match? | Yes -- identical hashes |
| **Action** | **Proceed silently to Step 2** |
