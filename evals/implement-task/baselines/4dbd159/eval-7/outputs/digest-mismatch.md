# Step 1.5 -- Description Integrity Verification: Digest Mismatch Handling

## Context

Task: TC-9201 (Add advisory severity aggregation service and endpoint)
Digest comment found on the issue, posted by a previous plan-feature run.

## Procedure Followed

### 1. Retrieve Issue Comments

After fetching and parsing the task in Step 1, Step 1.5 begins by retrieving all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

This returns the list of all comments on the issue.

### 2. Locate the Digest Comment

Search all returned comments for those whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

In this case, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256:0000000000000000000000000000000000000000000000000000000000000000
```

If multiple comments matched the marker, the most recent one by `created` timestamp would be selected, per the protocol's "Multiple Digest Comments" rule. Here only one comment matches, so it is used directly.

### 3. Comment Edit Detection

The protocol requires checking whether the digest comment was edited after initial posting by comparing its `created` and `updated` timestamps.

In this scenario, the comment's `created` and `updated` timestamps are identical. This means the comment has not been edited since it was posted. No edit-detection warning is emitted.

Had `updated` been later than `created`, the following warning would have been surfaced to the user: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." Digest comparison would still proceed regardless.

### 4. Extract the Stored Digest

Parse the `sha256:<hex-digest>` value from the comment body:

```
Stored digest: sha256:0000000000000000000000000000000000000000000000000000000000000000
```

### 5. Compute the Current Digest

Compute SHA-256 of the current description field text, following the normalization rules from the description digest protocol:

- **ADF JSON (MCP path):** Parse the description as JSON and re-serialize with compact separators (`json.dumps(parsed, separators=(',', ':'))`), then hash the result.
- **Raw text (REST API path):** Strip leading and trailing whitespace, then hash the result.

The preferred method is to use the `scripts/sha256-digest.py` tool:

```bash
# Write the description content to a temporary file
# Then compute the digest
python3 scripts/sha256-digest.py /tmp/desc.json
```

This produces the actual 64-character lowercase hexadecimal SHA-256 digest of the current description content. For this scenario, the computed digest will differ from the stored all-zeros digest because the task description was modified after plan-feature created it.

Example computed digest (illustrative):

```
Computed digest: sha256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069
```

### 6. Compare Digests -- Mismatch Detected

The stored digest and the computed digest do not match:

```
Expected (from comment): sha256:0000000000000000000000000000000000000000000000000000000000000000
Actual (computed now):    sha256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069
```

This indicates the task description was modified after plan-feature created it.

### 7. Alert the User

The following message is presented to the user:

> **Description integrity check failed.**
>
> The task description for TC-9201 has been modified since plan-feature created it.
>
> - **Expected digest** (from plan-feature comment): `sha256:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from current description): `sha256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069`
>
> The description may have been edited manually or by another process after the planning phase.
>
> **Choose how to proceed:**
> 1. **Proceed** -- accept the current description as-is and continue with implementation
> 2. **Stop** -- halt execution so you can re-run plan-feature to regenerate tasks with the updated description
>
> Choose (1/2):

### 8. Stop Execution Immediately

Per the SKILL.md specification, execution **stops immediately** after presenting the choice to the user. No subsequent steps are performed until the user responds:

- Step 2 (Verify Dependencies) is NOT entered.
- Step 3 (Transition to In Progress) is NOT entered.
- Step 4 (Understand the Code) is NOT entered.
- Step 5 (Create Branch) is NOT entered.
- No implementation planning, code changes, branching, or Jira transitions occur.

The skill is fully blocked, waiting for the user's explicit decision.

### 9. Handling the User's Response

- **If the user chooses "Proceed" (option 1):** The skill resumes from Step 2 onward, using the current (modified) description as the specification. The mismatch is noted but does not prevent implementation.

- **If the user chooses "Stop" (option 2):** The skill terminates. The user is expected to re-run plan-feature to regenerate the task descriptions, which will post a new digest comment reflecting the updated description. The user can then re-invoke implement-task on the regenerated task.

## Summary of Key Behaviors

| Aspect | Behavior |
|---|---|
| Digest comment location | Search all comments for marker prefix `[sdlc-workflow] Description digest:` |
| Multiple digest comments | Select most recent by `created` timestamp |
| Comment edit detection | Compare `created` vs `updated` timestamps; warn if edited, proceed regardless |
| Comment not edited (this scenario) | No warning emitted; proceed to digest comparison |
| Digest computation | Use `scripts/sha256-digest.py` (preferred) or manual SHA-256 with proper normalization |
| Digest match | Proceed silently, no user prompt |
| Digest mismatch (this scenario) | Alert user with expected vs actual values, offer proceed/stop choice |
| Execution on mismatch | Hard stop -- no steps after 1.5 execute until user responds |
| No digest comment found | Log warning, proceed normally (backward compatibility) |
