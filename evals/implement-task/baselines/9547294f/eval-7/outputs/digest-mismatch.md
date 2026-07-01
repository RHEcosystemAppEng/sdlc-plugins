# Step 1.5 — Description Integrity Verification for TC-9201

## Overview

This document describes exactly how the implement-task skill would handle Step 1.5 (Verify Description Integrity) for task TC-9201 given the scenario conditions.

## Step-by-Step Execution

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

This returns the list of comments on the issue.

### 2. Locate the digest comment

Search through all returned comments for those whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

In this scenario, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

If multiple comments matched the marker, the skill would select the most recent one by `created` timestamp. In this case, only one comment matches.

### 3. Check for comment editing (Comment Edit Detection)

The skill compares the comment's `created` and `updated` timestamps. In this scenario, the `created` and `updated` timestamps are identical. This means the comment has not been edited after initial posting — it is unmodified. The skill proceeds with digest comparison without any edit warning.

If `updated` had been later than `created`, the skill would have warned: "Digest comment was edited after initial posting — integrity cannot be fully guaranteed." and still proceeded with the comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Full tagged digest**: `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Format tag**: `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

The format tag is not the legacy untagged format (`sha256:<hex>`), so no legacy warning is needed. The skill proceeds with the full comparison.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (fetched in Step 1). Write the description content to a temporary file:

```bash
# Write the current description to a temp file
cat > /tmp/desc-TC-9201.txt << 'EOF'
<current description content from the Jira API response>
EOF
```

Then compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description was fetched via the same API method (MCP returns markdown), the script outputs a tagged digest in the form:

```
sha256-md:<computed-64-char-hex-digest>
```

If the script exits non-zero, the skill would warn and skip the integrity check without blocking execution. In this scenario, assume it exits successfully.

### 6. Compare format tags

- **Stored tag**: `sha256-md`
- **Computed tag**: `sha256-md`

The format tags match. Both the producer (plan-feature) and consumer (implement-task) used the same API access method, so the hashes are directly comparable. The skill proceeds to hex digest comparison.

If the tags had differed (e.g., stored was `sha256-adf` but computed was `sha256-md`), the skill would log a warning: "Digest format mismatch (stored: `sha256-adf`, current: `sha256-md`) — producer and consumer used different API access methods. Skipping integrity check." and proceed normally without blocking.

### 7. Compare hex digests — MISMATCH DETECTED

- **Expected digest** (from comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual digest** (computed from current description): `sha256-md:<different-64-char-hex-value>`

The hex digests do not match. This means the task description was modified after plan-feature created it.

### 8. Alert the user and stop execution

The skill presents the following alert to the user:

> **Warning: Task description modified after planning**
>
> The description of TC-9201 has been modified since plan-feature created it. The description integrity check detected a digest mismatch.
>
> - **Expected digest** (recorded by plan-feature): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from current description): `sha256-md:<computed-hex-digest>`
>
> The description may have been manually edited in Jira after the planning phase.
>
> How would you like to proceed?
>
> 1. **Proceed** — continue implementation using the current (modified) description as-is
> 2. **Stop** — abort so you can re-run plan-feature to regenerate tasks with a fresh plan
>
> Please choose (1/2):

**Execution stops immediately.** The skill does not proceed with any subsequent steps (Step 2 through Step 11) — no dependency verification, no branch creation, no code changes, no Jira transitions — until the user responds.

## User Response Handling

- **If the user chooses "Proceed" (option 1):** The skill continues with Step 2 (Verify Dependencies) using the current description as the implementation specification. The modified description is treated as the authoritative source for the remainder of the implementation.

- **If the user chooses "Stop" (option 2):** The skill halts entirely. No further steps are executed. The user is expected to re-run plan-feature to regenerate tasks that reflect the current state of the feature plan, then re-invoke implement-task on the newly created task.

## Key Behaviors

- The digest comparison is **not** a blocking gate when no digest is found — missing digests produce only a warning, for backward compatibility with tasks created before the digest protocol was introduced.
- The digest comparison **is** a blocking gate when a mismatch is detected — the skill stops and requires user input before proceeding.
- The comment edit detection (created vs. updated timestamps) is a defense-in-depth measure. In this scenario it passes cleanly (timestamps are identical), but even if it had flagged an edit, the skill would still proceed with the digest comparison.
- Legacy untagged digests (format `sha256:<hex>`) would be skipped with a warning rather than compared, since the format tag is needed to ensure the same representation is hashed.
- Format tag mismatches between stored and computed digests are skipped with a warning, since different API access methods produce different representations that hash differently.
