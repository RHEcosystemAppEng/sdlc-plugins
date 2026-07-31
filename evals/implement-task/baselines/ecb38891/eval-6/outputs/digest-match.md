# Step 1.5 -- Description Integrity Verification

## Process

### 1. Retrieve Issue Comments

After fetching the task TC-9201 via `jira.get_issue(TC-9201)` in Step 1, retrieve all comments on the issue:

```
jira.get_issue_comments(TC-9201)
```

### 2. Locate the Digest Comment

Search all returned comments for those whose body starts with the marker string `[sdlc-workflow] Description digest:` as defined in `shared/description-digest-protocol.md`. If multiple comments match, select the most recent one by `created` timestamp.

In this case, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 3. Check for Comment Editing

Compare the comment's `created` and `updated` timestamps. In this case, they are identical, confirming the comment was not edited after initial posting. No warning is needed.

### 4. Parse the Stored Digest

Extract the format-tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The `sha256-md` tag indicates the digest was computed from the markdown representation of the description.

### 5. Compute the Current Digest

Extract the description field from the issue response, write it to a temporary file, and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs a format-tagged digest:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 6. Compare Format Tags

The stored tag (`sha256-md`) and the computed tag (`sha256-md`) match. Both used the markdown representation. Proceed to hex digest comparison.

### 7. Compare Hex Digests

- **Stored digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The digests match. The description has not been modified since plan-feature created it.

## Result

**Digests match.** Proceeding silently to Step 2 and subsequent steps without any additional user prompt or latency. No alert or pause is needed -- the happy path requires no user interaction for the digest check.
