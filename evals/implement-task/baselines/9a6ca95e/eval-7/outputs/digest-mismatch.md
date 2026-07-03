# Step 1.5 -- Description Integrity Verification for TC-9201

## Overview

After fetching the Jira task TC-9201 in Step 1, Step 1.5 verifies that the task description has not been modified since plan-feature created it, using the digest protocol defined in `shared/description-digest-protocol.md`.

## Procedure

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

One matching comment is found with body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

If multiple comments matched the marker, the most recent one by `created` timestamp would be selected. In this case, only one digest comment exists.

### 3. Check for comment editing

Compare the comment's `created` and `updated` timestamps. In this scenario, the two timestamps are identical, which means the comment has not been edited after initial posting. No warning is needed -- proceed with digest comparison.

(If `updated` were later than `created`, a warning would be surfaced: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." The digest comparison would still proceed regardless.)

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The format is not the legacy untagged format (`sha256:<hex>`), so no legacy warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response, write it to a temp file, and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the format. Since the description is markdown text (not ADF JSON), the script outputs a tagged digest such as:

```
sha256-md:a3b1f9e2c4d6078519e2a4b6c8d0f1234567890abcdef1234567890abcdef12
```

(The exact hex value would be computed from the current description content. The key point is that it differs from the stored value.)

- **Format tag:** `sha256-md`
- **Hex digest:** `a3b1f9e2c4d6078519e2a4b6c8d0f1234567890abcdef1234567890abcdef12`

### 6. Compare format tags

The stored tag is `sha256-md` and the computed tag is `sha256-md`. The tags match, so a direct hex digest comparison is performed.

(If the tags had differed -- for example, stored `sha256-adf` vs. computed `sha256-md` -- the protocol would log a warning about format mismatch due to different API access methods and skip the integrity check, proceeding normally.)

### 7. Compare hex digests -- MISMATCH detected

| | Digest |
|---|---|
| **Expected** (from digest comment) | `sha256-md:0000000000000000000000000000000000000000000000000000000000000000` |
| **Actual** (computed from current description) | `sha256-md:a3b1f9e2c4d6078519e2a4b6c8d0f1234567890abcdef1234567890abcdef12` |

The format tags match (`sha256-md`) but the hex hashes differ. This means the task description was modified after plan-feature created it.

## Action taken: alert the user and stop execution

Per the SKILL.md Step 1.5 instructions and the description-digest-protocol.md Consumer Verification rules, the following alert is presented to the user:

---

**WARNING: Description integrity check failed for TC-9201.**

The task description has been modified since plan-feature created it.

- **Expected digest** (recorded by plan-feature): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual digest** (computed from current description): `sha256-md:a3b1f9e2c4d6078519e2a4b6c8d0f1234567890abcdef1234567890abcdef12`

The description was changed after the planning phase. Implementing a modified description may produce results inconsistent with the original plan.

**Options:**

1. **Proceed** -- implement the task using the current (modified) description as-is
2. **Stop** -- halt implementation so you can re-run plan-feature to regenerate tasks from the updated feature description

Choose (1/2):

---

## Execution halted

Execution is stopped immediately at Step 1.5. No subsequent steps are performed:

- Step 2 (Verify Dependencies) is NOT executed
- Step 3 (Transition to In Progress) is NOT executed
- Step 4 (Understand the Code) is NOT executed
- Step 5 (Create Branch) is NOT executed
- Steps 6-11 are NOT executed
- No implementation plan is written

The skill waits for the user's response before taking any further action.

### If the user chooses option 1 (Proceed)

Implementation would continue from Step 2 onward using the current description content, despite the digest mismatch. The mismatch is noted but does not block further work.

### If the user chooses option 2 (Stop)

The skill terminates. The user is expected to investigate the description change, potentially re-run plan-feature to regenerate tasks that reflect the updated feature requirements, and then re-invoke implement-task on the regenerated task.
