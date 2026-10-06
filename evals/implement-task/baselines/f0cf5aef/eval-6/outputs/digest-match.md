# Step 1.5 -- Verify Description Integrity for TC-9201

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201 using:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search the returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:`. This marker is defined in `shared/description-digest-protocol.md` and is the fixed prefix used by all sdlc-workflow skills.

In this case, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches the marker, it is selected directly. If multiple comments matched, the most recent one by `created` timestamp would be selected.

### 3. Check for comment editing

Compare the comment's `created` and `updated` timestamps. In this case, they are identical -- the comment has not been edited after initial posting. No warning is needed; proceed with digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

This is a format-tagged digest (not the legacy untagged `sha256:<hex>` format), so full verification proceeds.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text from the Description section). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as plain text (markdown) and outputs a tagged digest in the format `sha256-md:<64-char-hex>`.

### 6. Compare format tags

The stored tag is `sha256-md` and the computed tag is also `sha256-md` -- both tags match. This confirms the producer (plan-feature) and consumer (implement-task) used the same Jira access method (both received markdown). Proceed to hex digest comparison.

### 7. Compare hex digests

The stored hex digest matches the computed hex digest (both are `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`).

## Result: MATCH -- Proceed silently

The digests match. Per the protocol, this means the task description has not been modified since plan-feature created it. The skill proceeds silently to subsequent steps -- no user prompt, no alert, no added latency. The integrity of the description is confirmed.

Execution continues directly to Step 2 (Verify Dependencies).
