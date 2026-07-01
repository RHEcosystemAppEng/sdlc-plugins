# Step 1.5 -- Description Integrity Verification for TC-9201

## Context

Task TC-9201 ("Add advisory severity aggregation service and endpoint") was fetched
from Jira in Step 1. Step 1.5 requires verifying that the task description has not
been modified since plan-feature created it, using the digest protocol defined in
`plugins/sdlc-workflow/shared/description-digest-protocol.md`.

## Procedure

### 1. Retrieve issue comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search through the returned comments for any whose body starts with the marker
string `[sdlc-workflow] Description digest:`. In this case, one comment is found
with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Only one comment matches, so it is selected directly. If multiple comments matched,
the protocol requires selecting the most recent one by `created` timestamp.

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. In this scenario, the
timestamps are identical, meaning the comment has not been edited since it was
posted. No warning is needed -- proceed with digest comparison.

If `updated` were later than `created`, the following warning would be surfaced:
"Digest comment was edited after initial posting -- integrity cannot be fully
guaranteed."

### 4. Parse the stored digest

Extract the format tag and hex digest from the comment body:

- **Full tagged value:** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Format tag:** `sha256-md`
- **Hex digest (stored/expected):** `0000000000000000000000000000000000000000000000000000000000000000`

The format tag is `sha256-md` (not the legacy untagged `sha256:<hex>` format), so
the integrity check proceeds normally. If the legacy format had been detected, a
warning would be logged ("Legacy digest format detected -- skipping integrity
check") and execution would continue without blocking.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text
from the Description section). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is fetched as
markdown text (via MCP), the script outputs a tagged digest in the form:

```
sha256-md:<64-char-hex>
```

For this scenario, suppose the computed output is:

```
sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

(This is an illustrative example -- the actual hash would be computed from the
current description content.)

### 6. Compare format tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match. Both the producer (plan-feature) and the consumer
(implement-task) used the same Jira access method (MCP, which returns markdown),
so a direct hex digest comparison is valid.

If the tags had differed (e.g., stored `sha256-adf` vs. computed `sha256-md`),
the protocol requires logging a warning ("Digest format mismatch -- skipping
integrity check") and proceeding normally without blocking.

### 7. Compare hex digests -- MISMATCH DETECTED

- **Expected (from comment):** `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

The hex digests do NOT match. This means the task description was modified after
plan-feature created it and recorded the digest.

### 8. Alert the user

The following alert is presented to the user:

---

**WARNING: Description integrity check FAILED for TC-9201.**

The task description has been modified since plan-feature created it. The digest
recorded at creation time does not match the current description content.

| | Digest |
|---|---|
| **Expected** (from plan-feature comment) | `sha256-md:0000000000000000000000000000000000000000000000000000000000000000` |
| **Actual** (computed from current description) | `sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Someone (a human editor or another automation) modified the Jira task description
after plan-feature generated it. The implementation may no longer match the original
plan.

**How would you like to proceed?**

1. **Proceed** -- implement using the current (modified) description as-is
2. **Stop** -- halt implementation so you can re-run plan-feature to regenerate tasks with a fresh plan

Please choose (1 or 2):

---

### 9. STOP -- Await user response

**Execution is halted immediately.** No subsequent steps are performed:

- Step 2 (Verify Dependencies) is NOT executed
- Step 3 (Transition to In Progress) is NOT executed
- Step 4 (Understand the Code) is NOT executed
- Step 5 (Create Branch) is NOT executed
- Steps 6-11 (Implementation, Testing, Commit, Jira update) are NOT executed

The skill waits for the user to choose option 1 or 2 before taking any further
action. This prevents implementing against a description that may have diverged
from the original plan, which could result in work that conflicts with other
tasks generated from the same plan-feature run.

## Summary of Decision Points

| Check | Result | Action |
|---|---|---|
| Digest comment found? | Yes (1 comment matches marker) | Proceed to parse |
| Comment edited? | No (created == updated) | No warning needed |
| Legacy format? | No (tagged as `sha256-md`, not bare `sha256:`) | Proceed to compare |
| Format tags match? | Yes (both `sha256-md`) | Proceed to hex comparison |
| Hex digests match? | **No** -- hashes differ | Alert user, offer choice, STOP |
