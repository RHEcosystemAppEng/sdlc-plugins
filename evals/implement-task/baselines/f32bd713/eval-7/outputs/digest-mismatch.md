# Step 1.5 -- Description Integrity Verification for TC-9201

## Overview

After fetching and parsing the Jira task TC-9201 in Step 1, Step 1.5 verifies that the task description has not been modified since plan-feature created it, using the digest protocol defined in `shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search through all returned comments for those whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

One matching comment is found with body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected (if multiple matched, the most recent by `created` timestamp would be chosen).

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this case, the two timestamps are identical, meaning the comment was **not edited** after initial posting. No edit warning is needed. Proceed with digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the tagged format (not the legacy untagged `sha256:<hex>` format), so no legacy-format warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text describing the advisory severity aggregation service and endpoint). Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as plain text (markdown) and outputs a tagged digest, for example:

```
sha256-md:b7e23ec29af22b0b4e41da31e868d57226121c84f20f5e6ab40d1b3c295e1f90
```

(The actual hex value would be whatever SHA-256 produces from the current description content.)

### 6. Compare format tags

- Stored tag: `sha256-md`
- Computed tag: `sha256-md`

The format tags **match** -- both are `sha256-md`. This means both the producer (plan-feature) and the consumer (implement-task) used the same API access method (MCP, which returns markdown). Proceed to hex digest comparison.

### 7. Compare hex digests

- **Expected (from comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `sha256-md:b7e23ec29af22b0b4e41da31e868d57226121c84f20f5e6ab40d1b3c295e1f90`

The hex digests **do not match**. The format tags are the same (`sha256-md`), ruling out a cross-format mismatch. This means the task description was modified after plan-feature created it.

## Action Taken: Alert the User

Per the protocol, I would alert the user with the following message:

---

**Description integrity check failed for TC-9201.**

The task description has been modified since plan-feature created it. The digest recorded at creation time does not match the digest computed from the current description.

- **Expected digest (from plan-feature comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual digest (computed from current description):** `sha256-md:b7e23ec29af22b0b4e41da31e868d57226121c84f20f5e6ab40d1b3c295e1f90`

The description may have been manually edited in Jira after the planning phase. This could mean the implementation plan no longer reflects the intended specification.

**How would you like to proceed?**

1. **Proceed** -- implement the task using the current (modified) description as-is
2. **Stop** -- halt so you can re-run plan-feature to regenerate the task with a fresh plan and matching digest

---

## Execution State

**Execution is halted.** No subsequent steps (Step 2 -- Verify Dependencies, Step 3 -- Transition to In Progress, or any implementation steps) will be performed until the user responds with their choice.

- If the user chooses **option 1 (Proceed)**: continue to Step 2 using the current description content, accepting that it differs from what plan-feature originally produced.
- If the user chooses **option 2 (Stop)**: terminate the skill execution entirely. The user will re-run plan-feature to regenerate the task, which will post a new digest comment matching the updated description.

No branches are created, no code is read or modified, and no Jira status transitions occur while awaiting the user's decision.
