# Step 1.5 -- Description Integrity Verification for TC-9201

## Scenario

The Jira issue TC-9201 has one comment posted by a previous plan-feature run with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The comment's `created` and `updated` timestamps are identical. The digest matches the digest computed from the current task description.

## Verification Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search all returned comments for bodies starting with the marker string `[sdlc-workflow] Description digest:`. One comment matches. Since there is only one matching comment, no timestamp-based selection among multiple digest comments is needed -- use this comment directly.

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this scenario, they are identical, which means the comment was not edited after initial posting. No warning is emitted. Proceed with digest comparison.

### 4. Extract the stored digest

Parse the comment body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

- Format tag: `sha256-md`
- Hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag is `sha256-md` (not the legacy untagged `sha256:<hex>` format), so no legacy format warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response. Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 6. Compare format tags

- Stored tag: `sha256-md`
- Computed tag: `sha256-md`

Tags match. Proceed to hex digest comparison.

### 7. Compare hex digests

- Stored hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Computed hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Match.** The description has not been modified since plan-feature created it.

## Outcome

Proceed silently -- no additional user prompt, no warning, no added latency. The description integrity is verified. Continue to Step 2 (Verify Dependencies).
