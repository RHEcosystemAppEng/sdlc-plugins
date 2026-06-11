# Description Integrity Verification — Step 1.5

## Context

Task TC-9201 has one Jira comment posted by a previous plan-feature run with body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

## Procedure

### 1. Retrieve issue comments

Fetch all comments on the Jira issue TC-9201 using:

```
jira.get_issue_comments(TC-9201)
```

### 2. Locate the digest comment

Search all returned comments for those whose body starts with the marker string `[sdlc-workflow] Description digest:`. This is the fixed marker defined in `shared/description-digest-protocol.md`. If multiple comments match (e.g., from plan-feature re-runs), select the most recent one by `created` timestamp.

In this case, exactly one comment matches the marker. The full comment body is:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 3. Check for comment editing

Compare the comment's `created` and `updated` timestamps. In this case, the `created` and `updated` timestamps are identical, meaning the comment has not been edited after initial posting. No warning is needed — proceed to digest comparison.

If `updated` were later than `created`, a warning would be surfaced: "Digest comment was edited after initial posting — integrity cannot be fully guaranteed." The skill would still proceed with digest comparison regardless.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

This is not a legacy untagged format (`sha256:<hex>`), so no legacy warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response. Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is markdown text (fetched via MCP), the script outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If the script exits non-zero, the skill would warn and skip the integrity check without blocking execution.

### 6. Compare format tags

- **Stored tag**: `sha256-md`
- **Computed tag**: `sha256-md`

The tags match. Both the producer (plan-feature) and consumer (implement-task) used the same Jira access method (both yielded markdown text). No format mismatch warning is needed.

If the tags differed (e.g., stored `sha256-adf` vs. computed `sha256-md`), the skill would log: "Digest format mismatch (stored: sha256-adf, current: sha256-md) — producer and consumer used different API access methods. Skipping integrity check." and proceed normally.

### 7. Compare hex digests

- **Stored hex**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed hex**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**The digests match.** The description has not been modified since plan-feature created it.

## Outcome

**Proceed silently.** Per the protocol specification (SKILL.md Step 1.5.e and `shared/description-digest-protocol.md` Consumer Verification section 4): when tags match and hex digests match, proceed silently with no additional user prompt and no added latency. The user is not alerted, execution is not paused, and no confirmation is requested. The skill moves directly to Step 2 (Verify Dependencies).
