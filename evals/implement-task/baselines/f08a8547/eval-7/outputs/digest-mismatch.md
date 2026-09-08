# Step 1.5 -- Description Integrity Verification for TC-9201

## Context

Task TC-9201 has been fetched and its structured description parsed successfully in Step 1. Step 1.5 requires verifying that the description has not been modified since plan-feature created it, using the digest protocol defined in `shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search returned comments for any whose body starts with the marker string:

```
[sdlc-workflow] Description digest:
```

One matching comment is found with body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected directly. If multiple comments had matched, the most recent by `created` timestamp would be selected.

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this case, the two timestamps are identical -- the comment has not been edited since it was posted. No warning is needed for comment tampering.

If `updated` had been later than `created`, the following warning would be surfaced: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." Digest comparison would still proceed.

### 4. Extract the stored digest

Parse the tagged digest from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

The format tag is not the legacy untagged format (`sha256:<hex>`), so no legacy-format warning is needed. Proceed with full verification.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text of the Description section). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is markdown text (fetched via MCP or stored as plain text), the script outputs a tagged digest in the form:

```
sha256-md:<64-char-hex>
```

For this scenario, assume the script exits zero and produces a valid tagged digest such as:

```
sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

(The actual hex value would be whatever SHA-256 the current description content produces.)

### 6. Compare format tags

- **Stored tag**: `sha256-md`
- **Computed tag**: `sha256-md`

The tags match. Both the producer (plan-feature) and the consumer (implement-task) used the same description format (markdown). Proceed to hex digest comparison.

If the tags had differed (e.g., stored `sha256-adf` vs. computed `sha256-md`), the following warning would be logged: "Digest format mismatch (stored: sha256-adf, current: sha256-md) -- producer and consumer used different API access methods. Skipping integrity check." Execution would proceed normally without blocking.

### 7. Compare hex digests -- MISMATCH DETECTED

- **Expected (from comment)**: `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description)**: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

The hex digests do not match. This means the task description was modified after plan-feature created it.

### 8. Required action: alert the user and halt

Per Step 1.5 rule 4e of SKILL.md, when a digest mismatch is detected, the skill must:

1. **Alert the user** with a clear message explaining the situation:

   > **Warning: Task description integrity check failed.**
   >
   > The description for TC-9201 has been modified since plan-feature created it.
   >
   > - Expected digest (from plan-feature comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
   > - Actual digest (computed from current description): `sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
   >
   > The description may have been manually edited in Jira after the planning phase.
   >
   > Options:
   > 1. **Proceed** -- implement using the current (modified) description as-is
   > 2. **Stop** -- halt so you can re-run plan-feature to regenerate tasks with a fresh digest
   >
   > Choose (1/2):

2. **Stop execution immediately** -- do not proceed with any subsequent steps (Step 2 through Step 11) until the user responds.

### 9. Outcome depends on user choice

- **If the user chooses "Proceed" (option 1)**: continue with Step 2 (Verify Dependencies) using the current description as the specification. The modified description becomes the working specification for the remainder of the implementation. No further digest checks are performed.

- **If the user chooses "Stop" (option 2)**: halt execution entirely. The user should investigate what changed in the description, optionally re-run plan-feature to regenerate the task with an updated digest, and then re-invoke implement-task.

## Summary of key protocol behaviors demonstrated

| Aspect | Behavior |
|--------|----------|
| Comment location | Search for marker `[sdlc-workflow] Description digest:` among all issue comments |
| Multiple digest comments | Select most recent by `created` timestamp |
| Comment edit detection | Compare `created` vs `updated`; warn if edited but proceed regardless |
| Legacy format (`sha256:<hex>`) | Log warning and skip integrity check entirely |
| Format tag mismatch | Log warning and skip integrity check (different API methods) |
| Format tag match + hex match | Proceed silently with no user prompt |
| Format tag match + hex mismatch | Alert user, display both digests, offer proceed/stop, halt until response |
| No digest comment found | Log warning for backward compatibility, proceed normally |
| Script exits non-zero | Warn and skip integrity check, do not block |
