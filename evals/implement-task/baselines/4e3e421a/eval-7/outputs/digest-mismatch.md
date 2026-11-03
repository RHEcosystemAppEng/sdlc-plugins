# implement-task TC-9201: Step 1.5 Description Integrity Check

## Preceding steps (summary)

- **Step 0 – Validate Project Configuration:** The project CLAUDE.md has `## Repository Registry` (trustify-backend, Serena instance `serena_backend`), `## Jira Configuration` (Project key TC, Cloud ID, Feature issue type ID 10142) and `## Code Intelligence` (`mcp__<serena-instance>__<tool>` naming convention). Validation passes.
- **Step 0.5 – JIRA Access:** MCP is the preferred method. It is simulated here, and no external calls are made.
- **Step 1 – Fetch and Parse:** `jira.get_issue(TC-9201)` returns a description that contains every required section: Repository (`trustify-backend`), Target Branch (`main`), Description, Files to Modify, Files to Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements and Dependencies (`None`). There is no Target PR and no Bookend Type. The GitHub Issue custom field (`customfield_10747`) is configured. It would be read if present and skipped silently if empty.

## Step 1.5 – Verify Description Integrity

### 1. Retrieve issue comments

```
jira.get_issue_comments(TC-9201)
```

The response contains one comment.

### 2. Locate the digest comment

I search for comments whose body starts with the fixed marker `[sdlc-workflow] Description digest:`. Exactly one comment matches:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Because only one comment matches, I don't need to pick the most recent one by `created`.

### 3. No-digest fallback

This does not apply, because a digest comment exists.

### 4. Digest comment found

**a. Check whether the comment was edited.** The comment's `created` and `updated` timestamps are identical, so it has not been edited since it was posted. I raise no comment-edit warning and go on to the digest comparison.

**b. Extract the stored digest.**
- Format tag: `sha256-md`
- Hex digest: `0000000000000000000000000000000000000000000000000000000000000000` (64 hex chars)
- The digest is tagged rather than in the legacy `sha256:<hex>` format, so the legacy skip path does not apply.

**c. Compute the current digest.** I take the description field from the `get_issue` response, write it to a temp file and run:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script exits with code 0. The description is markdown from the MCP path, so the script detects that format and outputs a `sha256-md:<64-hex>` digest that is **not** all zeros. In this scenario the computed hex differs from the stored hex.

**d. Compare format tags.** The stored tag is `sha256-md` and the computed tag is `sha256-md`. **The tags match**, so the format-mismatch skip path does not apply. Both sides hashed the same representation, so a hex difference here is a real content change and not an artifact of different access methods.

**e. Compare hex digests.** They are different. **This is a MISMATCH.**

### Action: alert the user and stop

I would show the user this message:

> **Description integrity check failed for TC-9201**
>
> The task description was modified after plan-feature created it. The digest recorded at creation time doesn't match a digest of the current description.
>
> - **Expected digest** (from the plan-feature digest comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed now from the current description with `scripts/sha256-digest.py`): `sha256-md:<computed 64-char hex>`
>
> The digest comment has not been edited (its `created` and `updated` timestamps are the same). That means the change is in the task description, not in the recorded digest.
>
> How do you want to continue?
> 1. **Proceed** and implement the task using the current description as it is
> 2. **Stop** so you can re-run plan-feature and regenerate the tasks
>
> Please choose 1 or 2.

**Execution stops immediately here.** Until the user responds, I would **not**:
- go to Step 2 (Verify Dependencies)
- assign the issue or transition it to In Progress (Step 3)
- inspect the code with Serena (Step 4), create a branch (Step 5) or make any code changes (Steps 6 onward)
- post any Jira comment or transition any issue

I would not silently continue, guess which choice the user wants, or treat the mismatch as only a warning.

### What happens after the user responds

- **If the user chooses "Proceed":** Continue to Step 2 and use the **current** description as the specification. Then run the normal flow: dependencies are `None`, so I assign the issue and move it to In Progress, analyze the code with `serena_backend`, create branch `TC-9201` from `main`, and so on. The Step 11 Jira comment would record that the integrity check found a modified description and that the user chose to proceed.
- **If the user chooses "Stop":** End the skill without changing anything in Jira or the repository. The user can re-run `/plan-feature` for the parent feature (TC-9001) to regenerate the tasks and a fresh digest.

## Decision path summary

| Check | Result | Outcome |
|---|---|---|
| Digest comment present? | Yes (1 comment) | Continue with verification |
| Multiple digest comments? | No | Use the single comment |
| Comment edited (`updated` > `created`)? | No (timestamps identical) | No edit warning |
| Legacy untagged format? | No (`sha256-md:` tag) | Continue |
| Script exit code | 0 | Continue |
| Format tags match? | Yes (`sha256-md` == `sha256-md`) | Compare the hex digests |
| Hex digests match? | **No** | **Alert the user, show expected and actual digests, offer Proceed or Stop, and stop until the user responds** |
