# Step 1.5 — Description Integrity Verification for TC-9201

## Context

Task TC-9201 ("Add advisory severity aggregation service and endpoint") was fetched
from Jira in Step 1. Step 1.5 requires verifying the description has not been modified
since plan-feature created it, using the digest protocol defined in
`shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search the returned comments for any whose body starts with the marker string
`[sdlc-workflow] Description digest:`. One comment is found:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected (no need to pick the most
recent among multiple candidates).

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the
timestamps are identical, meaning the comment has not been edited after initial
posting. No edit-detection warning is emitted. Proceed with digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the format-tagged scheme (`sha256-md:`), not the legacy untagged
format (`sha256:`). No legacy format warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text
from the Description section). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as plain text (markdown) and outputs a tagged
digest, e.g.:

```
sha256-md:e4a7c1f9b2d6083e5a419f7c3b8d2e6a1f0c9b8d7e6f5a4b3c2d1e0f9a8b7c6d
```

The script exits with status 0, confirming successful computation.

### 6. Compare format tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match. Both the producer (plan-feature) and consumer (implement-task)
used the same Jira access method (both received markdown). Proceed to hex digest
comparison.

### 7. Compare hex digests

- **Expected (from comment):** `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `e4a7c1f9b2d6083e5a419f7c3b8d2e6a1f0c9b8d7e6f5a4b3c2d1e0f9a8b7c6d`

**Result: MISMATCH.** The hex digests differ, indicating the task description was
modified after plan-feature created it.

### 8. Alert the user and halt execution

Per the protocol, a digest mismatch with matching format tags requires alerting the
user and stopping execution immediately. The following message would be displayed:

---

> **Description integrity check failed for TC-9201.**
>
> The task description has been modified since plan-feature created it.
>
> - **Expected digest (from plan-feature comment):**
>   `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest (computed from current description):**
>   `sha256-md:e4a7c1f9b2d6083e5a419f7c3b8d2e6a1f0c9b8d7e6f5a4b3c2d1e0f9a8b7c6d`
>
> The description was changed after planning. This may indicate manual edits,
> re-planning without updating the digest, or unintended modifications.
>
> How would you like to proceed?
>
> 1. **Proceed** — implement the task using the current (modified) description as-is
> 2. **Stop** — halt so you can re-run plan-feature to regenerate tasks with a fresh digest

---

**Execution stops here.** No subsequent steps (Step 2 through Step 11) are executed
until the user responds with their choice.

## Outcome by user choice

- **If the user chooses "Proceed":** Implementation continues with Step 2 (Verify
  Dependencies), using the current description exactly as it appears in Jira. The
  mismatch is acknowledged but not treated as blocking.

- **If the user chooses "Stop":** Execution halts entirely. The user is expected to
  re-run plan-feature to regenerate the task description, which will post a new digest
  comment with the correct hash. After re-planning, implement-task can be re-invoked
  and the digest check will pass.

## Key protocol details applied

1. **No legacy format warning** — the digest uses the modern `sha256-md:` tagged
   format, not the legacy `sha256:` untagged format.
2. **No edit-detection warning** — the comment's `created` and `updated` timestamps
   are identical, confirming the comment itself was not tampered with.
3. **No format mismatch warning** — both stored and computed tags are `sha256-md`,
   meaning both sides used the same API access method (markdown via MCP).
4. **Hard stop on hex mismatch** — the protocol requires stopping execution and
   presenting the user with a binary choice (proceed or stop). The skill does not
   silently continue, does not attempt to diff the descriptions, and does not
   auto-resolve the conflict.
