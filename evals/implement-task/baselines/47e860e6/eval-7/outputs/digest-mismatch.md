# implement-task TC-9201 — Step 1.5 Description Integrity Verification

## Step 0 – Project Configuration Validation

The project CLAUDE.md (`claude-md-mock.md`) has everything required under `# Project Configuration`:

- **Repository Registry**: 1 entry (`trustify-backend`, Serena instance `serena_backend`, path `./`)
- **Jira Configuration**: Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`, Feature issue type ID `10142`
- **Code Intelligence**: present, with the `mcp__<serena-instance>__<tool>` naming convention

Validation passed, so the skill continues.

## Step 1 – Fetch and Parse Jira Task (simulated)

`jira.get_issue(TC-9201)` returns the task in `task-standard.md`. Every required section is present: Repository (`trustify-backend`), Target Branch (`main`), Description, Files to Modify, Files to Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies (None). The task has no Target PR and no Bookend Type, so the default flow applies. Parsing succeeds with no gaps.

## Step 1.5 – Verify Description Integrity

### 1. Retrieve issue comments

```
jira.get_issue_comments(TC-9201)
```

This returns one comment, posted by an earlier plan-feature run:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

### 2. Locate the digest comment

The comment body starts with the marker `[sdlc-workflow] Description digest:` defined in `shared/description-digest-protocol.md`. Only one comment matches, so it is the digest comment. No choice by most-recent `created` timestamp is needed.

### 3. No-digest fallback

Not applicable, because a digest comment was found. The backward-compatibility warning is not shown.

### 4a. Check for comment editing

The comment's `created` and `updated` timestamps are present and **identical**. The comment has not been edited since it was posted, so **no "Digest comment was edited after initial posting" warning is shown**. The digest comparison continues.

### 4b. Extract the stored digest

- Stored tagged digest: `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- Format tag: `sha256-md`. This is a tagged digest, not the legacy `sha256:<hex>` format, so the legacy skip path does not apply.
- Hex digest: `0000000000000000000000000000000000000000000000000000000000000000` (64 hex chars)

### 4c. Compute the current digest

Write the current description field from the `get_issue` response to a temp file and run the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script exits 0 and prints a tagged digest of the form `sha256-md:<64-char-hex>`. The description came back as markdown text via MCP, so the script detects plain text, strips leading and trailing whitespace, and hashes. Per the eval scenario, the computed hex is **not** all zeros. Below it is called `<computed-hex>`.

### 4d. Compare format tags

- Stored tag: `sha256-md`
- Computed tag: `sha256-md`

The tags **match**, so the format-mismatch skip path ("Digest format mismatch — skipping integrity check") does **not** apply. The hex digests are compared directly.

### 4e. Compare hex digests: MISMATCH

`0000…0000` (stored) != `<computed-hex>` (current). This means the task description was modified after plan-feature created it.

**The skill alerts the user and stops execution immediately.** The message shown is:

> **Description integrity check failed for TC-9201**
>
> The task description was modified after plan-feature created it. The digest computed from the current description does not match the digest that plan-feature recorded.
>
> - **Expected digest** (from the plan-feature digest comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from the current description via `scripts/sha256-digest.py`): `sha256-md:<computed-hex>`
>
> The digest comment has not been edited (`created` == `updated`), so the change is in the description itself.
>
> How would you like to proceed?
>
> 1. **Proceed** with the current description as-is
> 2. **Stop** so you can re-run plan-feature to regenerate tasks
>
> Please choose 1 or 2.

### Execution halted pending user response

Following the skill, **no later steps run** until the user answers. In particular:

- **Step 2** (verify dependencies): not run
- **Step 3** (assign to current user, transition to In Progress): not run. Jira is not changed.
- **Step 4** (code inspection via `serena_backend`): not run
- **Step 5** (`git checkout main && git pull && git checkout -b TC-9201`): not run
- **Steps 6–11** (implement, test, verify, commit, PR, Jira update): not run

The skill does not continue silently, does not assume consent, and does not treat the mismatch as a non-blocking warning. It is a hard pause that needs an explicit user decision.

### What happens after the user responds

- **If the user picks 1 (Proceed)**: continue to Step 2 using the **current** (modified) description as the spec. Optionally note in the final Jira comment (Step 11, under "deviations from the plan") that implementation went ahead despite a description digest mismatch that the user approved.
- **If the user picks 2 (Stop)**: end the skill without changing Jira, git, or the repository. Tell the user to re-run `/sdlc-workflow:plan-feature` for the parent feature (TC-9001) to regenerate the tasks and a fresh digest, then re-run `/sdlc-workflow:implement-task TC-9201`.

## Summary of decision branches in this scenario

| Check | Result | Action |
|---|---|---|
| Digest comment present? | Yes (1 comment) | Use it |
| Multiple digest comments? | No | No timestamp selection needed |
| Comment edited (`updated` > `created`)? | No (identical) | No edit warning |
| Legacy untagged format? | No (`sha256-md`) | Continue |
| Script exit status | 0 | Continue |
| Format tags match? | Yes (`sha256-md` == `sha256-md`) | Compare hex |
| Hex digests match? | **No** | **Alert user with expected and actual digests, offer Proceed/Stop, stop execution** |
