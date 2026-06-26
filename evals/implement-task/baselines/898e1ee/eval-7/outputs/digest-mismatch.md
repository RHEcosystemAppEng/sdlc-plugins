# Step 1.5 -- Verify Description Integrity (TC-9201)

## 1. Retrieve Issue Comments

Fetch all comments on TC-9201 using:

```
jira.get_issue_comments("TC-9201")
```

## 2. Locate the Digest Comment

Search through the returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:`. One matching comment is found with body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Only one comment matches the marker, so it is selected directly. (If multiple matched, the most recent by `created` timestamp would be selected.)

## 3. Check for Comment Editing

Compare the comment's `created` and `updated` timestamps. They are identical, so the comment has not been edited after initial posting. No edit warning is needed. Proceed with digest comparison.

## 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the format-tagged format (not the legacy untagged `sha256:<hex>` format), so the integrity check proceeds normally.

## 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (the markdown text describing the advisory severity aggregation service). Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as markdown text and outputs a tagged digest, for example:

```
sha256-md:7f3a1b2c4d5e6f7890abcdef1234567890abcdef1234567890abcdef12345678
```

The script exits with status 0 (success), so the computed digest is valid.

## 6. Compare Format Tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match. Both the producer (plan-feature) and the consumer (implement-task) used the same Jira access method (both returned markdown). Proceed to hex digest comparison.

## 7. Compare Hex Digests

- **Expected (from comment):** `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `7f3a1b2c4d5e6f7890abcdef1234567890abcdef1234567890abcdef12345678`

The hex digests **do not match**.

## 8. Alert the User

The task description for TC-9201 was modified after plan-feature created it. The description integrity check has failed.

**Description integrity check: MISMATCH**

The task description has been modified since plan-feature originally created it.

| | Digest |
|---|---|
| **Expected** (from plan-feature digest comment) | `sha256-md:0000000000000000000000000000000000000000000000000000000000000000` |
| **Actual** (computed from current description) | `sha256-md:7f3a1b2c4d5e6f7890abcdef1234567890abcdef1234567890abcdef12345678` |

Someone (or an automated process) modified the Jira task description after plan-feature generated it. The implementation may no longer match the original plan.

**Please choose how to proceed:**

1. **Proceed** -- Continue with the current description as-is. The implementation will be based on the modified description, which may differ from what plan-feature originally intended.
2. **Stop** -- Abort implementation so you can re-run plan-feature to regenerate tasks with a fresh description and digest. This ensures the implementation matches a verified plan.

## 9. Stop Execution

**Execution is halted.** No subsequent steps (Step 2 -- Verify Dependencies, Step 3 -- Transition to In Progress, Step 4 -- Understand the Code, Step 5 -- Create Branch, Step 6 -- Implement Changes, or any later steps) will proceed until the user responds to the prompt above.

This is a hard stop as specified by the description digest protocol. The skill will resume only after the user explicitly selects option 1 (Proceed) or option 2 (Stop).
