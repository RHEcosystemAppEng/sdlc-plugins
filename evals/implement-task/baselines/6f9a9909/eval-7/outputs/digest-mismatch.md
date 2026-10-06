# Step 1.5 -- Description Integrity Verification for TC-9201

## Context

After fetching and parsing the Jira task TC-9201 in Step 1, Step 1.5 verifies that the task description has not been modified since plan-feature created it. This verification follows the description digest protocol defined in `shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search through the returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:`. In this case, one comment matches:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since there is only one matching comment, it is selected (if multiple existed, the most recent by `created` timestamp would be chosen).

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this scenario, they are identical, which means the comment has not been edited after initial posting. No warning is needed -- proceed with digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the current tagged format (not the legacy untagged `sha256:<hex>` format), so no legacy-format warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text fetched in Step 1), write it to a temporary file, and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is plain markdown text (not ADF JSON), it outputs a tagged digest in the form `sha256-md:<64-char-hex>`.

### 6. Compare format tags

The stored tag is `sha256-md` and the computed tag is `sha256-md` -- the tags match. This means the producer (plan-feature) and consumer (implement-task) used the same API access method (both MCP, which returns markdown). Proceed to hex digest comparison.

### 7. Compare hex digests -- MISMATCH DETECTED

The stored hex digest (`0000000000000000000000000000000000000000000000000000000000000000`) does not match the hex digest computed from the current description. This means the task description was modified after plan-feature created it.

## Action Taken

Alert the user with the following message:

> **Warning: Task description modified after planning.**
>
> The description for TC-9201 has been modified since plan-feature created it. The description digest does not match the digest recorded at creation time.
>
> - **Expected digest (from plan-feature comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest (computed from current description):** `sha256-md:<actual-computed-64-char-hex>`
>
> Options:
> 1. **Proceed** -- implement using the current (modified) description as-is
> 2. **Stop** -- re-run plan-feature to regenerate tasks from the updated feature specification
>
> Choose (1/2):

**Execution is stopped immediately.** No subsequent steps (Step 2 dependency verification, Step 3 transition to In Progress, Step 5 branch creation, Step 6 implementation, etc.) are executed until the user responds with their choice.

- If the user chooses **1 (Proceed)**: continue with implementation using the current description, starting from Step 2.
- If the user chooses **2 (Stop)**: halt execution entirely. The user will re-run plan-feature to regenerate tasks that reflect the updated feature specification, producing a new digest comment that matches.

## Rationale

This integrity check guards against silent tampering or uncoordinated edits between the planning and implementation phases. If someone modifies the task description after plan-feature created it -- whether intentionally (refining requirements) or accidentally (copy-paste error) -- the implementer should be made aware so they can decide whether to proceed with the modified specification or regenerate from a consistent plan. The check is non-blocking in the sense that the user can choose to proceed, but it requires explicit acknowledgment of the discrepancy.
