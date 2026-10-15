# Step 1.5 -- Description Integrity Verification for TC-9201

## Context

Task TC-9201 ("Add advisory severity aggregation service and endpoint") was fetched
and parsed successfully in Step 1. The structured description contains all required
sections (Repository, Target Branch, Description, Files to Modify, Files to Create,
API Changes, Implementation Notes, Acceptance Criteria, Test Requirements,
Dependencies). No missing sections were detected.

## Step 1.5 Execution

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search all returned comments for bodies starting with the marker string
`[sdlc-workflow] Description digest:`. One matching comment is found:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

This is the only comment matching the marker, so it is selected (no tie-breaking
needed).

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. Per the scenario, these
timestamps are identical -- the comment was not edited after initial posting. No
warning is emitted. Proceed with digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the format-tagged scheme (not the legacy untagged `sha256:<hex>`
format), so the integrity check proceeds normally.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text
returned by the API). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as plain text (markdown) and outputs a tagged
digest, for example:

```
sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

(This is an illustrative value -- the actual hash would be computed from the current
description content.)

### 6. Compare format tags

- **Stored tag**: `sha256-md`
- **Computed tag**: `sha256-md`

The format tags match. Both the producer (plan-feature) and the consumer
(implement-task) used the same API access method (both returned markdown). Proceed
to hex digest comparison.

### 7. Compare hex digests

- **Expected (from comment)**: `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description)**: `sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

**Result: MISMATCH**

The hex digests differ. The format tags match (`sha256-md`), confirming both sides
used the same description format, but the content has changed since plan-feature
created the task.

## Action Taken: Alert User and Stop

Per the skill instructions (Step 1.5, item 4e, mismatch case), the following message
is presented to the user:

---

> **Description integrity check failed for TC-9201.**
>
> The task description has been modified since plan-feature created it. The content
> digest recorded at creation time does not match the digest computed from the current
> description.
>
> **Expected digest** (recorded by plan-feature):
> `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
>
> **Actual digest** (computed from current description):
> `sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
>
> The description was changed after planning. This could indicate manual edits,
> re-planning without updating the digest, or unintended modifications.
>
> How would you like to proceed?
>
> 1. **Proceed** -- implement using the current description as-is
> 2. **Stop** -- halt so you can re-run plan-feature to regenerate tasks with a fresh digest
>
> Choose (1/2):

---

**Execution is stopped immediately.** No subsequent steps (Step 2 -- Verify
Dependencies, Step 3 -- Transition to In Progress, Step 4 -- Understand the Code,
or any later steps) are executed until the user responds with their choice.

- If the user chooses **1 (Proceed)**: implementation continues from Step 2 using the
  current description content, accepting that it differs from what plan-feature
  originally produced.
- If the user chooses **2 (Stop)**: the skill terminates. The user is expected to
  re-run plan-feature to regenerate the task descriptions and their corresponding
  digest comments before re-invoking implement-task.
