# Step 1.5 -- Verify Description Integrity

## Overview

This document describes how Step 1.5 (Verify Description Integrity) would be handled for task TC-9201, given the scenario where a digest comment exists and the computed digest matches the stored digest.

## Procedure

### 1. Retrieve Issue Comments

After fetching the task in Step 1, retrieve all comments on the Jira issue:

```
jira.get_issue_comments(TC-9201)
```

This returns the list of comments associated with the issue. In this scenario, there is exactly one comment.

### 2. Locate the Digest Comment

Search all returned comments for those whose body starts with the marker string defined in `shared/description-digest-protocol.md`:

```
[sdlc-workflow] Description digest:
```

The single comment on TC-9201 matches this marker. Its full body is:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches, there is no need to apply the "most recent by `created` timestamp" tie-breaking rule from the protocol. This comment is selected as the digest comment.

### 3. Check for Comment Editing

Compare the comment's `created` and `updated` timestamps. In this scenario, the two timestamps are identical, which means the comment has not been edited after its initial posting. No warning is necessary. Proceed with digest comparison.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag is not the legacy untagged format (`sha256:<hex>`), so no legacy-format warning applies. Proceed with normal verification.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (the markdown text of the task description). Write it to a temporary file and compute the digest using the project's script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is markdown text (fetched via MCP, which returns markdown), the script outputs a tagged digest in the format:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If the script were to exit non-zero, we would log a warning and skip the integrity check without blocking execution. In this scenario, it exits successfully.

### 6. Compare Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md`. The tags match, so we proceed to hex digest comparison. No format mismatch warning is needed.

### 7. Compare Hex Digests

- **Stored digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Computed digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The hex digests match.

## Outcome

The digests MATCH. The task description has not been modified since plan-feature created it. Per the protocol specification:

> **Match:** proceed silently -- no additional user prompt, no added latency.

No alert is shown to the user. No pause in execution occurs. No confirmation is requested. The integrity check passes transparently, and execution proceeds directly to Step 2 (Verify Dependencies) without any interruption or user interaction. This is the happy path -- the verification adds zero latency from the user's perspective because it completes silently in the background.
