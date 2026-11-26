# implement-task TC-9201: Step 1.5 Description Integrity Verification

## Steps 0 to 1 (prerequisites, short version)

- **Step 0 (Validate Project Configuration):** passed. The mock CLAUDE.md has a Repository Registry (`trustify-backend`, Serena instance `serena_backend`), a Jira Configuration (Project key `TC`, Cloud ID, Feature issue type ID `10142`) and a Code Intelligence section.
- **Step 0.5 (JIRA access):** I would try Atlassian MCP first. Because this is an eval, no real Jira calls are made.
- **Step 1 (Fetch and parse):** I would call `jira.get_issue(TC-9201)`. Every required section is present: Repository, Target Branch (`main`), Description, Files to Modify, Files to Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies (None). There is no Target PR and no Bookend Type. If the GitHub Issue field (`customfield_10747`) has a value, I would extract it. If not, I would skip it without comment.

## Step 1.5: Verify Description Integrity

### 1. Retrieve issue comments

```
jira.get_issue_comments(TC-9201)
```

The response contains one comment:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

### 2. Locate the digest comment

The comment body starts with the marker `[sdlc-workflow] Description digest:`, so it is the digest comment. It is the only match, so I do not need to choose the most recent one by `created` timestamp.

### 3. No-digest fallback

This does not apply, because a digest comment exists.

### 4a. Check whether the comment was edited

The comment's `created` and `updated` timestamps are identical, so it has not been edited since it was posted. I would not show the "Digest comment was edited after initial posting" warning. I would continue to the digest comparison.

### 4b. Extract the stored digest

- Stored tagged digest: `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- Format tag: `sha256-md`
- Hex: `0000000000000000000000000000000000000000000000000000000000000000`
- This is the tagged format, not the legacy `sha256:<hex>` format, so the legacy skip does not apply.

### 4c. Compute the current digest

I would write the description field from the `get_issue` response to a temp file and run the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script exits 0. Its output is a tagged digest of the form `sha256-md:<64-hex>`. MCP returns markdown, so the script detects markdown and uses the `md` tag. For illustration, running the script locally on the mock description body gave:

```
sha256-md:94a37782f4aff8cdd79954d97a6b804040be27459879b5d3617f8354c85770f7
```

The scenario says to assume the computed hex differs from the stored hex. That holds here.

### 4d. Compare format tags

Stored tag `sha256-md` and computed tag `sha256-md` match. There is no format mismatch, so I would not skip the check. I would continue to the hex comparison.

### 4e. Compare hex digests: MISMATCH

The hex digests differ, which means the task description was modified after plan-feature created the task. I would **not** proceed silently. I would show the user this alert:

> **Description integrity check failed for TC-9201**
>
> The task description was modified after plan-feature created it.
>
> - **Expected digest** (from the plan-feature digest comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from the current description): `sha256-md:94a37782f4aff8cdd79954d97a6b804040be27459879b5d3617f8354c85770f7`
> - The digest comment has not been edited (its `created` and `updated` timestamps are identical), so the change is in the description itself.
>
> How would you like to continue?
>
> 1. **Proceed**: implement using the current (modified) description as-is
> 2. **Stop**: halt so you can review the change and re-run `/plan-feature` to regenerate tasks
>
> Please choose (1/2).

### Stop execution

I would **stop immediately** after asking and wait for the user's reply. Until the user answers, none of the later steps run:

- no dependency check (Step 2)
- no assignment and no transition to In Progress (Step 3)
- no code analysis through `serena_backend` (Step 4)
- no `git checkout -b TC-9201` (Step 5)
- no implementation, tests, commits, PR or Jira updates (Steps 6 to 11)

No Jira comment is posted at this point. The integrity alert goes only to the user in the session.

### What happens after the user answers

- **User picks 1 (Proceed):** continue with Step 2 using the current description as the specification. I would record the integrity-check override in the Step 11 Jira comment under "deviations from the plan", and the comment would end with the standard `sdlc-workflow/implement-task` footnote.
- **User picks 2 (Stop):** end the skill run. I would make no Jira transitions and no repository changes, and I would suggest re-running `/plan-feature` for the parent feature (TC-9001) to regenerate the task and a fresh digest.
