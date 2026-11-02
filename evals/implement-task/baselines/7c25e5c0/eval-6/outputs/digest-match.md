# Description Integrity Verification — Step 1.5

## Process

After fetching task TC-9201 via `jira.get_issue(TC-9201)` and parsing the structured description in Step 1, Step 1.5 verifies that the description has not been modified since plan-feature created it.

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments(TC-9201)
```

### 2. Locate the digest comment

Search through the returned comments for one whose body starts with the marker string `[sdlc-workflow] Description digest:`, as defined in `shared/description-digest-protocol.md`.

Found comment body:
```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Only one comment matches the marker, so this is the digest comment to use.

### 3. Check for comment editing

Compare the comment's `created` and `updated` timestamps. In this case, they are identical — the comment has not been edited after initial posting. No warning needed.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:
- **Format tag**: `sha256-md`
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag is `sha256-md` (not the legacy untagged `sha256:` format), so proceed with comparison.

### 5. Compute the current digest

Extract the description field from the issue response. Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the format and outputs a tagged digest. The computed result:
- **Format tag**: `sha256-md`
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

### 6. Compare format tags

Stored tag: `sha256-md`
Computed tag: `sha256-md`

The format tags match — both used the same API access method (Markdown format). Proceed to hex digest comparison.

### 7. Compare hex digests

Stored hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
Computed hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Result: MATCH**

### 8. Proceed silently

The digests match. The description has not been modified since plan-feature created it. Per the protocol, proceed silently — no additional user prompt, no added latency. Continue directly to Step 2 (Verify Dependencies) without any interruption or notification to the user.
