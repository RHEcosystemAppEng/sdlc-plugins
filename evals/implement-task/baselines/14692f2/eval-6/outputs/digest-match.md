# Description Integrity Verification -- Step 1.5

## Context

Task TC-9201 has one comment posted by a previous plan-feature run with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The comment's `created` and `updated` timestamps are identical.

## Step-by-Step Verification Process

### 1. Retrieve issue comments

Fetch all comments on TC-9201 using `jira.get_issue_comments("TC-9201")`.

### 2. Locate the digest comment

Search all returned comments for those whose body starts with the marker string `[sdlc-workflow] Description digest:`. In this case, exactly one comment matches. If multiple had matched, the most recent one by `created` timestamp would be selected.

The matching comment body is:
```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 3. Check for comment editing (defense-in-depth)

Compare the comment's `created` and `updated` timestamps. In this scenario, they are identical, which means the comment has not been edited after posting. No warning is needed. Proceed with digest comparison.

If `updated` had been later than `created`, a warning would be surfaced: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." The verification would still proceed regardless.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:
- **Format tag**: `md` (from `sha256-md:`)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

This is not a legacy untagged format (`sha256:<hex>`) -- it uses the current format-tagged scheme (`sha256-md:<hex>`), so full verification is performed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text returned by the Jira API). Write it to a temp file:

```bash
# Write the description to a temp file
cat > /tmp/desc-TC-9201.txt << 'DESCRIPTION'
<current description content from jira.get_issue response>
DESCRIPTION

# Compute the digest using the project script
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description was fetched as markdown text (via MCP), the script outputs a tagged digest in the form `sha256-md:<64-char-hex>`.

If the script exits non-zero, a warning is logged and the integrity check is skipped -- execution is not blocked.

### 6. Compare format tags

The stored tag is `sha256-md` and (per the scenario) the computed tag is also `sha256-md`. The tags match, so direct hex digest comparison is performed.

If the tags had differed (e.g., stored `sha256-adf` vs computed `sha256-md`), a warning would be logged: "Digest format mismatch (stored: adf, current: md) -- producer and consumer used different API access methods. Skipping integrity check." Execution would proceed normally without blocking.

### 7. Compare hex digests

The stored hex digest is `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.

Per the eval scenario, this MATCHES the digest computed from the current task description (same format tag and same hash).

**Result: MATCH**

### 8. Outcome

Since the format tags match and the hex digests match, the description has not been modified since plan-feature created it. Proceed silently to the next step -- no additional user prompt is needed, no warning is surfaced, and no added latency is introduced.

## Summary of Handling for a Matching Digest

When the digest matches:
1. Comment found with marker `[sdlc-workflow] Description digest:` -- proceed with verification.
2. Comment not edited (`created` == `updated`) -- no timestamp warning needed.
3. Format tags match (`sha256-md` == `sha256-md`) -- proceed with hex comparison.
4. Hex digests match -- description integrity confirmed.
5. **Action: proceed silently.** No user interaction, no warning, no prompt. Move directly to Step 2 (Verify Dependencies).
