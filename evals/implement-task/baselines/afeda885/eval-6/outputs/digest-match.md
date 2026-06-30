# Description Integrity Verification -- Step 1.5

## Overview

This document describes how Step 1.5 (Verify Description Integrity) is handled for task TC-9201, given that a matching digest comment exists on the Jira issue.

## Procedure

### 1. Retrieve Issue Comments

After fetching the task in Step 1, retrieve all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the Digest Comment

Search all returned comments for those whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

One comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches, it is selected directly. If multiple comments matched, the most recent one by `created` timestamp would be selected.

### 3. Check for Comment Editing

The comment's `created` and `updated` timestamps are compared. In this case, they are identical -- the comment has not been edited since it was posted. No warning is needed; proceed with digest comparison.

If `updated` were later than `created`, a warning would be surfaced: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." But the comparison would still proceed.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

This is not a legacy untagged format (`sha256:<hex>`), so no legacy warning is needed.

### 5. Compute the Current Digest

Extract the description field from the fetched issue response, write it to a temporary file, and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown in this case) and outputs a format-tagged digest. The script's exit code is checked -- if non-zero, we would warn and skip the integrity check. In this scenario, the script succeeds and outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 6. Compare Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md` -- they match. Proceed to hex digest comparison.

If tags differed (e.g., stored `sha256-adf` vs. computed `sha256-md`), a warning would be logged ("Digest format mismatch -- skipping integrity check") and the skill would proceed normally without blocking.

### 7. Compare Hex Digests

- **Stored hex**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed hex**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Result: MATCH.**

### 8. Outcome: Silent Proceed

Per Step 1.5(e) of the SKILL.md: when hex digests match, **proceed silently**. There is:

- No additional user prompt
- No alert or warning message
- No added latency
- No confirmation requested

The description is verified as unmodified since plan-feature created it. Execution continues directly to Step 2 (Verify Dependencies) with zero interruption.

## Key Point

A digest match is the happy path. The integrity check confirms that the task description has not been tampered with or modified between the planning phase (plan-feature) and the implementation phase (implement-task). Since no discrepancy exists, the skill proceeds without any user interaction, adding no latency to the workflow.
