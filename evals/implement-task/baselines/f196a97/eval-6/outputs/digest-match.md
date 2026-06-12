# Description Integrity Verification (Step 1.5) -- Digest Match Case

## Overview

This document describes how the implement-task skill handles the description integrity verification in Step 1.5 for task TC-9201, where the stored digest matches the computed digest.

## Procedure

### 1. Retrieve Issue Comments

After fetching the task in Step 1, retrieve all comments on the Jira issue:

```
jira.get_issue_comments(TC-9201)
```

This returns all comments posted on the issue, including the digest comment posted by plan-feature.

### 2. Locate the Digest Comment

Search through the returned comments for any comment whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

This marker string is defined in `shared/description-digest-protocol.md` and is fixed -- it does not vary per skill or invocation.

In this case, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If multiple comments had matched the marker string (e.g., from plan-feature re-runs), the most recent one by `created` timestamp would be selected. In this scenario, only one comment matches.

### 3. Check for Comment Editing

Compare the comment's `created` and `updated` timestamps. In this scenario, the `created` and `updated` timestamps are identical, which means the comment was not edited after initial posting. No warning is needed -- proceed with digest comparison.

(If `updated` were later than `created`, a warning would be surfaced: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." The digest comparison would still proceed regardless.)

### 4. Parse the Format Tag and Hex Digest

Extract the tagged digest value from the comment body:

- **Full tagged value**: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Format tag**: `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag `sha256-md` indicates the producer (plan-feature) hashed a markdown representation of the description. This is not a legacy untagged format (`sha256:<hex>`), so no legacy warning is needed.

### 5. Compute the Current Digest

Extract the description field from the issue response (as fetched in Step 1). Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs a tagged digest. In this scenario, the script outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The script exits with status 0 (success).

### 6. Compare Format Tags

Compare the format tag from the stored digest (`sha256-md`) with the format tag from the computed digest (`sha256-md`).

**Result**: Tags match -- both are `sha256-md`. This means the producer and consumer used the same Jira access method (both obtained the description as markdown). Proceed to hex digest comparison.

(If the tags had differed -- e.g., stored was `sha256-adf` but computed was `sha256-md` -- a warning would be logged: "Digest format mismatch (stored: sha256-adf, current: sha256-md) -- producer and consumer used different API access methods. Skipping integrity check." Implementation would proceed normally without comparing hex digests.)

### 7. Compare Hex Digests

Compare the hex digests:

- **Stored (from comment)**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed (from current description)**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Result**: Match. The description has not been modified since plan-feature created it.

### 8. Proceed Silently

Since the digests match, proceed silently to Step 2 (Verify Dependencies). This means:

- **No user prompt** -- do not ask the user to confirm or acknowledge the match
- **No pause** -- do not wait for any user input
- **No alert** -- do not display a success message, banner, or notification about the integrity check passing
- **No added latency** -- continue immediately to the next step

The integrity check is transparent when successful. The user is only notified when something is wrong (mismatch, legacy format, format tag mismatch, or edited comment).
