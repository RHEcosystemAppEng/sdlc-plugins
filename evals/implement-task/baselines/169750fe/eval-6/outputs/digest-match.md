# Description Integrity Verification — Step 1.5

## Procedure

### 1. Retrieve Issue Comments

After fetching the task description in Step 1, retrieve all comments on the Jira issue TC-9201:

```
jira.get_issue_comments(TC-9201)
```

### 2. Locate the Digest Comment

Search all returned comments for bodies starting with the marker string `[sdlc-workflow] Description digest:` as defined in `shared/description-digest-protocol.md`.

One comment is found with body:
```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches, it is selected as the digest comment.

### 3. Check for Comment Editing

The comment's `created` and `updated` timestamps are identical, confirming the comment has not been edited after initial posting. No warning is needed.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:
- **Format tag:** `sha256-md`
- **Hex digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag is `sha256-md` (not the legacy untagged `sha256:` format), so proceed with comparison.

### 5. Compute the Current Digest

Extract the description field from the fetched issue response. Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the Markdown format and outputs a tagged digest:
```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 6. Compare Format Tags

The stored format tag (`sha256-md`) matches the computed format tag (`sha256-md`). Both used the same Markdown-based access method. Proceed to hex digest comparison.

### 7. Compare Hex Digests

- **Stored digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Result: MATCH.**

The digests are identical, confirming the task description has not been modified since plan-feature created it.

## Outcome

**Proceed silently.** No user prompt is needed, no alert is displayed, and no additional latency is introduced. Execution continues directly to Step 2 (Verify Dependencies) without interruption.
