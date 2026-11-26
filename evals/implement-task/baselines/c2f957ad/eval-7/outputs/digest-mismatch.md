# implement-task TC-9201 — Step 1.5 Description Integrity Verification

## Steps completed before Step 1.5

### Step 0 – Validate Project Configuration
The project CLAUDE.md (claude-md-mock.md) contains everything this step requires:
- `## Repository Registry`: one entry (`trustify-backend`, Serena instance `serena_backend`, path `./`)
- `## Jira Configuration`: Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`, Feature issue type ID `10142`
- `## Code Intelligence`: present, with the `mcp__<serena-instance>__<tool>` naming convention

Result: passed. Execution continues.

### Step 0.5 – JIRA Access Initialization
Atlassian MCP would be tried first, with the REST fallback prompt shown only if MCP fails. Because MCP returns the description as markdown, the computed digest would use the `sha256-md` format. That is the same format tag as the stored digest.

### Step 1 – Fetch and Parse Jira Task
Called `jira.get_issue(TC-9201)` (simulated here with task-standard.md). Every required section is present:
- Repository: `trustify-backend`
- Target Branch: `main`
- Description, Files to Modify, Files to Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies (None)
- No Target PR, Review Context or Bookend Type, so this is the default flow.
- GitHub Issue custom field `customfield_10747` is configured. Its value would be read from the issue. If the field is empty, this is skipped silently.

Result: the description is structurally complete. Execution continues to Step 1.5.

## Step 1.5 – Verify Description Integrity

1. **Retrieve issue comments**: `jira.get_issue_comments(TC-9201)` returns one comment:
   `[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000`

2. **Locate the digest comment**: the comment body starts with the marker `[sdlc-workflow] Description digest:`. It is the only match, so there is no need to choose the most recent by `created` timestamp.

3. **No-digest fallback**: does not apply, because a digest comment was found.

4. **Digest comment found**:
   a. **Comment edit check**: the `created` and `updated` timestamps are identical. The comment was not edited after it was posted, so no "Digest comment was edited after initial posting" warning is shown.
   b. **Extract stored digest**: format tag `sha256-md`, hex `0000000000000000000000000000000000000000000000000000000000000000` (64 characters). This is a tagged digest, not the legacy `sha256:<hex>` format, so the legacy skip does not apply.
   c. **Compute the current digest**: write the description field to `/tmp/desc-TC-9201.txt` and run:
      ```bash
      python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
      ```
      The script exits 0 and prints a `sha256-md:<hex>` digest. As the eval scenario states, this hex differs from the stored hex. (For illustration, running the script locally on the task-standard.md description body gave `sha256-md:94a37782f4aff8cdd79954d97a6b804040be27459879b5d3617f8354c85770f7`.)
   d. **Compare format tags**: stored `sha256-md` and computed `sha256-md` match. This is not a format mismatch, so the check is not skipped. Go on to compare the hex values.
   e. **Compare hex digests**: they differ. **This is a mismatch.** The description was changed after plan-feature created it.

### Message shown to the user

> **Warning: task description integrity check failed for TC-9201**
>
> The description of TC-9201 was modified after plan-feature created it. The digest stored by plan-feature does not match the digest of the current description.
>
> - **Expected digest** (from the plan-feature comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from the current description): `sha256-md:<computed-hex>` (for example `sha256-md:94a37782f4aff8cdd79954d97a6b804040be27459879b5d3617f8354c85770f7`)
>
> Both digests use the same format (`sha256-md`), and the digest comment has not been edited (its `created` and `updated` timestamps match). So the difference comes from a change to the description itself, not from different API access methods.
>
> How would you like to proceed?
> 1. **Proceed**: implement TC-9201 using the current description as it is.
> 2. **Stop**: halt now so you can review the changes and re-run `/plan-feature` to regenerate the tasks.

### Execution halts here

**Execution stops immediately and waits for the user's answer.** None of the later steps run until the user chooses:
- No Step 2 (dependency verification)
- No Step 3: TC-9201 is not assigned and not transitioned to In Progress
- No Step 4: no Serena or code inspection
- No Step 5: no branch is created
- No Steps 6–11: no code changes, tests, commits, PR or Jira updates

The skill does not continue silently and does not pick an option for the user.

### What happens after the user answers
- **Proceed**: continue from Step 2 with the current description as the specification. Mention in the Step 11 Jira comment that the user chose to proceed despite the integrity-check mismatch.
- **Stop**: end the skill. The user can re-run plan-feature to regenerate the tasks and a new digest comment, then re-run `/implement-task TC-9201`.
