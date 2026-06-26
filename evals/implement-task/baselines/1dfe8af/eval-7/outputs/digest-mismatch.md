# Step 1.5 -- Description Integrity Verification for TC-9201

## 1. Locating the Digest Comment

After fetching the task TC-9201 via `jira.get_issue("TC-9201")` and parsing the structured description in Step 1, Step 1.5 begins by retrieving all comments on the issue:

```
jira.get_issue_comments("TC-9201")
```

The response contains a list of comments. Each comment is searched for the marker string `[sdlc-workflow] Description digest:` at the start of the comment body. This marker is defined in the description digest protocol (`plugins/sdlc-workflow/shared/description-digest-protocol.md`).

In this case, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected directly. (If multiple comments matched, the most recent one by `created` timestamp would be selected to handle plan-feature re-run scenarios.)

## 2. Comment Edit Detection

The protocol requires checking whether the digest comment was edited after posting by comparing its `created` and `updated` timestamps. In this scenario, the comment's `created` and `updated` timestamps are identical, which means the comment has not been edited since it was posted. No warning is issued for comment editing -- the comment is trustworthy from a tampering perspective.

## 3. Extracting the Stored Digest

The tagged digest value is parsed from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The format is not legacy (it is not the untagged `sha256:<hex>` format), so the integrity check proceeds normally.

## 4. Computing the Current Digest

The current description is extracted from the issue response (the markdown text of the task description). It is written to a temporary file:

```bash
# Write the description to a temp file
cat > /tmp/desc-TC-9201.txt << 'DESCRIPTION'
Add a service method and REST endpoint that aggregates vulnerability advisory severity
counts for a given SBOM. The endpoint returns a summary with counts per severity level
(Critical, High, Medium, Low) and a total, enabling dashboard widgets to render severity
breakdowns without client-side counting.
...
DESCRIPTION

# Compute the digest using the project script
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (plain markdown text) and outputs a tagged digest, for example:

```
sha256-md:b7e4f89a2c1d3e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f
```

(This is an illustrative hash -- the actual value would be computed from the current description content.)

## 5. Comparing Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md`. The format tags match, so we proceed to compare the hex digests directly. (If the tags differed -- e.g., stored was `sha256-adf` but computed was `sha256-md` -- we would log a warning about different API access methods and skip the integrity check entirely.)

## 6. Detecting the Digest Mismatch

The hex digests are compared:

- **Expected (from comment):** `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `b7e4f89a2c1d3e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f`

The digests do NOT match. This means the task description was modified after plan-feature originally created it.

## 7. Alerting the User

The following alert is presented to the user:

> **Warning: Task description modified after planning**
>
> The description for TC-9201 has been modified since plan-feature created it.
> The description digest does not match the value recorded at creation time.
>
> - **Expected digest (from plan-feature):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest (current description):** `sha256-md:b7e4f89a2c1d3e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f`
>
> The description may have been edited manually in Jira after plan-feature generated the tasks.
> This could mean the implementation plan is out of sync with the current description.
>
> How would you like to proceed?
>
> 1. **Proceed** -- implement using the current description as-is
> 2. **Stop** -- abort so you can re-run plan-feature to regenerate tasks from the updated description
>
> Choose (1/2):

## 8. Stopping Execution

**Execution stops immediately at this point.** The skill does NOT proceed to Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), or any subsequent implementation steps. This follows the same pause-and-ask pattern used when the description is incomplete -- the user must explicitly choose an option before the skill continues.

- If the user chooses **option 1 (Proceed)**: the skill resumes from Step 2 using the current description content, acknowledging the mismatch.
- If the user chooses **option 2 (Stop)**: the skill terminates entirely. The user is expected to re-run plan-feature to regenerate tasks that reflect the updated description, then re-invoke implement-task.

No branches are created, no code is read or modified, no Jira transitions are made, and no implementation planning occurs until the user responds.

## Summary of Step 1.5 Decision Flow

```
Fetch comments on TC-9201
   |
   v
Search for marker: "[sdlc-workflow] Description digest:"
   |
   v
Found 1 matching comment --> select it (most recent if multiple)
   |
   v
Check created vs updated timestamps --> identical, no edit warning
   |
   v
Parse stored digest --> tag: sha256-md, hex: 0000...0000
   |
   v
Not legacy format (not untagged "sha256:") --> continue
   |
   v
Compute current digest via scripts/sha256-digest.py --> sha256-md:<current-hex>
   |
   v
Compare format tags --> both sha256-md, tags match --> compare hex digests
   |
   v
Hex digests differ --> MISMATCH DETECTED
   |
   v
Alert user with expected vs actual digests
   |
   v
Offer choice: (1) Proceed with current description, (2) Stop to re-run plan-feature
   |
   v
STOP EXECUTION -- wait for user input
```
