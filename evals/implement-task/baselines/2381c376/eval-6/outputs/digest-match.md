# Step 1.5 -- Description Integrity Verification for TC-9201

## Procedure

After fetching the TC-9201 issue in Step 1, Step 1.5 verifies that the task description has not been modified since plan-feature created it, following the digest protocol in `shared/description-digest-protocol.md`.

### 1. Retrieve issue comments

Fetch all comments on TC-9201 using `jira.get_issue_comments("TC-9201")`.

### 2. Locate the digest comment

Search all returned comments for bodies starting with the marker string `[sdlc-workflow] Description digest:`. One comment is found with body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since there is only one matching comment, it is selected directly (no need to compare `created` timestamps to pick the most recent).

### 3. Check for comment editing

Compare the comment's `created` and `updated` timestamps. They are identical, which means the comment has not been edited after initial posting. No warning is emitted. Proceed with digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:
- **Format tag:** `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The digest uses the current tagged format (`sha256-md:`), not the legacy untagged format (`sha256:`), so no legacy-format warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text from the Description section). Write it to a temp file `/tmp/desc-TC-9201.txt` and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as markdown text and outputs a tagged digest in the format `sha256-md:<64-char-hex>`.

### 6. Compare format tags

The stored tag is `sha256-md` and the computed tag is also `sha256-md`. Tags match, so proceed to hex digest comparison. No format-mismatch warning is needed.

### 7. Compare hex digests

The stored hex digest matches the computed hex digest (both are `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`).

### Result: Match -- Proceed silently

Per the SKILL.md specification (Step 1.5, item 4e): when the digests match, **proceed silently** -- no additional user prompt, no added latency. The description is confirmed to be unmodified since plan-feature created it.

No warning is displayed. No user interaction is required. Execution continues directly to Step 2 (Verify Dependencies).
