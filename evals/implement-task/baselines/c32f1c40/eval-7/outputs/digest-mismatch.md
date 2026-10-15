# Step 1.5 -- Description Integrity Verification for TC-9201

## Procedure

After fetching and parsing the TC-9201 task in Step 1, Step 1.5 verifies that the
description has not been modified since plan-feature created it. The following
sub-steps are executed in order, as defined in the SKILL.md and
`shared/description-digest-protocol.md`.

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search through the returned comments for any whose body starts with the marker
string `[sdlc-workflow] Description digest:`. In this scenario, exactly one comment
matches:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches, it is selected directly (no need to resolve
multiple matches by `created` timestamp).

### 3. Check for comment editing

Compare the comment's `created` and `updated` timestamps. In this scenario, the
timestamps are identical -- the comment was not edited after initial posting. No
warning is emitted. Proceed with digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the current tagged format (not the legacy untagged `sha256:<hex>`
format), so no legacy-format warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text
fetched in Step 1). Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (plain markdown text) and outputs a
tagged digest, e.g.:

```
sha256-md:b7e4f2a1c3d5e6f708192a3b4c5d6e7f8091a2b3c4d5e6f7a8b9c0d1e2f3a4b5
```

(The actual hex value would differ -- this is illustrative.)

### 6. Compare format tags

The stored tag is `sha256-md` and the computed tag is `sha256-md` -- the tags
match. This means both the producer (plan-feature) and the consumer
(implement-task) used the same API access method (both obtained markdown). No
format-mismatch warning is needed. Proceed to hex digest comparison.

### 7. Compare hex digests -- MISMATCH DETECTED

The stored hex digest (`0000...0000`) does not match the computed hex digest from
the current description. This means the task description was modified after
plan-feature created it.

**Action taken: alert the user and halt execution.**

The following message is displayed:

> **Warning: Task description was modified after plan-feature created it.**
>
> - Expected digest (from plan-feature comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - Actual digest (computed from current description): `sha256-md:<computed-hex-digest>`
>
> The task description for TC-9201 has been changed since plan-feature generated it.
> This could indicate manual edits, re-planning without updating the digest, or
> unintended modifications.
>
> How would you like to proceed?
> 1. **Proceed** -- use the current description as-is for implementation
> 2. **Stop** -- abort so you can re-run plan-feature to regenerate tasks with a fresh digest
>
> Please choose (1/2):

**Execution stops immediately.** No subsequent steps (Step 2 through Step 11) are
executed until the user responds. This is a hard stop -- the skill does not
silently continue with a modified description.

## Rationale

The digest mismatch indicates the description content changed between planning and
implementation. This guard exists to prevent implementing against a silently
tampered or outdated specification. The user must explicitly acknowledge the change
and decide whether the current description is acceptable or whether re-planning is
needed.

The fact that the comment was not edited (created equals updated) rules out the
scenario where someone modified both the description and the digest comment to
cover their tracks -- in this case, only the description was changed while the
original digest comment remained intact, which is the straightforward detection
case the protocol is designed for.
