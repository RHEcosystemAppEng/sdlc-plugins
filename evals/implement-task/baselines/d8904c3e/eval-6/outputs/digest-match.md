# Step 1.5 -- Description Integrity Verification for TC-9201

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search all returned comments for bodies starting with the marker string `[sdlc-workflow] Description digest:`.

One matching comment is found:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches the marker, it is selected directly. If multiple comments had matched, the most recent one by `created` timestamp would be selected.

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this case, the timestamps are identical, meaning the comment has not been edited after initial posting. No warning is needed. Proceed with digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

This is not a legacy untagged format (which would be `sha256:<hex>` without the `-md` or `-adf` suffix), so no legacy warning is needed.

### 5. Compute the current digest

Extract the description field from the issue response (the markdown text of the task description). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (plain text / markdown in this case) and outputs a format-tagged digest. Check that the script exits with status 0 before using the output.

Expected output (given the assumption that the digest matches):

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 6. Compare format tags

- Stored tag: `sha256-md`
- Computed tag: `sha256-md`

Tags match. Both the producer (plan-feature) and the consumer (implement-task) used the same Jira access method, producing markdown-format descriptions. Proceed to hex digest comparison.

If the tags had differed (e.g., stored `sha256-adf` vs. computed `sha256-md`), a warning would be logged ("Digest format mismatch -- producer and consumer used different API access methods. Skipping integrity check.") and execution would proceed without blocking.

### 7. Compare hex digests

- Stored hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Computed hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Result: MATCH**

The digests are identical. The task description has not been modified since plan-feature created it.

## Outcome

Proceed silently to Step 2. No user prompt is needed, no warning is displayed, and no additional latency is introduced. The integrity of the task description is confirmed.

## Summary of checks performed

| Check | Result | Action |
|---|---|---|
| Digest comment found | Yes (1 comment with marker) | Proceed to verification |
| Comment edit detection | created == updated (unmodified) | No warning needed |
| Digest format | Tagged (`sha256-md`), not legacy | Proceed with comparison |
| Format tag comparison | Both `sha256-md` (match) | Proceed to hex comparison |
| Hex digest comparison | Match | Proceed silently |
