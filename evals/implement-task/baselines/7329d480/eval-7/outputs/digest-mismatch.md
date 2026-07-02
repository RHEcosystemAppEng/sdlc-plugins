# Step 1.5 -- Verify Description Integrity

## 1. Retrieve Issue Comments

After fetching the TC-9201 task in Step 1, retrieve all comments on the issue:

```
jira.get_issue_comments("TC-9201")
```

## 2. Locate the Digest Comment

Search all returned comments for those whose body starts with the marker string defined in `shared/description-digest-protocol.md`:

```
[sdlc-workflow] Description digest:
```

One comment matches. Its body is:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches, it is selected directly (no need to resolve multiple matches by `created` timestamp).

## 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. They are identical, so the comment has not been edited after initial posting. No warning is needed; proceed with digest comparison.

## 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the format-tagged format (not the legacy untagged `sha256:<hex>` format), so the integrity check proceeds normally.

## 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response, write it to a temporary file, and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects that the input is markdown text and outputs a tagged digest, for example:

```
sha256-md:e4a1f7c9b2d805634aef1290dc37b5468e12fa0983c7d6510ab2e9f483017d52
```

## 6. Compare Format Tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match. Both the producer (plan-feature) and consumer (implement-task) used the same Jira access method. Proceed to hex digest comparison.

## 7. Compare Hex Digests -- MISMATCH DETECTED

- **Expected (from digest comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `sha256-md:e4a1f7c9b2d805634aef1290dc37b5468e12fa0983c7d6510ab2e9f483017d52`

The hex digests do not match. This means the task description for TC-9201 was modified after plan-feature originally created it.

## 8. Alert the User

Present the following message to the user:

> **Description integrity check failed for TC-9201.**
>
> The task description has been modified since plan-feature created this task. The stored digest from the plan-feature comment does not match the digest computed from the current description.
>
> **Expected digest (stored by plan-feature):**
> `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
>
> **Actual digest (computed from current description):**
> `sha256-md:e4a1f7c9b2d805634aef1290dc37b5468e12fa0983c7d6510ab2e9f483017d52`
>
> **How would you like to proceed?**
>
> 1. **Proceed** -- implement using the current (modified) description as-is
> 2. **Stop** -- abort so you can re-run plan-feature to regenerate tasks with an up-to-date description and digest

## 9. Stop Execution

Execution stops here. The skill does NOT proceed to Step 2 (Verify Dependencies), does NOT create an implementation plan, does NOT create a branch, and does NOT make any code changes. No further steps are taken until the user responds with their choice.
