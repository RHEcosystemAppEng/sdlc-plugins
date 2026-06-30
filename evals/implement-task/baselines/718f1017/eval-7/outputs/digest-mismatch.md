# Step 1.5 — Description Integrity Verification for TC-9201

## Scenario

The Jira issue TC-9201 has one comment posted by a previous plan-feature run with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

The comment's `created` and `updated` timestamps are identical. The digest uses the `sha256-md` format tag. The hex hash does NOT match the digest computed from the current task description.

## How Step 1.5 Would Be Handled

### Sub-step 1: Retrieve issue comments

Fetch all comments on TC-9201 using:

```
jira.get_issue_comments("TC-9201")
```

### Sub-step 2: Locate the digest comment

Search all returned comments for bodies starting with the marker string `[sdlc-workflow] Description digest:`. One matching comment is found. Since there is only one match, no tiebreaking by `created` timestamp is needed — this comment is selected as the digest comment.

### Sub-step 3: Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the two timestamps are identical, meaning the comment has not been edited after initial posting. No warning is emitted. Proceed to digest comparison.

### Sub-step 4: Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the current tagged format (not the legacy untagged `sha256:<hex>` format), so no legacy-format warning is needed.

### Sub-step 5: Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text of the task description). Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as plain text (markdown) and outputs a tagged digest, e.g.:

```
sha256-md:f4e8a1b3c9d7...  (64-character hex digest)
```

### Sub-step 6: Compare format tags

The stored tag is `sha256-md` and the computed tag is also `sha256-md` — the tags match. This means both the producer (plan-feature) and the consumer (implement-task) used the same API access method (MCP, which returns markdown). No format mismatch warning is needed. Proceed to hex digest comparison.

### Sub-step 7: Compare hex digests — MISMATCH

The stored hex digest (`0000000000000000000000000000000000000000000000000000000000000000`) does NOT match the computed hex digest from the current description. This means the task description was modified after plan-feature created it.

**Action taken: alert the user and stop execution.**

The following message would be displayed to the user:

> **Warning: Task description modified after planning.**
>
> The description of TC-9201 has been modified since plan-feature created it. The description integrity check failed.
>
> - **Expected digest** (from plan-feature comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from current description): `sha256-md:<actual-64-char-hex-from-script>`
>
> How would you like to proceed?
>
> 1. **Proceed** with the current description as-is
> 2. **Stop** so you can re-run plan-feature to regenerate tasks
>
> Please choose (1/2):

**Execution is halted immediately.** No subsequent steps (Step 2 through Step 11) are executed until the user responds. This is a hard stop — the skill does not proceed with dependency verification, branch creation, code inspection, implementation, or any other work.

### User response handling

- **If the user chooses "Proceed" (option 1):** Implementation continues with the current (modified) description. Steps 2 through 11 execute normally using the description as it currently exists in Jira, accepting the risk that it may differ from what was originally planned.

- **If the user chooses "Stop" (option 2):** Execution terminates. The user is expected to re-run plan-feature to regenerate the task description and its digest comment, ensuring consistency between the plan and the implementation input.

## Summary of Decision Points

| Check | Result | Action |
|---|---|---|
| Digest comment found? | Yes (1 comment matches marker) | Proceed to verification |
| Legacy format? | No (uses tagged `sha256-md` format) | No legacy warning |
| Comment edited? | No (`created` equals `updated`) | No edit warning |
| Format tags match? | Yes (both `sha256-md`) | Proceed to hex comparison |
| Hex digests match? | No (mismatch) | Alert user, stop execution, await user decision |
