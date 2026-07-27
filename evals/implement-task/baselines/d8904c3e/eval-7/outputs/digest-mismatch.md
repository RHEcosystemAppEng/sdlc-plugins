# Step 1.5 -- Description Integrity Verification for TC-9201

## Scenario

- Task: TC-9201 (Add advisory severity aggregation service and endpoint)
- A digest comment exists on the Jira issue, posted by a previous plan-feature run.
- Comment body: `[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- The comment's `created` and `updated` timestamps are identical.
- The format tags match (both `sha256-md`), but the hex hashes differ -- the description was modified after plan-feature created it.

## Step-by-Step Handling

### 1. Retrieve Issue Comments

Fetch all comments on TC-9201 using Jira:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the Digest Comment

Search all returned comments for bodies starting with the marker string `[sdlc-workflow] Description digest:`. In this case, one comment matches:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches, it is selected. (If multiple had matched, the most recent by `created` timestamp would be selected.)

### 3. Check for Comment Editing

Compare the comment's `created` and `updated` timestamps. In this scenario they are identical, which means the comment was not edited after initial posting. No warning is emitted for comment tampering -- proceed normally.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the tagged format (not the legacy untagged `sha256:<hex>` format), so no legacy-format warning is needed.

### 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (the markdown text from the Description section). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the format. Since the description is plain markdown text (not ADF JSON), the script outputs:

```
sha256-md:<computed-64-char-hex>
```

The script exits with status 0 (success), so we proceed with comparison.

### 6. Compare Format Tags

- **Stored tag**: `sha256-md`
- **Computed tag**: `sha256-md`

The tags match. This means both the producer (plan-feature) and consumer (implement-task) used the same Jira access method (both received markdown). No format-mismatch warning is needed. Proceed to hex digest comparison.

### 7. Compare Hex Digests

- **Expected (from comment)**: `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description)**: `<different-64-char-hex>` (a different hash computed from the current description content)

**Result: MISMATCH.** The hex digests differ, meaning the task description was modified after plan-feature originally created it.

### 8. Alert the User and Stop

Display the following alert to the user:

> **Warning: Task description modified after planning.**
>
> The description of TC-9201 has been modified since plan-feature created it. The content digest does not match the one recorded at creation time.
>
> - **Expected digest** (from plan-feature comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from current description): `sha256-md:<computed-hex>`
>
> How would you like to proceed?
>
> 1. **Proceed** -- implement using the current (modified) description as-is
> 2. **Stop** -- abort so you can re-run plan-feature to regenerate tasks with a fresh digest

**Execution stops immediately.** No subsequent steps (Step 2 onward -- dependency verification, transitioning to In Progress, branching, implementation, tests, commits, or Jira updates) are performed until the user responds.

- If the user chooses **Proceed** (option 1): continue to Step 2 (Verify Dependencies) using the current task description as the specification.
- If the user chooses **Stop** (option 2): halt execution entirely. The user would then re-run plan-feature on the parent feature to regenerate the task descriptions and digest comments, and then re-invoke implement-task on the refreshed TC-9201.

## Rationale

This verification guards against silent tampering or unintentional drift between the planning and implementation phases. When plan-feature creates a task, it records a cryptographic digest of the description. If someone (or an automated process) later modifies the description -- changing acceptance criteria, file lists, implementation notes, or API contracts -- the digest mismatch catches it before implementation begins. The human operator makes the final decision on whether the modified description is acceptable, preserving human oversight over the specification that drives code generation.
