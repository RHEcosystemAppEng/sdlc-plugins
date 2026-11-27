# implement-task TC-9201: Step 1.5 Description Integrity Verification

## Step 0: Validate Project Configuration: PASS

The project CLAUDE.md (`claude-md-mock.md`) has all the required sections under `# Project Configuration`:
- `## Repository Registry`: one entry (trustify-backend, Serena instance `serena_backend`, path `./`)
- `## Jira Configuration`: Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID 10142
- `## Code Intelligence`: includes the tool naming convention `mcp__<serena-instance>__<tool>`

## Step 0.5: Jira Access

The skill would try Atlassian MCP first. It would offer the REST API fallback only if MCP failed. This eval is simulated, so no Jira calls were made. The scenario says the stored digest is `sha256-md`, which means the description was read as markdown (the MCP path). The consumer gets a `sha256-md` digest too, so the format tags match.

## Step 1: Fetch and Parse Jira Task: PASS

`jira.get_issue(TC-9201)` returns a description that follows the template. All required sections are present:
- Repository: `trustify-backend`
- Target Branch: `main`
- Description, Files to Modify, Files to Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies (None): all present
- No Target PR and no Bookend Type, so the mode is **default**

## Step 1.5: Verify Description Integrity

1. **Retrieve comments**: `jira.get_issue_comments(TC-9201)` returns one comment.

2. **Locate the digest comment**: one comment body starts with the marker `[sdlc-workflow] Description digest:`:
   ```
   [sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
   ```
   Only one comment matches, so no tie-break by `created` is needed.

3. **A digest comment exists**, so the "no digest" backward-compatibility path does not apply.

4. **Process the digest comment**:
   - **a. Edit detection**: `created` == `updated`, so the comment has not been edited since it was posted. No "Digest comment was edited after initial posting" warning is shown.
   - **b. Extract the stored digest**: format tag = `sha256-md`, hex = `0000000000000000000000000000000000000000000000000000000000000000`. This is the tagged format, not the legacy untagged `sha256:<hex>`, so the check continues.
   - **c. Compute the current digest**: write the fetched description field to `/tmp/desc-TC-9201.txt` and run:
     ```bash
     python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
     ```
     The script exits 0 and prints a tagged digest. In this simulated run, hashing the task-standard description body gave:
     `sha256-md:94a37782f4aff8cdd79954d97a6b804040be27459879b5d3617f8354c85770f7`
   - **d. Compare format tags**: stored `sha256-md` and computed `sha256-md` match. There is no format mismatch, so the check is not skipped.
   - **e. Compare hex digests**: they **DO NOT MATCH**. The integrity check fails.

### Action: alert the user and stop

The skill does not continue silently. It shows this message to the user:

> **Warning: Task description was modified after plan-feature created it.**
>
> The description of TC-9201 no longer matches the digest recorded by plan-feature.
>
> - **Expected digest** (from the `[sdlc-workflow] Description digest` comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from the current description): `sha256-md:94a37782f4aff8cdd79954d97a6b804040be27459879b5d3617f8354c85770f7`
>
> The format tags match (`sha256-md`) and the digest comment has not been edited (created == updated). So the description itself changed after planning. The change could be a legitimate manual edit, or it could be unauthorized tampering.
>
> How would you like to continue?
> 1. **Proceed** with the current description as-is
> 2. **Stop** so you can review the changes and re-run plan-feature to regenerate the tasks

**Execution stops here until the user responds.** None of the later steps run before the user chooses:
- Step 2: verify dependencies
- Step 3: assign the task and transition it to In Progress
- Step 4 onward: branch creation, code inspection, implementation, tests, commit, PR, Jira updates

Nothing is assigned or transitioned in Jira, no branch is created, and no files are changed.

### What happens after the user responds
- **Proceed (1)**: continue with Step 2 (Dependencies: None, so this passes immediately), then Step 3 and the rest of the default-mode flow. The current description is the source of truth.
- **Stop (2)**: end the skill and make no further changes. The user can review the description history and re-run `/sdlc-workflow:plan-feature` on the parent feature (TC-9001) to regenerate the tasks and a fresh digest.
