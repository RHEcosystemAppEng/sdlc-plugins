# Description Integrity Verification — Step 1.5 (Digest Mismatch)

## 1. Retrieve Issue Comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

## 2. Locate the Digest Comment

Search through all returned comments for those whose body starts with the marker string `[sdlc-workflow] Description digest:`. This exact prefix is defined in the shared description-digest-protocol and is how the consumer identifies digest comments among all issue comments.

In this case, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected directly. (If multiple comments matched, the most recent one by `created` timestamp would be selected.)

## 3. Comment Edit Detection

The comment's `created` and `updated` timestamps are identical. This means the comment has not been edited after initial posting -- no tampering warning is needed. Proceed with digest comparison.

## 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the format-tagged scheme (not the legacy untagged `sha256:<hex>` format), so integrity checking proceeds normally.

## 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response, write it to a temp file, and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format and outputs a tagged digest. Suppose the output is:

```
sha256-md:a3f7b2c1d9e8046f5123456789abcdef0123456789abcdef0123456789abcdef
```

## 6. Compare Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md` -- the tags match. This means both the producer (plan-feature) and the consumer (implement-task) used the same API access method (both MCP / markdown path). Proceed to hex digest comparison.

## 7. Compare Hex Digests — MISMATCH DETECTED

- **Expected (from digest comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `sha256-md:a3f7b2c1d9e8046f5123456789abcdef0123456789abcdef0123456789abcdef`

The format tags match (both `sha256-md`) but the hex hashes differ. This means the task description was **modified** after plan-feature originally created it.

## 8. Alert the User

> **Warning: Task description modified after planning**
>
> The description of TC-9201 has been modified since plan-feature created this task. The description integrity check detected a digest mismatch:
>
> - **Expected digest** (recorded by plan-feature): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from current description): `sha256-md:a3f7b2c1d9e8046f5123456789abcdef0123456789abcdef0123456789abcdef`
>
> Someone (or an automated process) changed the task description after plan-feature generated it. Implementing from a modified description may produce results inconsistent with the original plan.
>
> **How would you like to proceed?**
>
> 1. **Proceed** — continue implementing with the current (modified) description as-is
> 2. **Stop** — halt implementation so you can re-run plan-feature to regenerate tasks from the updated feature description
>
> Please choose (1 or 2):

## 9. Stop Execution

**Execution is halted at Step 1.5.** No subsequent steps are performed -- Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), Step 4 (Understand the Code), implementation planning, branching, code changes, and all other downstream steps are blocked until the user responds to the choice above.

This is a hard stop. The skill does not proceed with any work until the user explicitly chooses option 1 (proceed) or option 2 (stop to re-plan).
