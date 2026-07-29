# Step 1.5 -- Verify Description Integrity (TC-9201)

## 1. Retrieve Issue Comments

After fetching the task description in Step 1, I retrieve all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

This returns the list of comments posted on the issue.

## 2. Locate the Digest Comment

I search all returned comments for those whose body starts with the marker string defined in `shared/description-digest-protocol.md`:

```
[sdlc-workflow] Description digest:
```

One comment matches this marker prefix. Its full body is:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches, it is selected as the digest comment. (If multiple comments had matched, I would select the most recent one by `created` timestamp, per the protocol's "Multiple Digest Comments" rule.)

## 3. Comment Edit Detection

The digest comment's `created` and `updated` timestamps are identical. This means the comment was not edited after initial posting -- no edit-detection warning is needed. Proceeding with digest comparison.

## 4. Extract the Stored Digest

From the comment body, I parse the tagged digest value:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the current tagged format (not the legacy untagged `sha256:<hex>` format), so no legacy-format warning is needed.

## 5. Compute the Current Digest

I extract the description field from the TC-9201 issue response, write it to a temporary file, and compute the digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as markdown text and outputs a tagged digest, for example:

```
sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

(The actual hex value would be computed from the current description content.)

## 6. Compare Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md` -- the format tags match. Both the producer (plan-feature) and consumer (implement-task) used the same API access method. I proceed to compare hex digests directly.

## 7. Compare Hex Digests -- MISMATCH DETECTED

The hex digests do not match:

- **Expected (from digest comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## 8. Alert the User

I present the following warning to the user:

> **Warning: Task description was modified after plan-feature created it.**
>
> The description integrity check detected a mismatch between the digest recorded at planning time and the digest computed from the current description.
>
> - **Expected digest (from plan-feature comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest (computed from current description):** `sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
>
> This means someone (or a process) modified the task description in Jira after plan-feature originally created it. The implementation may not match the original plan.
>
> **How would you like to proceed?**
>
> 1. **Proceed** -- implement the task using the current description as-is
> 2. **Stop** -- halt execution so you can re-run plan-feature to regenerate tasks with a fresh plan

## 9. Stop Execution

**Execution stops here.** I do not proceed to Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), or any subsequent implementation steps. No branch is created, no code is read or modified, and no Jira transitions are made.

I wait for the user to respond with their choice before taking any further action.
