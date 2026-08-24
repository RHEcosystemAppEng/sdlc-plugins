# Description Integrity Verification (Step 1.5)

## Process

After fetching the Jira issue TC-9201 in Step 1, the skill proceeds to verify description integrity per `shared/description-digest-protocol.md`.

### 1. Retrieve Issue Comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the Digest Comment

Search through the returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:` as defined in `shared/description-digest-protocol.md`.

Found one matching comment:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If multiple comments matched the marker, the most recent one by `created` timestamp would be selected per the protocol's "Multiple Digest Comments" section.

### 3. Comment Edit Detection

The comment's `created` and `updated` timestamps are identical, indicating the comment has not been edited since it was posted. No warning is needed. Proceed with digest comparison.

### 4. Parse the Stored Digest

Extract the format tag and hex digest from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag `sha256-md` indicates the digest was computed from the markdown representation of the description (MCP access path).

### 5. Compute the Current Digest

Extract the current description from the issue response, write it to a temp file, and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description was fetched via MCP (markdown), the output is:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 6. Compare Format Tags

Both the stored tag and the computed tag are `sha256-md` -- they match. Proceed to hex digest comparison.

If they had differed (e.g., stored `sha256-adf` vs. computed `sha256-md`), the skill would log a warning about the producer and consumer using different API access methods and skip the integrity check.

### 7. Compare Hex Digests

- **Stored digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Result: MATCH**

The digests are identical. The task description has not been modified since plan-feature created it.

### 8. Outcome: Proceed Silently

Per the protocol and Step 1.5 of the SKILL.md, when the digests match:

> "**Match**: proceed silently -- no additional user prompt, no added latency."

The skill does not alert the user, does not pause execution, and does not display any digest information. It proceeds directly to Step 2 (Verify Dependencies) without interruption. This is the happy path -- the integrity check confirms the description is authentic and unmodified, so it adds zero friction to the implementation workflow.
