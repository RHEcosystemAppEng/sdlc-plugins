# implement-task TC-9201 — Step 1.5 Description Integrity Verification

## Step 0 – Project Configuration (passed)

The project CLAUDE.md (`claude-md-mock.md`) has all the required sections:
- `## Repository Registry`: trustify-backend, Serena instance `serena_backend`, path `./`
- `## Jira Configuration`: Project key TC, Cloud ID, Feature issue type ID 10142
- `## Code Intelligence`: has the `mcp__<serena-instance>__<tool>` naming convention

## Step 1 – Fetch and Parse (passed)

`jira.get_issue(TC-9201)` returns a description with every required section: Repository
(trustify-backend), Target Branch (main), Description, Files to Modify, Files to Create,
API Changes, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies
(None). There is no Target PR and no Bookend Type, so the default flow applies.

## Step 1.5 – Verify Description Integrity

### 1. Retrieve issue comments

```
jira.get_issue_comments(TC-9201)
```

The call returns one comment:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

### 2. Locate the digest comment

The comment body starts with the marker `[sdlc-workflow] Description digest:`, which is
defined in `shared/description-digest-protocol.md`. It is the only matching comment, so I
select it. No tie-break by `created` timestamp is needed.

### 3. Missing-digest path

Not taken, because a digest comment exists.

### 4a. Check for comment editing

The comment's `created` and `updated` timestamps are identical. This means the comment has
not been edited since it was posted, so I raise **no** "Digest comment was edited after
initial posting" warning. I go on to compare the digests.

### 4b. Extract the stored digest

- Tagged value: `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- Format tag: `sha256-md` (tagged, not the legacy untagged `sha256:` format, so the integrity check goes ahead)
- Hex digest: `0000000000000000000000000000000000000000000000000000000000000000`

### 4c. Compute the current digest

I write the current description field from the `get_issue` response to a temp file and
hash it with the script. I do not compute SHA-256 by hand.

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script exits 0 and prints a tagged digest of the form `sha256-md:<64-hex>`. For
example, running it locally on the description sections of the mock gave
`sha256-md:94a37782f4aff8cdd79954d97a6b804040be27459879b5d3617f8354c85770f7`.

### 4d. Compare format tags

Stored tag `sha256-md` matches computed tag `sha256-md`. Both sides used the same
description representation (markdown), so there is no format-mismatch skip. I compare the
hex digests.

### 4e. Compare hex digests: MISMATCH

The hex digests differ. The task description was modified after plan-feature created it.
This is the alert I show the user:

---

> **Description integrity check failed for TC-9201**
>
> The task description was modified after plan-feature created it. The digest recorded
> when the task was created does not match the digest of the current description.
>
> - **Expected digest** (from the plan-feature digest comment):
>   `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from the current description with `scripts/sha256-digest.py`):
>   `sha256-md:94a37782f4aff8cdd79954d97a6b804040be27459879b5d3617f8354c85770f7`
>
> The format tags match (`sha256-md`) and the digest comment has not been edited
> (`created` == `updated`). The difference therefore comes from a change to the
> description itself.
>
> How would you like to proceed?
>
> 1. **Proceed**: implement TC-9201 using the current description as-is
> 2. **Stop**: halt so you can review the change and re-run `/plan-feature` to regenerate the tasks
>
> Please choose (1/2).

---

### Execution halts here

**Execution stops immediately** until the user responds. None of the later steps run:
- Step 2 (verify dependencies): not run
- Step 3 (assign to current user / transition to In Progress): not run. The Jira issue stays unchanged in "To Do".
- Step 4 (Serena code inspection), Step 5 (create branch `TC-9201` from `main`), Steps 6–11: not run

I do not change any files, run any git commands, or write anything to Jira.

### What happens after the user responds

- **If 1 (Proceed):** continue from Step 2, treating the current Jira description as the
  authoritative specification. Mentioning the integrity mismatch and the user's decision to
  proceed under "deviations from the plan" in the Step 11 Jira comment would help reviewers.
- **If 2 (Stop):** end the skill run without further action. The user can re-run
  `/plan-feature` to regenerate the tasks along with a fresh digest comment.
