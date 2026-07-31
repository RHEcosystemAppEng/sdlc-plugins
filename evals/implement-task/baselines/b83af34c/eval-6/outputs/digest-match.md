# Description Integrity Verification (Step 1.5) -- Digest Match Scenario

## Context

Task TC-9201 was fetched in Step 1. A description integrity check is now performed
before proceeding with implementation.

## Step 1.5 Execution

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search the returned comments for any whose body starts with the marker string
`[sdlc-workflow] Description digest:`. One comment is found:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

This is the only matching comment, so it is selected (no need to resolve among
multiple candidates by `created` timestamp).

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the
timestamps are identical -- the comment has not been edited after initial posting.
No warning is emitted. Proceed with digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The tag is `sha256-md` (not the legacy untagged `sha256:<hex>` format), so no
legacy-format warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response. Write it to a
temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

(In this scenario we assume the script exits zero and the output matches the stored
digest exactly.)

### 6. Compare format tags

- Stored tag: `sha256-md`
- Computed tag: `sha256-md`

Tags match. Proceed to hex digest comparison.

### 7. Compare hex digests

- Stored hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Computed hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Match.** The description has not been modified since plan-feature created it.

### 8. Outcome

Per the SKILL.md specification for the match case: **proceed silently -- no
additional user prompt, no added latency.** No warning, no confirmation dialog,
no message to the user. Step 1.5 completes and execution continues directly to
Step 2 (Verify Dependencies) without any interruption.

## Summary

| Check                  | Result                  | Action              |
|------------------------|-------------------------|---------------------|
| Digest comment found   | Yes (1 comment)         | Proceed to verify   |
| Comment edited         | No (created == updated) | No warning          |
| Digest format          | Tagged (sha256-md)      | Not legacy, proceed |
| Format tags match      | Yes (both sha256-md)    | Compare hex digests |
| Hex digests match      | Yes                     | Proceed silently    |
