# Description Integrity Verification (Step 1.5) -- TC-9201

## Overview

Step 1.5 verifies that the task description has not been modified since plan-feature created it. This uses the digest protocol defined in `shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve Issue Comments

Fetch all comments on TC-9201 using:

```
jira.get_issue_comments("TC-9201")
```

This returns the full list of comments on the issue, each with `body`, `created`, and `updated` fields.

### 2. Locate the Digest Comment

Search through all returned comments for those whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

In this scenario, one comment matches with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches, it is selected directly. If multiple comments matched the marker, the most recent one by `created` timestamp would be selected.

### 3. Check for Comment Editing (Defense-in-Depth)

Compare the comment's `created` and `updated` timestamps. In this scenario, the timestamps are identical, which means the comment has not been edited since it was posted. No warning is necessary.

If `updated` were later than `created`, the skill would warn: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." but would still proceed with the digest comparison.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Full tagged digest**: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Format tag**: `md` (indicating the digest was computed from a markdown representation)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The digest uses the modern format-tagged format (`sha256-md:...`), not the legacy untagged format (`sha256:...`), so no legacy warning is needed.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (as fetched in Step 1). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description was retrieved via MCP (which returns markdown), the script outputs a tagged digest in the format `sha256-md:<64-char-hex>`.

If the script exits non-zero, the skill would warn and skip the integrity check without blocking execution.

### 6. Compare Format Tags

Compare the format tag from the stored digest (`md`) with the format tag from the computed digest (`md`).

In this scenario, both tags are `md`, so they match. The skill proceeds to hex digest comparison.

If the tags differed (e.g., stored was `sha256-adf` but computed was `sha256-md`), the skill would log a warning: "Digest format mismatch (stored: adf, current: md) -- producer and consumer used different API access methods. Skipping integrity check." and proceed normally without blocking.

### 7. Compare Hex Digests

Compare the hex digest from the stored comment with the hex digest computed from the current description.

In this scenario, the digests MATCH (the eval specifies they are identical).

**Result: MATCH -- proceed silently.**

When digests match, the skill proceeds to Step 2 with no user prompt, no warning, and no additional latency. The description is confirmed to be unmodified since plan-feature created it.

## Mismatch Behavior (not triggered in this scenario)

If the digests did NOT match, the skill would:

1. Alert the user that the task description was modified after plan-feature created it
2. Display the expected digest (from the comment) and the actual digest (computed from the current description)
3. Ask the user whether to:
   - **Proceed** with the current description as-is
   - **Stop** so they can re-run plan-feature to regenerate tasks
4. Stop execution immediately until the user responds

## Summary

| Check | Result | Action |
|---|---|---|
| Digest comment found | Yes (1 comment with marker) | Continue verification |
| Comment edited after posting | No (created == updated) | No warning needed |
| Digest format | Modern tagged (`sha256-md:`) | No legacy warning |
| Format tags match | Yes (both `md`) | Proceed to hex comparison |
| Hex digests match | Yes | Proceed silently to Step 2 |
