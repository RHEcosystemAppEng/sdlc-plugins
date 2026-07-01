# Step 1.5 -- Description Integrity Verification for TC-9201

## Overview

Step 1.5 verifies that the task description has not been modified since plan-feature
created it. This uses the digest protocol defined in
`plugins/sdlc-workflow/shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve Issue Comments

Fetch all comments on the Jira issue TC-9201:

```
jira.get_issue_comments("TC-9201")
```

This returns all comments on the issue, each with body text, `created` timestamp,
and `updated` timestamp.

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
comments matched, the most recent one by `created` timestamp would be selected
to handle plan-feature re-run scenarios deterministically.

### 3. Check for Comment Editing

Compare the comment's `created` and `updated` timestamps. In this scenario, the
timestamps are identical (created equals updated), which means the comment has not
been edited after initial posting. No warning is needed.

If `updated` were later than `created`, a warning would be surfaced:
"Digest comment was edited after initial posting -- integrity cannot be fully
guaranteed." The digest comparison would still proceed, but the warning would be
shown to the user alongside the result.

If the API response did not include these timestamp fields, the check would be
skipped silently.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Full value**: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- **Format tag**: `md` (indicates the description was hashed as markdown text)
- **Hex digest**: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

The format tag is not `sha256:` (legacy untagged format), so this is a modern
format-tagged digest. No legacy-format warning is needed.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (the markdown text
of the task description). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is markdown text
(obtained via MCP or as plain text), the script outputs:

```
sha256-md:<64-char-hex>
```

Per the eval scenario, the script produces exactly:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

If the script exited non-zero, a warning would be logged and the integrity check
would be skipped without blocking execution.

### 6. Compare Format Tags

- Stored tag: `sha256-md`
- Computed tag: `sha256-md`

The format tags match. Both the producer (plan-feature) and consumer
(implement-task) used the same format (markdown), so the hex digests are directly
comparable.

If the tags differed (e.g., stored was `sha256-adf` but computed was `sha256-md`),
a warning would be logged: "Digest format mismatch (stored: adf, current: md) --
producer and consumer used different API access methods. Skipping integrity check."
Implementation would proceed normally without blocking.

### 7. Compare Hex Digests

- Stored hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Computed hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Result: MATCH**

The digests are identical. The task description has not been modified since
plan-feature created it.

### 8. Outcome: Proceed Silently

Per the SKILL.md specification (Step 1.5, item 4e): when digests match, **proceed
silently** -- no additional user prompt, no added latency. The implementation
continues directly to Step 2 (Verify Dependencies) without any interruption or
confirmation dialog.

This is the optimal path: the integrity check confirms the description is
authentic and unmodified, and the skill moves forward without delay.

## Summary of Decision Points

| Check | Result | Action |
|---|---|---|
| Digest comment found? | Yes (1 comment) | Proceed to extraction |
| Comment edited? | No (created == updated) | No warning needed |
| Legacy format? | No (tagged as sha256-md) | Proceed to comparison |
| Format tags match? | Yes (both sha256-md) | Compare hex digests |
| Hex digests match? | Yes | Proceed silently |
