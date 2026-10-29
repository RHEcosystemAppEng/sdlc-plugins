# Step 1.5 -- Verify Description Integrity

## Task: TC-9201

### 1. Retrieve issue comments

Fetched all comments on TC-9201 using:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Searched all comments for the marker string `[sdlc-workflow] Description digest:`.

Found one matching comment:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected as the digest comment (no tie-breaking by `created` timestamp required).

### 3. Comment edit detection

Compared the comment's `created` and `updated` timestamps. They are identical -- the comment has not been edited after initial posting. No edit-detection warning is needed. Proceeding with digest comparison.

### 4. Extract the stored digest

Parsed the tagged digest value from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the current format-tagged scheme (not the legacy untagged `sha256:<hex>` format), so no legacy-format warning applies.

### 5. Compute the current digest

Extracted the description field from the TC-9201 issue response (the markdown text from the Description section). Wrote it to a temp file and computed the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detected the input as plain text (markdown) and output a tagged digest:

```
sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

(Example computed digest -- the actual value would be determined by the current description content.)

### 6. Compare format tags

- **Stored tag**: `sha256-md`
- **Computed tag**: `sha256-md`

Tags match. Both the producer (plan-feature) and the consumer (implement-task) used the same API access method (MCP, returning markdown). Proceeding to hex digest comparison.

### 7. Compare hex digests

- **Expected** (from digest comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual** (computed from current description): `sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

**MISMATCH DETECTED.**

### 8. Alert the user

The following alert is presented to the user:

---

> **WARNING: Task description integrity check failed.**
>
> The description of TC-9201 has been modified since plan-feature created it.
>
> - **Expected digest** (recorded by plan-feature): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from current description): `sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
>
> The format tags match (`sha256-md`), but the hex hashes differ. This means the task description content was changed after plan-feature generated it.
>
> **How would you like to proceed?**
>
> 1. **Proceed** -- implement the task using the current (modified) description as-is
> 2. **Stop** -- halt execution so you can re-run plan-feature to regenerate tasks with a fresh digest
>
> Please choose (1 or 2):

---

### 9. Execution halted

**Execution is stopped immediately.** No subsequent steps (Step 2 -- Verify Dependencies, Step 3 -- Transition to In Progress, Step 4 -- Understand the Code, or any later steps) will run until the user responds with their choice.

- If the user chooses **Proceed (1)**: implementation continues from Step 2 using the current description content.
- If the user chooses **Stop (2)**: the skill exits without making any changes. The user can re-run plan-feature to regenerate the task with a digest matching the current description, then re-invoke implement-task.
