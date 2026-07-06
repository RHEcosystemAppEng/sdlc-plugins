# Step 1.5 -- Description Integrity Verification for TC-9201

## Overview

After fetching and parsing the TC-9201 task description in Step 1, Step 1.5 verifies
that the description has not been modified since plan-feature originally created it.
This uses the digest protocol defined in `shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search the returned comments for any whose body starts with the marker string
`[sdlc-workflow] Description digest:`. In this case, one comment matches:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected directly (no need to
resolve multiple matches by `created` timestamp).

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this case, they are
identical, which means the comment has not been edited after initial posting. No
warning is emitted. Proceed with digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the current tagged format (`sha256-md`), not the legacy untagged
format (`sha256:<hex>`), so no legacy-format warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text
returned by the Jira API). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is plain markdown
text (not ADF JSON), the script outputs a tagged digest in the form:

```
sha256-md:<64-char-hex-of-current-description>
```

### 6. Compare format tags

The stored tag is `sha256-md` and the computed tag is `sha256-md` -- they match.
This means the producer (plan-feature) and the consumer (implement-task) used
compatible API access methods, so a direct hex digest comparison is valid. No
format-mismatch warning is needed.

### 7. Compare hex digests -- MISMATCH DETECTED

The stored hex digest is:

```
0000000000000000000000000000000000000000000000000000000000000000
```

The computed hex digest (from the current description) is a different value. The
digests do not match.

This means the task description was modified after plan-feature created it.

### 8. Alert the user and halt execution

Per the protocol, the mismatch triggers an immediate halt. The following message
is displayed to the user:

> **Warning: Task description integrity check failed.**
>
> The description for TC-9201 has been modified since plan-feature created it.
>
> - **Expected digest (from plan-feature comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest (computed from current description):** `sha256-md:<computed-hex-digest>`
>
> The task description was changed after the planning phase. This may indicate
> manual edits, a Jira workflow automation, or unintended modification.
>
> How would you like to proceed?
>
> 1. **Proceed** -- continue implementing with the current (modified) description as-is
> 2. **Stop** -- halt so you can re-run plan-feature to regenerate tasks with a fresh digest
>
> Please choose (1/2):

**Execution stops immediately.** No subsequent steps (Step 2 through Step 11) are
executed until the user responds.

- If the user chooses **Proceed (1)**: implementation continues from Step 2 using the
  current description content, accepting that it differs from what plan-feature
  originally generated.
- If the user chooses **Stop (2)**: the skill terminates. The user is expected to
  investigate the description change, optionally re-run plan-feature to regenerate
  the task with an updated digest, and then re-invoke implement-task.

## Summary of checks performed

| Check                  | Result                              | Action taken                     |
|------------------------|-------------------------------------|----------------------------------|
| Digest comment found?  | Yes (1 comment matches marker)      | Proceed to verification          |
| Comment edited?        | No (created == updated)             | No warning; proceed              |
| Digest format          | Tagged (`sha256-md`), not legacy    | No legacy warning; proceed       |
| Format tag comparison  | Both `sha256-md` -- tags match      | No format-mismatch warning       |
| Hex digest comparison  | Mismatch (stored != computed)       | Alert user, halt execution       |
