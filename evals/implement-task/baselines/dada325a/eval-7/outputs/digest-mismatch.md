# implement-task TC-9201: Step 1.5, Description Integrity Verification

## Steps before 1.5 (summary)

- **Step 0: Validate Project Configuration.** The mock CLAUDE.md (`claude-md-mock.md`) has all three required sections: Repository Registry (trustify-backend / serena_backend / `./`), Jira Configuration (Project key TC, Cloud ID, Feature issue type ID 10142), and Code Intelligence (with the `mcp__<serena-instance>__<tool>` naming convention). Validation passes.
- **Step 0.5: JIRA access.** Use MCP first. Fall back to REST only if MCP fails and the user agrees.
- **Step 1: Fetch and parse TC-9201.** Every required section is present: Repository = `trustify-backend`, Target Branch = `main`, Description, Files to Modify, Files to Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements, and Dependencies (None). There is no Target PR and no Bookend Type, so this is the default flow. I would also capture the `webUrl` and read the GitHub Issue custom field `customfield_10747`, if it is set.

## Step 1.5: Verify Description Integrity

This follows `plugins/sdlc-workflow/shared/description-digest-protocol.md`.

### 1. Retrieve issue comments

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

I search the comments for bodies that start with the fixed marker `[sdlc-workflow] Description digest:`. Exactly one comment matches:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Only one comment matches, so there is no need to pick the most recent by `created` timestamp. A digest comment exists, so the "no digest found" fallback does not apply.

### 3. Check whether the comment was edited (4a)

The comment's `created` and `updated` timestamps are **identical**. That means the comment has not been edited since it was posted, so I raise **no** "Digest comment was edited after initial posting" warning. I then go on to compare the digests.

### 4. Extract the stored digest (4b)

- Stored tagged digest: `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- Format tag: `sha256-md`
- Hex digest: `0000000000000000000000000000000000000000000000000000000000000000` (64 hex characters)
- The digest is tagged, not the legacy `sha256:<hex>` format, so the legacy skip does not apply.

### 5. Compute the current digest (4c)

I take the `description` field from the `jira.get_issue` response, write it to a temp file, and run the script. I would not compute SHA-256 by hand.

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script exits with code 0 and prints a tagged digest of the form `sha256-md:<64-hex>`. The description came through MCP as markdown, so the tag is `md`. For illustration, running the script on the mock description body gave `sha256-md:94a37782f4aff8cdd79954d97a6b804040be27459879b5d3617f8354c85770f7`. In a real run, the value would come from the live Jira description. If the script had exited non-zero, I would warn the user and skip the check without blocking.

### 6. Compare format tags (4d)

The stored tag is `sha256-md` and the computed tag is `sha256-md`. **The tags match**, so the "Digest format mismatch, skipping integrity check" path does not apply, and I compare the hex values directly.

### 7. Compare hex digests (4e): MISMATCH

The hex digests are different. The task description was changed after plan-feature created the task. I do **not** continue silently. I alert the user with this message:

> **Description integrity check failed for TC-9201**
>
> The task description was modified after plan-feature created it.
> The digest recorded at planning time does not match the digest of the current description.
>
> - **Expected digest** (from the plan-feature digest comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from the current description): `sha256-md:94a37782f4aff8cdd79954d97a6b804040be27459879b5d3617f8354c85770f7`
>
> Note: the digest comment itself has not been edited (its `created` and `updated` timestamps are identical). The change is in the task description.
>
> How would you like to proceed?
>
> 1. **Proceed**: implement TC-9201 using the current description as-is.
> 2. **Stop**: halt so you can review the changes and re-run plan-feature to regenerate the tasks.

### 8. Stop and wait for the user

**Execution stops here** until the user answers. Until then I do none of the later steps:

- No dependency verification (Step 2)
- No Jira assignment or transition to In Progress (Step 3)
- No code inspection, branch creation, implementation, tests, commit, PR, or Jira updates (Steps 4–11)

What happens next depends on the answer:

- **1 (Proceed):** continue from Step 2 using the current description as the specification. I would mention in the final Jira comment, under "deviations from the plan", that the user chose to proceed even though the digest did not match.
- **2 (Stop):** end the skill run without changing anything in Jira, git, or the repository, and suggest re-running `/sdlc-workflow:plan-feature` for the parent feature (TC-9001).
