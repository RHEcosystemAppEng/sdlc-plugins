# Step 1.5 -- Description Integrity Verification for TC-9201

## Context

After fetching TC-9201 in Step 1, Step 1.5 verifies that the task description has not been modified since plan-feature originally created it. This verification follows the Description Digest Protocol defined in `shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search all returned comments for bodies starting with the marker string `[sdlc-workflow] Description digest:`. In this case, one comment matches:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since there is only one matching comment, it is selected directly. (If multiple comments matched, I would select the most recent one by `created` timestamp to handle plan-feature re-runs deterministically.)

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the timestamps are identical, meaning the comment has not been edited after initial posting. No warning is needed -- proceed with digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the current tagged format (not the legacy untagged `sha256:<hex>` format), so no legacy-format warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text fetched via `jira.get_issue`). Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is markdown text (fetched via MCP or stored as plain text), the script outputs a tagged digest in the form `sha256-md:<64-char-hex>`.

If the script exits non-zero, I would warn and skip the integrity check without blocking execution.

### 6. Compare format tags

The stored tag is `sha256-md` and the computed tag is also `sha256-md`. The tags match, so I proceed to hex digest comparison. (If the tags differed -- e.g., stored `sha256-adf` vs. computed `sha256-md` -- I would log a warning about different API access methods and skip the integrity check without blocking.)

### 7. Compare hex digests -- MISMATCH

The stored hex digest (`0000000000000000000000000000000000000000000000000000000000000000`) does not match the hex digest computed from the current description. This means the task description was modified after plan-feature created it.

### 8. Alert the user and halt execution

I would present the following alert to the user:

> **Description integrity check failed for TC-9201.**
>
> The task description has been modified since plan-feature created it.
>
> - **Expected digest** (from plan-feature comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from current description): `sha256-md:<actual-computed-64-char-hex>`
>
> This means someone (or a process) edited the Jira task description after plan-feature generated it. The implementation may not match the original plan.
>
> How would you like to proceed?
>
> 1. **Proceed** -- implement the task using the current (modified) description as-is
> 2. **Stop** -- halt so you can re-run plan-feature to regenerate tasks with a fresh plan

**Execution stops immediately at this point.** No subsequent steps (Step 2 through Step 11) are executed until the user responds. This is a hard stop -- I do not proceed with dependency verification, branch creation, code changes, or any other action.

### 9. Outcome based on user response

- **If the user chooses "Proceed"**: I continue with Step 2 (Verify Dependencies) using the current description content as the specification. The mismatch is acknowledged but does not block further work.
- **If the user chooses "Stop"**: I halt execution entirely. The user would then re-run plan-feature to regenerate the task descriptions, which would post a new digest comment with an updated hash matching the new description. After re-planning, implement-task can be invoked again and the digest check would pass.

## Key protocol details applied

- **Marker string is fixed**: `[sdlc-workflow] Description digest:` -- used exactly as specified, no variation.
- **Most-recent comment selection**: If multiple digest comments existed, I would pick the one with the latest `created` timestamp.
- **Legacy format handling**: If the digest used the untagged format `sha256:<hex>`, I would log a warning and skip the integrity check (proceed normally).
- **Format tag comparison before hex comparison**: Tags must match before comparing hex values. Different tags indicate different API access methods and make comparison meaningless.
- **Comment edit detection**: Checked `created` vs `updated` timestamps. If they differed, I would warn about reduced integrity guarantees but still proceed with digest comparison.
- **Non-blocking on infrastructure errors**: If `scripts/sha256-digest.py` exits non-zero, I warn and skip the check rather than blocking execution.
- **Hard stop on mismatch**: A hex digest mismatch with matching format tags triggers an immediate halt with user prompt. I do not silently continue.
