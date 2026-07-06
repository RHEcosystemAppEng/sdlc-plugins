# Step 1.5 — Description Integrity Verification for TC-9201

## Scenario

- **Digest comment found**: One comment on TC-9201 with body:
  `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Comment timestamps**: `created` and `updated` are identical (comment was not edited after posting).
- **Computed digest**: The current task description, when written to a temp file and processed through `scripts/sha256-digest.py`, produces `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890` — an exact match.

## Verification Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201 using `jira.get_issue_comments("TC-9201")`.

### 2. Locate the digest comment

Search all returned comments for bodies starting with the marker string `[sdlc-workflow] Description digest:`. One comment matches. Since there is only one matching comment, there is no need to resolve multiple candidates by `created` timestamp — this single comment is selected.

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this scenario, they are identical, meaning the comment has not been edited after initial posting. No warning is emitted. Proceed to digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Full tagged value**: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Format tag**: `sha256-md` (indicates the description was hashed as markdown/plain text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag is not the legacy untagged format (`sha256:<hex>`), so no legacy warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response. Write it to a temp file (e.g., `/tmp/desc-TC-9201.txt`) and run:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects that the input is plain text (not ADF JSON) and outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The script exits with status 0 (success).

### 6. Compare format tags

- Stored tag: `sha256-md`
- Computed tag: `sha256-md`

Tags match. No format mismatch warning is needed. Proceed to hex digest comparison.

### 7. Compare hex digests

- Stored hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Computed hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Match.** The description has not been modified since plan-feature created it.

## Outcome

Proceed silently to Step 2 (Verify Dependencies). No user prompt is required, no warning is emitted, and no additional latency is introduced. The integrity check passes cleanly.

## Summary of Decision Points

| Check | Result | Action |
|---|---|---|
| Digest comment found? | Yes (1 comment) | Proceed with verification |
| Multiple digest comments? | No | Use the single matching comment |
| Comment edited? (`created` vs `updated`) | No (timestamps identical) | No warning; proceed |
| Legacy untagged format? | No (`sha256-md` is format-tagged) | No warning; proceed |
| Format tags match? | Yes (both `sha256-md`) | Compare hex digests |
| Hex digests match? | Yes | Proceed silently |
