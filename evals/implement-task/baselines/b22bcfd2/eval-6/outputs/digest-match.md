# Step 1.5 -- Description Integrity Verification for TC-9201

## Overview

This document describes how the implement-task skill handles the description integrity verification in Step 1.5 for task TC-9201, given that the stored digest matches the computed digest.

## Procedure

### 1. Retrieve Issue Comments

After fetching and parsing the TC-9201 task description in Step 1, retrieve all comments on the Jira issue:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the Digest Comment

Search all returned comments for those whose body starts with the marker string `[sdlc-workflow] Description digest:`. This marker is defined in `shared/description-digest-protocol.md` and is the fixed prefix used by all digest comments posted by plan-feature.

In this case, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches the marker, it is selected directly. If multiple comments had matched, the most recent one by `created` timestamp would be selected.

### 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this case, the `created` and `updated` timestamps are identical, meaning the comment has not been edited since it was posted. No warning is needed -- proceed with digest comparison.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response, write it to a temporary file, and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text in this case) and outputs a format-tagged digest. The output is:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 6. Compare Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md`. The tags match, so we proceed to hex digest comparison. (If the tags had differed, we would log a warning about format mismatch and skip the integrity check.)

### 7. Compare Hex Digests

- **Stored digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The digests match.

## Outcome

The stored digest from the plan-feature comment matches the digest computed from the current task description. This confirms the description has not been modified since plan-feature created it.

**Action: Proceed silently.** Per Step 1.5 rule 4e of the SKILL.md, when digests match, the skill proceeds silently -- no additional user prompt is displayed, no alert is raised, and no pause in execution occurs. The skill moves directly to Step 2 (Verify Dependencies) without any delay or user interaction related to the integrity check.
