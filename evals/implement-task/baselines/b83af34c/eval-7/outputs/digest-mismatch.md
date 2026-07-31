# Step 1.5 — Description Integrity Verification for TC-9201

## Scenario

The Jira issue TC-9201 has one comment posted by a previous plan-feature run with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

The format tag is `sha256-md` and the hex hash is `0000000000000000000000000000000000000000000000000000000000000000`. The comment's `created` and `updated` timestamps are identical, meaning the comment was not edited after posting.

## Verification Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search the returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:`. In this scenario, exactly one comment matches. If multiple had matched, the most recent by `created` timestamp would be selected.

### 3. Check for comment editing

Compare the comment's `created` and `updated` timestamps. In this scenario they are identical, so the comment is unmodified. No warning is emitted. Proceed to digest comparison.

### 4. Extract the stored digest

Parse the tagged digest from the comment body:

- **Full tagged value:** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The format uses the `sha256-md` tag (not the legacy untagged `sha256:<hex>` format), so we proceed with the full comparison rather than skipping with a legacy-format warning.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text of the task description), write it to a temp file, and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the format (markdown text in this case) and outputs a tagged digest, for example:

```
sha256-md:a3f8b7c2e1d9045f6b8a2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f
```

(The exact hex value would depend on the actual description content; the key point is that it will differ from the stored hash.)

### 6. Compare format tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match. Both the producer (plan-feature) and consumer (implement-task) used the same API access method (both markdown). Proceed to hex digest comparison.

### 7. Compare hex digests

- **Expected (from comment):** `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `a3f8b7c2e1d9045f6b8a2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f` (example)

**MISMATCH DETECTED.** The hex digests differ, which means the task description was modified after plan-feature originally created it.

### 8. Alert the user and stop execution

The skill alerts the user with the following message:

---

> **Warning: Task description integrity check failed.**
>
> The description of TC-9201 has been modified since plan-feature created it.
>
> - **Expected digest (from plan-feature comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest (computed from current description):** `sha256-md:a3f8b7c2e1d9045f6b8a2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f`
>
> The description was changed after planning. This means the implementation requirements may no longer match what was originally planned.
>
> **How would you like to proceed?**
>
> 1. **Proceed** — implement the task using the current (modified) description as-is
> 2. **Stop** — halt implementation so you can re-run plan-feature to regenerate tasks with an updated plan
>
> Please choose (1 or 2):

---

### 9. Stop execution — do NOT proceed to Step 2

Execution halts immediately at this point. The skill does NOT proceed to Step 2 (Verify Dependencies), Step 3, or any subsequent step. No branch is created, no code is read, no implementation begins.

The skill waits for the user's explicit response before taking any further action:

- **If the user chooses 1 (Proceed):** The skill continues to Step 2 using the current task description, accepting the modified content as the implementation specification.
- **If the user chooses 2 (Stop):** The skill terminates. The user is expected to re-run plan-feature to regenerate a consistent set of tasks, which will post a new digest comment reflecting the updated description.
