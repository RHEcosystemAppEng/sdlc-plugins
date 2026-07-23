# Step 1.5 -- Description Integrity Verification for TC-9201

## 1. Retrieve Issue Comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

## 2. Locate the Digest Comment

Search the returned comments for any whose body starts with the marker string
`[sdlc-workflow] Description digest:` as defined in `shared/description-digest-protocol.md`.

One matching comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected directly (no need to compare
`created` timestamps to pick the most recent).

## 3. Check for Comment Editing

The comment's `created` and `updated` timestamps are identical. This means the comment
was not edited after initial posting -- no warning is needed. Proceed with digest comparison.

## 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the format-tagged style (not the legacy untagged `sha256:<hex>` format),
so the integrity check proceeds normally.

## 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (the markdown text returned
by `jira.get_issue`). Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects that the input is plain markdown text and outputs a tagged digest:

```
sha256-md:b7e4a3f1c9d2e8...  (example -- the actual 64-char hex from the current description)
```

## 6. Compare Format Tags

- Stored tag: `sha256-md`
- Computed tag: `sha256-md`

The format tags match (both `sha256-md`), so the hex digests can be compared directly.
No format mismatch warning is needed.

## 7. Compare Hex Digests -- MISMATCH DETECTED

- **Expected** (from digest comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual** (computed from current description): `sha256-md:<computed-64-char-hex-digest>`

The hex hashes differ. This means the task description was modified after plan-feature
created it.

## 8. Alert the User

The following warning is displayed to the user:

> **Description integrity check failed for TC-9201.**
>
> The task description has been modified since plan-feature created it.
>
> - **Expected digest** (recorded by plan-feature): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from current description): `sha256-md:<computed-64-char-hex-digest>`
>
> The description content no longer matches what was originally planned. This could mean
> someone edited the task description in Jira after plan-feature generated it.
>
> **How would you like to proceed?**
>
> 1. **Proceed** -- implement the task using the current (modified) description as-is
> 2. **Stop** -- halt implementation so you can re-run plan-feature to regenerate tasks from the updated feature specification
>
> Please choose (1 or 2):

## 9. Stop Execution

Execution is **stopped immediately** after presenting the choice. No subsequent steps
are executed -- Step 2 (Verify Dependencies), Step 3 (Transition to In Progress),
Step 4 (Understand the Code), Step 5 (Create Branch), Step 6 (Implement Changes), and
all remaining steps are blocked until the user responds.

This follows the same pause-and-ask pattern used when the task description is incomplete
(as specified in Step 1): "stop execution immediately -- do not proceed with any subsequent
steps (branching, implementation planning, code changes) until the user provides the
missing information."

No implementation plan is produced. The skill waits for the user's explicit choice before
taking any further action.
