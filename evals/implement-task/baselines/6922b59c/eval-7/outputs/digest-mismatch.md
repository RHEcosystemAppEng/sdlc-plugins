# Step 1.5 -- Description Integrity Verification for TC-9201

## Context

Task TC-9201 ("Add advisory severity aggregation service and endpoint") has been
fetched and parsed successfully in Step 1. The structured description contains all
required sections (Repository, Target Branch, Description, Files to Modify, Files
to Create, API Changes, Implementation Notes, Acceptance Criteria, Test
Requirements, Dependencies). Step 1 parsing is complete with no gaps.

Proceeding to Step 1.5 -- Verify Description Integrity.

## Step 1.5 Execution

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

The API returns one comment with the following properties:
- **Body**: `[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Created**: (timestamp T)
- **Updated**: (timestamp T) -- identical to created

### 2. Locate the digest comment

Search all comments for bodies starting with the marker string
`[sdlc-workflow] Description digest:`. One comment matches. Since there is only
one matching comment, no tie-breaking by `created` timestamp is needed. This
comment is selected as the digest comment.

### 3. Check for comment editing

The comment's `created` and `updated` timestamps are identical. This means the
comment has not been edited after initial posting. No warning is issued. Proceed
with digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Full value**: `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Format tag**: `sha256-md`
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the current tagged format (not the legacy untagged `sha256:<hex>`
format), so no legacy-format warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response. Write it to a
temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as plain text (markdown, not ADF JSON) and
outputs a tagged digest:

```
sha256-md:e4a7b2c9d1f3... (example -- actual 64-character hex from current description)
```

- **Computed format tag**: `sha256-md`
- **Computed hex digest**: (the actual 64-character hex hash of the current description content)

The script exits with status 0 (success), so the computed digest is valid.

### 6. Compare format tags

- **Stored tag**: `sha256-md`
- **Computed tag**: `sha256-md`

The format tags match. Both the producer (plan-feature) and the consumer
(implement-task) used the same API access method (MCP/markdown). No format
mismatch warning is needed. Proceed to hex digest comparison.

### 7. Compare hex digests

- **Expected (from comment)**: `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description)**: (different 64-character hex hash)

The hex digests **do not match**. This means the task description was modified
after plan-feature originally created it.

### 8. Alert the user

Per the SKILL.md Step 1.5(e) mismatch handling, the following alert is presented
to the user:

```
WARNING: Task description integrity check failed for TC-9201.

The task description has been modified since plan-feature created it.

  Expected digest (from plan-feature comment):
    sha256-md:0000000000000000000000000000000000000000000000000000000000000000

  Actual digest (computed from current description):
    sha256-md:<actual-64-char-hex-from-current-description>

The description was changed after the planning phase. This may indicate
manual edits, a partial re-plan, or unintended modifications.

How would you like to proceed?
  1. Proceed -- use the current (modified) description as-is
  2. Stop -- abort so you can re-run plan-feature to regenerate tasks

Choose (1/2):
```

### 9. Stop execution

**Execution stops immediately.** No subsequent steps (Step 2 -- Verify
Dependencies, Step 3 -- Transition to In Progress, Step 4 -- Understand the Code,
or any later steps) are executed until the user responds.

- If the user chooses **1 (Proceed)**: implementation continues with Step 2 using
  the current description content as the specification, accepting the risk that it
  differs from what was originally planned.
- If the user chooses **2 (Stop)**: the skill terminates. The user is expected to
  re-run plan-feature to regenerate task descriptions with fresh digests, then
  re-invoke implement-task.

## Summary of Verification Logic Applied

| Check | Result | Action |
|---|---|---|
| Digest comment found? | Yes (1 comment matches marker) | Continue verification |
| Comment edited? | No (created == updated) | No warning, continue |
| Digest format (legacy untagged)? | No (uses tagged sha256-md format) | No legacy warning, continue |
| Format tags match? | Yes (both sha256-md) | Compare hex digests |
| Hex digests match? | No (hashes differ) | Alert user, stop execution |

## Key Behavioral Notes

- The digest comment itself was **not tampered with** (created == updated), so the
  stored digest is trustworthy. The mismatch is caused by a change to the task
  description, not to the digest comment.
- Because the format tags match, we can be confident the comparison is valid --
  both sides hashed the same representation (markdown text).
- The skill does **not** silently proceed on a digest mismatch. It requires
  explicit user acknowledgment before continuing.
- The skill does **not** attempt to diff the descriptions or identify what changed.
  It reports the cryptographic evidence (expected vs actual digest) and defers the
  decision to the user.
