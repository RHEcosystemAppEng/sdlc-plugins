# implement-task TC-9201 — Step 1.5 Description Integrity Verification

## Preceding steps (summary)

- **Step 0 — Project Configuration validation**: The project CLAUDE.md (claude-md-mock.md) has
  `## Repository Registry` (trustify-backend / serena_backend / `./`), `## Jira Configuration`
  (Project key TC, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`, Feature issue type ID 10142),
  and `## Code Intelligence` (naming convention `mcp__<serena-instance>__<tool>`). Validation passes.
- **Step 0.5 — Jira access**: MCP would be tried first. If it failed, I would ask the user whether to use
  the REST API fallback.
- **Step 1 — Fetch and parse**: `jira.get_issue(TC-9201)` returns a full structured description.
  Repository: `trustify-backend`. Target Branch: `main`. Description, Files to Modify, Files to Create,
  API Changes, Implementation Notes, Acceptance Criteria, Test Requirements and Dependencies (None) are
  all present. There is no Target PR and no Bookend Type. No required sections are missing.

## Step 1.5 — Verify Description Integrity

### 1. Retrieve issue comments

```
jira.get_issue_comments(TC-9201)
```

One comment comes back.

### 2. Locate the digest comment

I search for comments whose body starts with the marker `[sdlc-workflow] Description digest:`
(from `shared/description-digest-protocol.md`). One comment matches:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Only one comment matches, so I don't need the "most recent by `created`" rule.

### 3. No-digest fallback

Not applicable. A digest comment exists, so the backward-compatibility warning does not apply.

### 4a. Check whether the comment was edited

The comment's `created` and `updated` timestamps are identical, so it has not been edited since it
was posted. **No edit warning is raised.** I continue to the digest comparison.

### 4b. Extract the stored digest

- Format tag: `sha256-md`
- Hex digest: `0000000000000000000000000000000000000000000000000000000000000000` (64 chars)

This is the tagged format, not the legacy untagged `sha256:<hex>` format, so the legacy skip does not apply.

### 4c. Compute the current digest

I would write the current description field from the `get_issue` response to a temp file and run:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

I would check the exit code. A non-zero exit would mean "warn and skip the integrity check", but
in this scenario the script succeeds. It detects plain markdown, since MCP returns markdown, and
outputs a `sha256-md:<64-hex>` digest. In this scenario that hex value differs from the stored one.
I call it `<computed-hex>` below.

### 4d. Compare format tags

Stored tag `sha256-md` matches computed tag `sha256-md`. There is no format mismatch, so the
"different API access methods, skipping" path does not apply. I compare the hex digests.

### 4e. Compare hex digests: MISMATCH

The hex digests differ. The task description was modified after plan-feature created it. I would
**not** continue silently. I would show this message to the user:

> **Description integrity check failed for TC-9201.**
>
> The task description was modified after plan-feature created it. The digest recorded at
> planning time does not match the digest of the current description.
>
> - **Expected digest** (from the plan-feature comment):
>   `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from the current description with `scripts/sha256-digest.py`):
>   `sha256-md:<computed-hex>`
>
> The digest comment has not been edited (its `created` and `updated` timestamps match). The
> difference is in the description itself, not the recorded digest.
>
> How would you like to proceed?
>
> 1. **Proceed**: implement TC-9201 using the current description as-is.
> 2. **Stop**: halt now so you can review the changes and re-run plan-feature to regenerate the tasks.

### Execution halts here

**Execution stops immediately and waits for the user to answer.** No later steps run:

- No Step 2 (dependency verification)
- No Step 3: TC-9201 is not assigned and not moved to In Progress
- No Step 4 code inspection through `serena_backend`
- No Step 5 branch creation (`git checkout -b TC-9201`)
- No code changes, tests, commits, PRs or Jira updates

### What happens after the user replies

- **If the user chooses "Proceed"**: continue from Step 2 using the current description exactly as fetched.
  Dependencies are "None", so Step 3 runs next (assign to the current user, move to In Progress), and so on.
  In the final Step 11 Jira comment I would list "description changed after planning; user approved
  proceeding" as a deviation from the plan.
- **If the user chooses "Stop"**: end the run with no changes to the repository or Jira. Suggest that
  the user re-run `/sdlc-workflow:plan-feature` for the parent feature (TC-9001) to regenerate the
  task and a fresh digest comment, then re-run `/sdlc-workflow:implement-task TC-9201`.
