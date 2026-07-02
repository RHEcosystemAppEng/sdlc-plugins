# Step 1.5 -- Description Integrity Verification (Mismatch Handling)

## 1. Locate the Digest Comment

After fetching issue TC-9201 in Step 1, retrieve all comments on the issue:

```
jira.get_issue_comments(TC-9201)
```

Search through the returned comments for any whose body starts with the marker string `[sdlc-workflow] Description digest:`, as defined in `shared/description-digest-protocol.md`. If multiple comments match this marker (e.g., from plan-feature re-runs), select the most recent one by `created` timestamp.

In this case, one comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

## 2. Check for Comment Editing

Compare the comment's `created` and `updated` timestamps. In this case they are identical, so the comment has not been edited since it was posted. Proceed with digest comparison.

## 3. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the modern tagged format (not the legacy untagged `sha256:<hex>` format), so proceed with comparison.

## 4. Compute the Current Digest

Extract the description field from the TC-9201 issue response. Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format and outputs a tagged digest. Suppose the script outputs:

```
sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2
```

## 5. Compare Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md`. The format tags match, so proceed to compare hex digests directly.

## 6. Compare Hex Digests -- MISMATCH DETECTED

The hex digests do not match:

- **Expected** (from plan-feature digest comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual** (computed from current description): `sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`

## 7. Alert the User and Stop Execution

Present the following alert to the user:

> **Description integrity check failed.** The task description for TC-9201 was modified after plan-feature created it.
>
> - **Expected digest** (recorded by plan-feature): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from current description): `sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`
>
> The description content has changed since plan-feature generated this task. This may indicate manual edits, re-planning without updating the digest, or unintended modification.
>
> **Options:**
> 1. **Proceed** -- continue implementing with the current (modified) description as-is
> 2. **Stop** -- halt implementation so you can re-run plan-feature to regenerate tasks with a fresh digest
>
> Choose (1/2):

**Execution stops here.** No subsequent steps are taken -- Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), implementation planning, branching, code changes, and all other downstream work are blocked until the user responds with their choice. This follows the same pause-and-ask pattern used when the task description is incomplete: the skill presents the issue, offers options, and waits for explicit user direction before proceeding.
