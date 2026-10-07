# Step 1.5 -- Description Integrity Verification for TC-9201

## Locating the Digest Comment

After fetching the task TC-9201 via `jira.get_issue("TC-9201")` in Step 1 and parsing
all required sections, Step 1.5 begins by retrieving all comments on the issue:

```
jira.get_issue_comments("TC-9201")
```

The skill searches the returned comments for any whose body starts with the marker
string `[sdlc-workflow] Description digest:`, as defined in
`shared/description-digest-protocol.md`. In this case, one comment is found with the
body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected directly. If multiple
comments had matched, the most recent one by `created` timestamp would be selected.

## Comment Edit Detection

The comment's `created` and `updated` timestamps are compared. In this scenario, the
timestamps are identical, meaning the comment has not been edited after initial posting.
No edit warning is emitted. The skill proceeds to digest comparison.

## Extracting the Stored Digest

The tagged digest value is parsed from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The value does not use the legacy untagged format (`sha256:<hex>`), so no legacy
warning applies.

## Computing the Current Digest

The skill extracts the description field from the TC-9201 issue response, writes it
to a temp file, and computes the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the format (plain markdown text) and outputs a tagged digest,
for example:

```
sha256-md:b7e4f2c8a1d9370e5f6b2c8d4a1e9f0370b5c8d2a4e7f1039b6c5d8e2a4f7013
```

(The exact hex value depends on the current description content.)

## Comparing Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md` -- the format tags
match. This means both the producer (plan-feature) and the consumer (implement-task)
used the same Jira access method, so a direct hex digest comparison is valid.

## Comparing Hex Digests -- Mismatch Detected

The hex digests are compared:

- **Expected (from digest comment):** `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `b7e4f2c8a1d9370e5f6b2c8d4a1e9f0370b5c8d2a4e7f1039b6c5d8e2a4f7013`

The hex hashes differ. This means the task description was modified after plan-feature
originally created it.

## User Alert and Execution Halt

The skill alerts the user with the following message:

> **Description integrity check failed.**
>
> The task description for TC-9201 was modified after plan-feature created it.
>
> - **Expected digest (from plan-feature comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest (computed from current description):** `sha256-md:b7e4f2c8a1d9370e5f6b2c8d4a1e9f0370b5c8d2a4e7f1039b6c5d8e2a4f7013`
>
> The description has been changed since plan-feature generated the task breakdown.
> The implementation may no longer align with the original plan.
>
> **How would you like to proceed?**
>
> 1. **Proceed** -- implement the task using the current (modified) description as-is
> 2. **Stop** -- halt execution so you can re-run plan-feature to regenerate tasks based on the updated description
>
> Please choose (1/2):

**Execution stops immediately at this point.** The skill does not proceed to Step 2
(Verify Dependencies), Step 3 (Transition to In Progress), or any subsequent
implementation steps. No branch is created, no code is modified, and no Jira
transitions occur. The skill waits for the user's explicit decision before taking
any further action.

This follows the same pause-and-ask pattern used when the task description has missing
or incomplete sections -- the skill halts and requires user input before continuing,
ensuring the user is aware of and has approved proceeding with a potentially stale
or altered task specification.
