# Step 1.5 -- Description Integrity Verification

## Procedure

### 1. Retrieve issue comments

Fetch all comments on the Jira issue TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search through the returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:`, as defined in `shared/description-digest-protocol.md`. If multiple comments match the marker (e.g., from plan-feature re-runs), select the most recent one by `created` timestamp.

One matching comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 3. Check for comment editing

Compare the comment's `created` and `updated` timestamps. In this case, the timestamps are identical, meaning the comment has not been edited after initial posting. No warning is needed.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The digest uses the format-tagged format (not the legacy untagged `sha256:<hex>` format), so full verification proceeds.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response, write it to a temp file, and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs a tagged digest:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 6. Compare format tags

The stored tag is `sha256-md` and the computed tag is `sha256-md`. The format tags match, so hex digest comparison proceeds.

### 7. Compare hex digests

- **Stored**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The hex digests **match**.

## Outcome

The description has not been modified since plan-feature created it. Per the SKILL.md Step 1.5 rule for a matching digest: **proceed silently** -- no additional user prompt, no added latency, no warning displayed. Execution continues directly to Step 2 (Verify Dependencies) without interruption.
