# Description Integrity Verification (Step 1.5) for TC-9201

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

This returns one comment posted by a previous plan-feature run.

### 2. Locate the digest comment

Search for comments whose body starts with the marker string `[sdlc-workflow] Description digest:`. One comment matches:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Only one digest comment exists, so it is selected directly (no need to resolve multiple matches by `created` timestamp).

### 3. Check for comment editing

Compare the comment's `created` and `updated` timestamps. They are identical, which means the comment has not been edited after initial posting. No warning is needed. Proceed with digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

This is not a legacy untagged format (`sha256:<hex>`) -- it uses the current format-tagged scheme, so no legacy warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response. Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The script exits with status 0, so the digest is valid.

### 6. Compare format tags

- Stored tag: `sha256-md`
- Computed tag: `sha256-md`

Tags match. Both the producer (plan-feature) and consumer (implement-task) used the same Jira access method, so the digests are directly comparable. No format mismatch warning is needed.

### 7. Compare hex digests

- Stored hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Computed hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Match.** The digests are identical.

## Outcome

The description has not been modified since plan-feature created the task. Per the protocol, proceed silently -- no additional user prompt, no added latency, no warning. Implementation continues to Step 2 (Verify Dependencies).

## Summary of decision points evaluated

| Check | Result | Action |
|---|---|---|
| Digest comment found? | Yes (1 comment) | Proceed with verification |
| Multiple digest comments? | No | Use the single comment |
| Comment edited? (created vs updated) | No (timestamps identical) | No warning |
| Legacy untagged format? | No (uses `sha256-md:` tag) | No legacy warning |
| Script exit code | 0 (success) | Use computed digest |
| Format tags match? | Yes (both `sha256-md`) | Compare hex digests |
| Hex digests match? | Yes | Proceed silently |
