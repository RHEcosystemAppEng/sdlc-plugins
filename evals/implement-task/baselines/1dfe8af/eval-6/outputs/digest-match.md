# Description Integrity Verification (Step 1.5) -- Digest Match Scenario

## Overview

This document describes how the implement-task skill handles the description integrity verification in Step 1.5 for task TC-9201, given that the digest matches.

## Step-by-Step Verification Process

### 1. Retrieve Issue Comments

After fetching the task in Step 1, retrieve all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the Digest Comment

Search through all returned comments for ones whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

This marker is defined in `shared/description-digest-protocol.md` and is fixed across all skills and invocations. In this scenario, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If multiple comments matched (e.g., from plan-feature re-runs), the most recent one by `created` timestamp would be selected. In this case, only one comment matches.

### 3. Check for Comment Editing

Compare the comment's `created` and `updated` timestamps. In this scenario, the timestamps are identical, meaning the comment has not been edited after initial posting. No warning is needed -- proceed directly to digest comparison.

If `updated` were later than `created`, a warning would be surfaced: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." But the comparison would still proceed.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Full value**: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Format tag**: `md` (indicates the description was hashed as markdown text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag is not `sha256:<hex>` (legacy untagged format), so no legacy-format warning is needed.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (the markdown text of the task description). Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is fetched as markdown text (from MCP), the script outputs a tagged digest in the format:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If the script exited non-zero, we would warn and skip the integrity check without blocking execution. In this scenario, the script succeeds.

### 6. Compare Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md`. The tags match, so we proceed to hex digest comparison.

If the tags differed (e.g., stored `sha256-adf` vs. computed `sha256-md`), we would log a warning about the format mismatch ("Digest format mismatch -- producer and consumer used different API access methods. Skipping integrity check.") and proceed normally without blocking.

### 7. Compare Hex Digests

The stored hex digest and the computed hex digest are identical:

- **Stored**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Result: MATCH**

### 8. Outcome -- Proceed Silently

Since the digests match, the description has not been modified since plan-feature created it. The skill proceeds silently to Step 2 (Verify Dependencies) with:

- No user prompt or alert
- No added latency
- No warning message
- No pause in execution

This is the happy path -- the integrity check confirms the description is unmodified and execution continues without interruption.

## Summary of Decision Points

| Condition | Result | Action |
|---|---|---|
| Digest comment found | Yes | Continue verification |
| Comment edited (created != updated) | No (timestamps identical) | No warning needed |
| Digest format is legacy (untagged `sha256:`) | No (tagged `sha256-md:`) | No legacy warning |
| Format tags match | Yes (both `sha256-md`) | Compare hex digests |
| Hex digests match | Yes | Proceed silently |

The entire verification completes without any user interaction, which is the expected behavior for the happy path where the description remains intact from planning through implementation.
