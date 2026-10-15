# Description Integrity Verification — Step 1.5 for TC-9201

## Scenario

- Jira issue TC-9201 has one comment with body:
  `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- The comment's `created` and `updated` timestamps are identical.
- The digest computed from the current task description matches the stored digest (same format tag and same hash).

## Step-by-Step Verification

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments(TC-9201)
```

Returns one comment whose body starts with the marker `[sdlc-workflow] Description digest:`.

### 2. Locate the digest comment

Search all comments for bodies starting with `[sdlc-workflow] Description digest:`. One comment matches. Since there is only one matching comment, it is selected directly (no need to resolve among multiple by `created` timestamp).

### 3. Check for comment editing

Compare the comment's `created` and `updated` timestamps. They are identical, meaning the comment has not been edited after initial posting. No warning is emitted. Proceed with digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- Full value: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Format tag: `md`
- Hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

This is not a legacy untagged format (`sha256:<hex>` without a format tag), so no legacy-format warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response. Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is markdown text (not ADF JSON), the script outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The script exits with status 0, so the integrity check proceeds.

### 6. Compare format tags

- Stored tag: `sha256-md`
- Computed tag: `sha256-md`

Tags match. Proceed to hex digest comparison.

### 7. Compare hex digests

- Stored hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Computed hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Match.**

### 8. Outcome

The digests match. Per the protocol, proceed silently — no additional user prompt, no added latency. The description has not been modified since plan-feature created it. Implementation continues to Step 2.

## Summary of Decision Path

| Check | Result | Action |
|---|---|---|
| Digest comment found? | Yes (1 comment) | Proceed with verification |
| Comment edited? | No (`created` == `updated`) | No warning |
| Digest format | `sha256-md` (format-tagged, not legacy) | Proceed with comparison |
| Script exit code | 0 | Proceed |
| Format tags match? | Yes (both `sha256-md`) | Compare hex digests |
| Hex digests match? | Yes | Proceed silently |
