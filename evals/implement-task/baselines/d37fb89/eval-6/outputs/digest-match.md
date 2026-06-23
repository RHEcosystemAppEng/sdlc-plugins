# Step 1.5 -- Verify Description Integrity (Digest Match Scenario)

## Overview

This document describes how implement-task handles the description integrity verification in Step 1.5 when the stored digest matches the current description digest.

## Procedure

### 1. Retrieve issue comments

After fetching the task TC-9201 in Step 1, retrieve all comments on the Jira issue:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search through all returned comments for those whose body starts with the marker string `[sdlc-workflow] Description digest:`. This marker is defined in `shared/description-digest-protocol.md` and is fixed across all skills and invocations.

In this scenario, one comment matches:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches the marker, it is selected directly. If multiple comments had matched (e.g., from plan-feature re-runs), the most recent one by `created` timestamp would be selected.

### 3. Check for comment editing

Compare the comment's `created` and `updated` timestamps. In this scenario, the `created` and `updated` timestamps are identical, meaning the comment has not been edited since it was originally posted. No warning is needed -- proceed with digest comparison.

### 4. Parse the format tag and hex digest from the comment

Extract the tagged digest value from the comment body:

- **Full tagged digest:** `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Format tag:** `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format is not the legacy untagged format (`sha256:<hex>`) -- it uses the current format-tagged convention, so no legacy warning is needed.

### 5. Compute the current digest

Extract the description field from the issue response (the markdown text of the task description). Write it to a temporary file and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects that the input is plain text (markdown) and outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

The script exits with status 0, confirming successful computation.

### 6. Compare format tags

The stored format tag is `sha256-md` and the computed format tag is `sha256-md`. The tags match, meaning both the producer (plan-feature) and the consumer (implement-task) used the same Jira access method (both accessed the description as markdown text). Proceed to hex digest comparison.

### 7. Compare hex digests

- **Stored hex digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed hex digest:** `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The hex digests match. The description has not been modified since plan-feature created the task.

### 8. Proceed silently

Per the protocol, when the digests match: proceed silently. There is no user prompt, no alert, no warning, and no added latency. This is the happy path -- the integrity check confirms the description is intact, and execution continues directly to Step 2 (Verify Dependencies) without any interruption or notification to the user.

## Key behaviors for the match scenario

- No user-facing output is produced for the digest verification step
- No confirmation prompt is displayed
- No pause in execution occurs
- The skill proceeds immediately to the next step (Step 2 -- Verify Dependencies)
- The match result is not logged or surfaced unless debug logging is enabled
- This ensures zero added latency on the happy path
