# Step 1.5 -- Description Integrity Verification for TC-9201

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201 using `jira.get_issue_comments(TC-9201)`.

### 2. Locate the digest comment

Search through the returned comments for any whose body starts with the marker string defined in `shared/description-digest-protocol.md`:

```
[sdlc-workflow] Description digest:
```

One matching comment is found. Since only one comment matches, it is selected directly (if multiple had matched, the most recent by `created` timestamp would be selected per the protocol).

The full comment body is:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 3. Check for comment editing

Compare the comment's `created` and `updated` timestamps. In this case, the timestamps are identical -- the comment has not been edited after initial posting. No warning is needed. Proceed with digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format is the current tagged format (not the legacy untagged `sha256:<hex>` format), so no legacy warning is needed.

### 5. Compute the current digest

Fetch the current description from the Jira issue via `jira.get_issue(TC-9201)`. Write the description content to a temporary file `/tmp/desc-TC-9201.txt`. Compute the digest using the project script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (plain text/markdown in this case) and outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The script exits with status 0 (success).

### 6. Compare format tags

- Stored tag: `sha256-md`
- Computed tag: `sha256-md`

The format tags match. Both the producer (plan-feature) and consumer (implement-task) used the same Jira access method (markdown/MCP path). Proceed to hex digest comparison.

### 7. Compare hex digests

- Stored hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Computed hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The hex digests are identical.

## Result

**MATCH** -- The description has not been modified since plan-feature created it.

Proceed silently to the next step. No user prompt is displayed. No alert is raised. No additional latency is introduced. This is the happy path -- the integrity check confirms the description is intact, and execution continues without interruption to Step 2 (Verify Dependencies).
