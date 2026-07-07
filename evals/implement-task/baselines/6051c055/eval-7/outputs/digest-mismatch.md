# Step 1.5 -- Verify Description Integrity: Digest Mismatch Handling

## Context

Task: TC-9201

After fetching and parsing the task description in Step 1, Step 1.5 verifies that the description has not been modified since plan-feature created it, using the digest protocol defined in `shared/description-digest-protocol.md`.

The Jira issue has one comment posted by a previous plan-feature run with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

## Procedure

### 1. Retrieve Issue Comments

Fetch all comments on TC-9201 using the Jira MCP tool (or REST API fallback per Step 0.5):

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the Digest Comment Using the Marker String

Search the returned comments for any whose body starts with the marker string defined in `shared/description-digest-protocol.md`:

```
[sdlc-workflow] Description digest:
```

One comment is found matching this marker prefix. Its full body is:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected directly. (Per the protocol's "Multiple Digest Comments" rule, if multiple comments had matched, the most recent by `created` timestamp would be selected.)

### 3. Comment Edit Detection

Per the protocol's "Comment Edit Detection" section, compare the comment's `created` and `updated` timestamps to detect post-hoc editing. In this scenario, the `created` and `updated` timestamps are identical -- the comment was not edited after initial posting. No edit warning is raised. Proceed with digest comparison.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body after the marker string:

- **Full stored digest:** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Format tag:** `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the format-tagged syntax (`sha256-md:...`), not the legacy untagged format (`sha256:...`), so full verification proceeds.

### 5. Compute the Current Digest

Fetch the current description of TC-9201, write it to a temporary file, and compute its digest using the `scripts/sha256-digest.py` script as required by the protocol:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is markdown text (not ADF JSON), the script strips leading and trailing whitespace, computes the SHA-256 hash, and outputs a format-tagged digest:

```
sha256-md:a3f7b2c9d1e04856... (example -- the actual 64-character hex value computed from the current description)
```

Check the exit code: the script exited zero, so the output is valid.

### 6. Compare Format Tags

Per the protocol, compare the format tags before comparing hex digests:

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match (both `sha256-md`), confirming the producer and consumer used the same Jira access method (markdown text). Proceed to compare the hex digests directly.

(If the tags had differed -- e.g., stored `sha256-adf` vs computed `sha256-md` -- the protocol instructs logging a warning about different API access methods and skipping the integrity check entirely, proceeding normally without blocking.)

### 7. Compare Hex Digests -- MISMATCH DETECTED

The hex digests do not match:

```
Expected (from plan-feature comment): sha256-md:0000000000000000000000000000000000000000000000000000000000000000
Actual   (computed from current desc): sha256-md:a3f7b2c9d1e04856... (actual computed value)
```

The stored digest recorded by plan-feature at task creation time does not match the digest computed from the current task description. This means the task description was modified after plan-feature originally created the task.

### 8. Alert the User

Per Step 1.5 of implement-task and the protocol's consumer verification rules, the mismatch must not be silently ignored. The following alert is displayed to the user:

---

**Warning: Task description modified after planning.**

The description of TC-9201 has been modified since plan-feature created this task. The description integrity check failed -- the stored digest does not match the digest computed from the current description.

- **Expected digest** (recorded by plan-feature): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual digest** (computed from current description): `sha256-md:<computed-64-char-hex>`

Someone or something modified the task description between planning and implementation. The implementation may no longer be aligned with what was originally planned.

**How would you like to proceed?**

1. **Proceed** -- Continue implementing with the current (modified) description as-is
2. **Stop** -- Abort implementation so you can review the changes and re-run plan-feature to regenerate tasks

Choose (1/2):

---

### 9. STOP Execution -- Await User Response

Execution halts immediately at this point. No subsequent steps are performed until the user responds. This follows the same pause-and-ask pattern used for incomplete description handling in Step 1 ("list the gaps, ask the user for clarification, and stop execution immediately -- do not proceed with any subsequent steps").

The following steps are NOT executed while awaiting the user's choice:

- Step 2 (Verify Dependencies) is not executed.
- Step 3 (Transition to In Progress and Assign) is not executed.
- Step 4 (Understand the Code) is not executed.
- Step 5 (Create Branch) is not executed.
- Steps 6-11 (implementation, testing, commit, Jira update) are not executed.
- No implementation plan is produced.
- No code changes, branches, or commits are made.
- No Jira transitions occur.

The skill waits for the user's explicit choice before taking any further action:

- If the user chooses **option 1 (Proceed):** execution resumes from Step 2, using the current (modified) description as the basis for implementation.
- If the user chooses **option 2 (Stop):** execution terminates entirely. The user can review what changed in the description, re-run plan-feature to regenerate the task with a fresh digest matching the updated description, and then re-invoke implement-task.

## Summary

| Check | Result |
|---|---|
| Digest comment found? | Yes -- one comment matches `[sdlc-workflow] Description digest:` marker |
| Comment edited after posting? | No -- `created` equals `updated` |
| Legacy untagged format? | No -- uses format-tagged `sha256-md:` syntax |
| Format tags match? | Yes -- both `sha256-md` |
| Stored digest | `sha256-md:0000000000000000000000000000000000000000000000000000000000000000` |
| Computed digest | `sha256-md:<computed-64-char-hex>` (different from stored) |
| Digests match? | No -- MISMATCH |
| Action | Alert user with expected vs actual digests, offer proceed/stop choice, halt execution until user responds |
