# Step 1.5 – Description Integrity Verification for TC-9201

Protocol reference: `plugins/sdlc-workflow/shared/description-digest-protocol.md`
Skill reference: `plugins/sdlc-workflow/skills/implement-task/SKILL.md`, Step 1.5

## Preconditions (Steps 0, 0.5 and 1)

- **Step 0:** The project CLAUDE.md (`claude-md-mock.md`) has all three required sections under `# Project Configuration`:
  - Repository Registry: `trustify-backend` / `serena_backend` / `./`
  - Jira Configuration: Project key TC, Cloud ID, Feature issue type ID 10142
  - Code Intelligence: includes the `mcp__<serena-instance>__<tool>` naming convention

  Validation passes.
- **Step 0.5:** Jira operations would go through Atlassian MCP first. The REST fallback would only be offered if MCP failed. For this eval, no Jira call is made.
- **Step 1:** `jira.get_issue(TC-9201)` returns a structured description. Every required section is present: Repository, Target Branch, Description, Files to Modify, Files to Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements and Dependencies. There is no Target PR and no Bookend Type, so the default flow applies. The skill would also capture `webUrl` and read the GitHub Issue custom field (`customfield_10747`). If that field is empty, the skill skips it without comment.

## Step 1.5 walk-through

### 1. Retrieve issue comments

```
jira.get_issue_comments(TC-9201)
```

This returns one comment:

```
[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 2. Locate the digest comment

The comment body starts with the fixed marker `[sdlc-workflow] Description digest:`, so it is a digest comment. It is the only match, so no tie-break by `created` timestamp is needed. With several matches, the skill would pick the one with the latest `created` time.

### 3. No-digest branch

Not taken, because a digest comment exists. The "No description digest found" warning is not logged.

### 4a. Comment edit detection

The comment's `created` and `updated` timestamps are present and identical, so the comment has not been edited since it was posted. The skill issues **no** "Digest comment was edited after initial posting" warning.

### 4b. Extract the stored digest

- Tagged value: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Format tag: `sha256-md`, meaning the markdown/MCP representation was hashed
- Hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`, which is 64 lowercase hex characters

This is the tagged format, not the legacy untagged `sha256:<hex>` format, so the legacy-skip branch is not taken.

### 4c. Compute the current digest

The skill would write the description field from the `get_issue` response to a temp file and hash it with the script. It would not compute SHA-256 by hand.

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects plain text (markdown), strips leading and trailing whitespace, and prints a tagged digest. The skill checks the exit code first. A non-zero exit would mean "warn and skip the integrity check, do not block", but in this scenario the script exits 0.

Per the eval premise, the script outputs:

```
sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
```

### 4d. Compare format tags

Both the stored and computed tags are `sha256-md`. Tags match, so there is no "Digest format mismatch" warning, and the skill goes on to compare the hex digests.

### 4e. Compare hex digests

| | Value |
|---|---|
| Stored (comment) | `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890` |
| Computed (current description) | `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890` |
| Result | **MATCH** |

## Outcome

The digests match, so the description has not changed since plan-feature created it. The skill **proceeds silently**:

- No prompt to the user. The proceed/stop question is only asked on a mismatch.
- No warnings: no missing digest, legacy format, format mismatch or edited comment.
- No added latency or confirmation step. Execution continues straight to **Step 2 – Verify Dependencies**.
- No Jira comment is posted about the integrity check.

Step 2 follows. TC-9201 lists "Depends on: None", so no dependency issues need fetching. Step 3 then assigns the issue to the current user and transitions it to In Progress. The rest of the plan is in `plan.md`.
