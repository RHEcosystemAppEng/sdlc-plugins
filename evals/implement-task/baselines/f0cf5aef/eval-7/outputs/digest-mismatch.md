# Step 1.5 -- Verify Description Integrity for TC-9201

## Procedure

After fetching the task TC-9201 in Step 1 and parsing its structured description
(Repository, Target Branch, Files to Modify, Files to Create, etc.), Step 1.5
verifies that the description has not been modified since plan-feature created it.

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search all returned comments for those whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

In this case, one comment matches. Its full body is:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since there is only one matching comment, it is selected directly. If multiple
comments matched, the most recent one by `created` timestamp would be selected.

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this case they are
identical, which means the comment has not been edited after initial posting. No
edit warning is needed. Proceed to digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the modern format-tagged syntax (not the legacy untagged `sha256:<hex>`
format), so the integrity check proceeds normally.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response. Write it to a
temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as plain text (markdown) and outputs a tagged
digest, for example:

```
sha256-md:b7e23ec29af22b0b4e41da31e868d57226121c84f19e58bce55a6f823ce8654f
```

(The exact hex value above is illustrative -- the actual value would be computed
from the current description content.)

### 6. Compare format tags

The stored tag is `sha256-md` and the computed tag is `sha256-md`. The format tags
match, meaning both the producer (plan-feature) and consumer (implement-task) used
the same Jira access method (both received markdown). Proceed to hex digest
comparison.

### 7. Compare hex digests -- MISMATCH DETECTED

The hex digests do NOT match:

| Source   | Tagged Digest |
|----------|---------------|
| Expected (from comment) | `sha256-md:0000000000000000000000000000000000000000000000000000000000000000` |
| Actual (computed from current description) | `sha256-md:<actual-64-char-hex-from-script-output>` |

The format tags are identical (`sha256-md`) but the hex hashes differ. This means
the task description was modified after plan-feature originally created TC-9201.

## User Alert

The following alert would be presented to the user:

> **Description integrity check failed for TC-9201.**
>
> The task description has been modified since plan-feature created this task.
> The description digest recorded at creation time does not match the current
> description content.
>
> - **Expected digest** (from plan-feature comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from current description): `sha256-md:<actual-64-char-hex-from-script-output>`
>
> This could indicate that someone manually edited the task description in Jira
> after plan-feature generated it. The implementation may not match the original
> plan if you proceed.
>
> **Options:**
> 1. **Proceed** -- implement using the current (modified) description as-is
> 2. **Stop** -- halt so you can re-run plan-feature to regenerate tasks from the updated feature specification
>
> Choose (1/2):

## Execution State

**Execution is STOPPED.** No subsequent steps are taken until the user responds.
Specifically:

- Step 2 (Verify Dependencies) is NOT executed
- Step 3 (Transition to In Progress) is NOT executed
- No branch is created
- No implementation plan is drafted
- No code changes are made

The skill resumes only after the user selects option 1 (proceed) or option 2 (stop).
If the user selects option 2, the skill terminates entirely and the user is expected
to re-run plan-feature before re-invoking implement-task.
