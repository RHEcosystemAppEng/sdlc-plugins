# Step 1.5 -- Description Integrity Verification for TC-9201

## Context

Task TC-9201 ("Add advisory severity aggregation service and endpoint") has been
fetched from Jira. Before proceeding to dependency verification (Step 2), Step 1.5
requires verifying that the task description has not been modified since plan-feature
originally created it. This verification uses the digest protocol defined in
`shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve Issue Comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the Digest Comment

Search the returned comments for any whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

In this scenario, one matching comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

If multiple comments matched the marker, the most recent one by `created` timestamp
would be selected. Here only one exists, so it is used directly.

### 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the two
timestamps are identical, meaning the comment has not been edited after its initial
posting. No warning is emitted. Proceed to digest comparison.

If `updated` had been later than `created`, a warning would be surfaced:
"Digest comment was edited after initial posting -- integrity cannot be fully
guaranteed." The comparison would still proceed, but the warning would be shown to the
user alongside the result.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Full tagged digest:** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The format is not the legacy untagged format (`sha256:<hex>`), so there is no need
to skip the integrity check on format grounds.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (the full markdown
description text as returned by the Jira API), write it to a temporary file, and
compute its digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description was fetched as
markdown text (via MCP or as plain text from the API), the script produces a tagged
digest in the form:

```
sha256-md:<64-char-hex>
```

For this scenario, assume the script outputs something like:

```
sha256-md:b7e4a3f1c9d8e2b5a0f6c3d9e1b4a7f0c2d5e8b1a4f7c0d3e6b9a2f5c8d1e4a7
```

(The exact hex value would be computed from the actual current description content.)

### 6. Compare Format Tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match. Both the producer (plan-feature) and the consumer
(implement-task) used the same Jira access method, producing the same description
format (markdown). Proceed to hex digest comparison.

If the tags had differed (e.g., stored `sha256-adf` vs. computed `sha256-md`), the
skill would log: "Digest format mismatch (stored: sha256-adf, current: sha256-md) --
producer and consumer used different API access methods. Skipping integrity check."
and proceed normally without blocking.

### 7. Compare Hex Digests -- MISMATCH DETECTED

- **Expected (from comment):** `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `b7e4a3f1c9d8e2b5a0f6c3d9e1b4a7f0c2d5e8b1a4f7c0d3e6b9a2f5c8d1e4a7`

The hex digests do not match. This means the task description was modified after
plan-feature originally created the task and recorded the digest.

### 8. Alert the User and Stop Execution

The skill presents the following alert to the user:

> **Description integrity check failed for TC-9201.**
>
> The task description has been modified since plan-feature created it.
>
> - **Expected digest (from plan-feature comment):**
>   `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest (computed from current description):**
>   `sha256-md:b7e4a3f1c9d8e2b5a0f6c3d9e1b4a7f0c2d5e8b1a4f7c0d3e6b9a2f5c8d1e4a7`
>
> The description was changed after planning. Please choose how to proceed:
>
> 1. **Proceed** -- implement the task using the current (modified) description as-is
> 2. **Stop** -- abort so you can re-run plan-feature to regenerate tasks with a fresh digest
>
> Choose (1/2):

**Execution stops immediately.** No subsequent steps (Step 2 through Step 11) are
executed until the user responds. This is a hard stop -- the skill does not silently
continue with a mismatched description.

### 9. Outcome Based on User Response

- **If the user chooses "Proceed" (option 1):** The skill continues with Step 2
  (Verify Dependencies) using the current task description as the implementation
  specification. The mismatch is noted but does not block further work.

- **If the user chooses "Stop" (option 2):** The skill terminates immediately. The
  user is expected to investigate what changed in the description, potentially re-run
  plan-feature to regenerate the task with an updated digest, and then re-invoke
  implement-task.

## Summary of Checks Performed

| Check | Result | Action |
|---|---|---|
| Digest comment found | Yes (1 comment matches marker) | Proceed to verification |
| Comment edited after posting | No (`created` equals `updated`) | No warning; proceed |
| Digest format (legacy vs tagged) | Tagged (`sha256-md`) | Proceed (not legacy) |
| Format tag comparison | Match (both `sha256-md`) | Proceed to hex comparison |
| Hex digest comparison | **Mismatch** | Alert user; stop execution |

## Rationale

This integrity check guards against silent tampering between the planning and
implementation phases. Without it, a modified description could cause the
implementation to diverge from what was originally planned and approved, without
anyone being aware of the change. The digest protocol provides a cryptographic
guarantee that what plan-feature wrote is exactly what implement-task reads. When
that guarantee is broken, the user must explicitly decide whether the modified
description is acceptable.
