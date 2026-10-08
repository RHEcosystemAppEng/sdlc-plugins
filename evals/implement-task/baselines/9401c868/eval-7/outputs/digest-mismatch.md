# Step 1.5 -- Description Integrity Verification for TC-9201

## Overview

This document describes how the implement-task skill handles the description
integrity verification in Step 1.5 for task TC-9201, given a digest mismatch
scenario.

## Step 1.5 Execution Trace

### 1. Retrieve Issue Comments

After fetching the task in Step 1, I retrieve all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

The API returns one comment with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

### 2. Locate the Digest Comment

I search all returned comments for bodies starting with the marker string
`[sdlc-workflow] Description digest:`. One comment matches. Since there is
only one matching comment, there is no need to select among multiple by
`created` timestamp -- this single comment is used.

### 3. Comment Edit Detection

The comment's `created` and `updated` timestamps are identical. Per the
protocol, this means the comment was not edited after initial posting.
No warning is emitted. Proceed with digest comparison.

### 4. Extract the Stored Digest

From the comment body `[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000`, I parse:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the current tagged format (not the legacy untagged `sha256:<hex>`
format), so no legacy-format warning is needed. Proceed with comparison.

### 5. Compute the Current Digest

I extract the description field from the TC-9201 issue response (the markdown
content from the Description section), write it to a temporary file, and
compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as plain text (markdown) and outputs a
tagged digest, for example:

```
sha256-md:b7e23ec29af22b0b4e41da31e868d57226121c84847562bacef36507739a83a4
```

(The actual hex value would be computed from the current task description
content. The key point is that it differs from the stored digest.)

### 6. Compare Format Tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match. Both the producer (plan-feature) and the consumer
(implement-task) used the same Jira access method (markdown/MCP path). No
format-mismatch warning is needed. Proceed to hex digest comparison.

### 7. Compare Hex Digests -- MISMATCH DETECTED

- **Expected (from comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `sha256-md:b7e23ec29af22b0b4e41da31e868d57226121c84847562bacef36507739a83a4`

The hex digests do not match. This means the task description was modified
after plan-feature created it.

### 8. Alert the User

I present the following alert to the user:

---

> **Warning: Task description modified after planning**
>
> The description for TC-9201 has been modified since plan-feature created it.
> The integrity digest recorded at planning time does not match the current
> description content.
>
> - **Expected digest (from plan-feature):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest (current description):** `sha256-md:b7e23ec29af22b0b4e41da31e868d57226121c84847562bacef36507739a83a4`
>
> This may indicate that someone edited the task description in Jira after
> plan-feature generated it. The implementation may not match the original
> planning intent.
>
> How would you like to proceed?
>
> 1. **Proceed** -- implement the task using the current (modified) description as-is
> 2. **Stop** -- halt implementation so you can review the changes and optionally re-run plan-feature to regenerate tasks
>
> Please choose (1 or 2):

---

### 9. Stop Execution Immediately

**Execution halts at this point.** I do not proceed to Step 2 (Verify
Dependencies), Step 3 (Transition to In Progress), or any subsequent step.
No branch is created, no code is read or modified, and no Jira transitions
are performed.

The skill waits for the user's explicit response before taking any further
action:

- **If the user chooses 1 (Proceed):** I continue with the current description
  as the implementation specification, resuming at Step 2 (Verify Dependencies).
- **If the user chooses 2 (Stop):** I terminate the skill execution entirely.
  The user can review the description changes, optionally re-run plan-feature
  to regenerate the task with an updated digest, and then re-invoke
  implement-task.

## Key Behaviors

1. **Detection is automatic:** The digest check runs as part of the standard
   Step 1.5 flow for every task that has a digest comment. No user action is
   needed to trigger it.

2. **Format tag comparison precedes hex comparison:** The format tags are
   compared first. Only when tags match (as in this scenario, both `sha256-md`)
   does the hex digest comparison proceed. If tags had differed, the check
   would have been skipped with a warning.

3. **Comment edit detection runs independently:** The `created` vs `updated`
   timestamp check happens before digest comparison. In this scenario, the
   timestamps are identical, so no edit warning is raised. Had they differed,
   an additional warning would have been surfaced alongside the mismatch alert.

4. **Hard stop on mismatch:** The mismatch triggers an immediate halt. No
   subsequent steps execute. This prevents implementing a task whose
   specification may have been tampered with or inadvertently changed between
   planning and implementation.

5. **User decision required:** The skill does not make a default choice. Both
   options (proceed or stop) are presented, and the user must explicitly
   respond. This ensures accountability for proceeding with a modified
   description.

6. **Both digests displayed:** The expected (stored) and actual (computed)
   digests are shown in full so the user can independently verify or
   investigate the mismatch.
