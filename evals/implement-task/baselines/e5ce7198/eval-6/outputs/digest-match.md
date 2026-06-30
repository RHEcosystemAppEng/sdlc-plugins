# Step 1.5 -- Description Integrity Verification for TC-9201

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201 via `jira.get_issue_comments(<jira-issue-id>)`.

### 2. Locate the digest comment

Search all returned comments for those whose body starts with the marker string `[sdlc-workflow] Description digest:`. One comment is found with body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches, it is selected (no tie-breaking needed).

### 3. Check for comment editing

Compare the comment's `created` and `updated` timestamps. They are identical, so no editing occurred. No warning is emitted. Proceed with digest comparison.

### 4. Extract the stored digest

Parse the tagged digest from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag is `sha256-md` (not the legacy untagged `sha256:<hex>` format), so verification proceeds normally.

### 5. Compute the current digest

Extract the Description field from the fetched TC-9201 issue response. Write it to a temporary file `/tmp/desc-TC-9201.txt` and run:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is plain text (markdown), not JSON, the script outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 6. Compare format tags

- Stored format tag: `sha256-md`
- Computed format tag: `sha256-md`

Tags match. Proceed to hex digest comparison.

### 7. Compare hex digests

- Stored hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Computed hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Digests match.**

## Outcome

The description has not been modified since plan-feature created it. Per the protocol, the skill proceeds silently -- no user prompt, no warning, no added latency. Execution continues to Step 2 (Verify Dependencies).
