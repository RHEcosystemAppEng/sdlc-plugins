# Description Integrity Verification -- Step 1.5 for TC-9201

## Overview

Step 1.5 verifies that the Jira task description has not been modified since
plan-feature originally created it. This uses the digest protocol defined in
`shared/description-digest-protocol.md`.

## Procedure Applied to TC-9201

### 1. Retrieve Issue Comments

After fetching and parsing the TC-9201 task in Step 1, retrieve all comments on
the issue:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the Digest Comment

Search the returned comments for any whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

In this scenario, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

Since only one comment matches the marker, it is selected directly. If multiple
comments had matched, the most recent one by `created` timestamp would be
selected.

### 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the
two timestamps are identical, meaning the comment has not been edited since it
was posted. No warning is emitted. Proceed with digest comparison.

If `updated` had been later than `created`, the skill would warn: "Digest
comment was edited after initial posting -- integrity cannot be fully
guaranteed." It would still proceed with the digest comparison.

If timestamps were not available in the API response, this check would be
skipped silently.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag is not the legacy untagged format (`sha256:<hex>`), so no legacy
warning is needed. If it had been the legacy format, the skill would log "Legacy
digest format -- skipping integrity check" and proceed without comparison.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response, write it to a
temporary file, and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description was fetched via
MCP (which returns markdown), the script outputs a tagged digest in `sha256-md`
format.

If the script had exited non-zero, the skill would warn and skip the integrity
check without blocking execution.

### 6. Compare Format Tags

The stored tag is `sha256-md`. The computed tag is also `sha256-md`. The tags
match, so a direct hex digest comparison is valid.

If the tags had differed (e.g., stored `sha256-adf` vs. computed `sha256-md`),
the skill would log: "Digest format mismatch (stored: adf, current: md) --
producer and consumer used different API access methods. Skipping integrity
check." It would proceed normally without blocking.

### 7. Compare Hex Digests

The stored hex digest matches the computed hex digest. Per the protocol:

- **Match**: proceed silently. No user prompt, no warning, no added latency.

The skill moves directly to Step 2 (Verify Dependencies) without any
interruption or message to the user.

## What Would Happen on Mismatch

If the hex digests had not matched, the skill would:

1. Alert the user that the task description was modified after plan-feature
   created it.
2. Display the expected digest (from the comment) and the actual digest
   (computed from the current description).
3. Ask the user whether to:
   - **Proceed** with the current description as-is
   - **Stop** so they can re-run plan-feature to regenerate tasks
4. Stop execution immediately and wait for the user's response before
   continuing to any subsequent step.

## Summary of Decision Tree

```
Fetch comments
  |
  +-- No digest comment found --> warn (backward compat), proceed
  |
  +-- Digest comment found
        |
        +-- Check created vs updated timestamps
        |     +-- Same --> no warning
        |     +-- Different --> warn "edited after posting", continue
        |     +-- Unavailable --> skip silently
        |
        +-- Parse format tag
        |     +-- Legacy untagged (sha256:<hex>) --> warn, skip check, proceed
        |     +-- Tagged (sha256-md or sha256-adf) --> continue
        |
        +-- Compute current digest via scripts/sha256-digest.py
        |     +-- Script fails --> warn, skip check, proceed
        |     +-- Script succeeds --> continue
        |
        +-- Compare format tags
        |     +-- Tags differ --> warn "format mismatch", proceed
        |     +-- Tags match --> compare hex digests
        |
        +-- Compare hex digests
              +-- MATCH --> proceed silently  <-- THIS SCENARIO
              +-- MISMATCH --> alert user, ask proceed/stop, halt
```
