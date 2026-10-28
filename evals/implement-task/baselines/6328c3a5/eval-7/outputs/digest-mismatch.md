# Step 1.5 -- Description Integrity Verification for TC-9201

## Context

Task TC-9201 ("Add advisory severity aggregation service and endpoint") has been
fetched and parsed in Step 1. The structured description is complete and all
required sections are present. Step 1.5 now verifies that the description has not
been modified since plan-feature created it, following the protocol defined in
`shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve Issue Comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

The API returns one comment with the following body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

### 2. Locate the Digest Comment

Search all returned comments for bodies starting with the marker string
`[sdlc-workflow] Description digest:`. One comment matches. Since there is only
one matching comment, no tie-breaking by `created` timestamp is needed -- this
comment is selected.

### 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this case the two
timestamps are identical, meaning the comment has not been edited after initial
posting. No edit-detection warning is raised. Proceed with digest comparison.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Full tagged value:** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The format uses the `sha256-md` tag (not the legacy untagged `sha256:<hex>` format),
so the legacy-format bypass does not apply. Proceed with full verification.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (the markdown text
of the task description). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as plain text (markdown) and outputs a tagged
digest. Suppose the output is:

```
sha256-md:a3f7b2c9e1d84f6502ab9c3d7e81f094d6b2e5a1c8f03947d2b6e8a1c5f79024
```

(The exact hex value would be computed from the actual description content. The
key fact is that it differs from the stored value.)

- **Computed format tag:** `sha256-md`
- **Computed hex digest:** `a3f7b2c9e1d84f6502ab9c3d7e81f094d6b2e5a1c8f03947d2b6e8a1c5f79024`

### 6. Compare Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md`. The tags match,
so there is no format mismatch. Both the producer (plan-feature) and consumer
(implement-task) used the same API access method (both markdown). Proceed to hex
digest comparison.

### 7. Compare Hex Digests -- MISMATCH DETECTED

| Field | Value |
|-------|-------|
| **Expected (from digest comment)** | `sha256-md:0000000000000000000000000000000000000000000000000000000000000000` |
| **Actual (computed from current description)** | `sha256-md:a3f7b2c9e1d84f6502ab9c3d7e81f094d6b2e5a1c8f03947d2b6e8a1c5f79024` |

The hex digests do not match. This means the task description was modified after
plan-feature originally created it.

## Action: Alert User and Pause

Per the protocol, the skill must alert the user and stop execution immediately.
The following message would be presented:

---

> **Description integrity check failed for TC-9201.**
>
> The task description has been modified since plan-feature created it.
> The digest recorded at planning time does not match the current description.
>
> - **Expected digest (from plan-feature comment):**
>   `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest (computed from current description):**
>   `sha256-md:a3f7b2c9e1d84f6502ab9c3d7e81f094d6b2e5a1c8f03947d2b6e8a1c5f79024`
>
> This means someone (or an automated process) edited the Jira task description
> after the planning phase completed. The implementation may no longer align with
> the original plan.
>
> How would you like to proceed?
>
> 1. **Proceed** -- implement using the current (modified) description as-is
> 2. **Stop** -- abort so you can re-run plan-feature to regenerate tasks with
>    a consistent plan
>
> Choose (1/2):

---

**Execution halts here.** No subsequent steps (Step 2 -- Verify Dependencies,
Step 3 -- Transition to In Progress, Step 4 -- Understand the Code, etc.) are
executed until the user responds.

- If the user chooses **1 (Proceed)**: the skill continues with Step 2 using the
  current description content, acknowledging the user accepted the modification.
- If the user chooses **2 (Stop)**: the skill terminates immediately. The user
  should re-run plan-feature on the parent feature to regenerate task descriptions
  with fresh digests that reflect the current content.

## Why This Matters

The description digest protocol guards against silent tampering between the
planning and implementation phases. Without this check, a modified description
could cause the implementation to diverge from the approved plan without anyone
noticing. The integrity verification ensures the human operator is aware of any
changes and explicitly approves proceeding with modified requirements.

In this specific case:
- The digest comment was not edited (created == updated), so the stored digest
  is trustworthy as the original value posted by plan-feature.
- The format tags match (both `sha256-md`), so a direct hex comparison is valid.
- The hex hashes differ, confirming the description content changed after planning.
- The skill correctly stops and asks the user rather than silently proceeding with
  potentially inconsistent requirements.
