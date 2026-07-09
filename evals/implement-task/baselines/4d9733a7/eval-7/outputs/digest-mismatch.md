# Step 1.5 -- Verify Description Integrity (TC-9201)

## 1. Retrieve Issue Comments

After fetching the task in Step 1, retrieve all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

## 2. Locate the Digest Comment

Search through the returned comments for any whose body starts with the marker string defined in `shared/description-digest-protocol.md`:

```
[sdlc-workflow] Description digest:
```

One matching comment is found with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

If multiple comments matched the marker, the most recent one by `created` timestamp would be selected. In this case there is only one.

## 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this case the two timestamps are identical, which means the comment has not been edited since it was posted. No edit-detection warning is needed. Proceed to digest comparison.

(If `updated` had been later than `created`, a warning would be surfaced: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed." If the timestamps were absent from the API response, this check would be skipped silently.)

## 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The digest uses the current tagged format (`sha256-md`), not the legacy untagged format (`sha256:<hex>`), so no legacy-format warning is needed.

## 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (the markdown text fetched via `jira.get_issue`). Write it to a temporary file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as plain-text markdown and outputs a tagged digest, for example:

```
sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

(The actual hex value would be whatever SHA-256 produces from the current description content.)

## 6. Compare Format Tags

The stored tag is `sha256-md` and the computed tag is `sha256-md` -- they match. Proceed to hex digest comparison.

(If the tags had differed -- e.g., stored `sha256-adf` vs. computed `sha256-md` -- a warning would be logged: "Digest format mismatch (stored: sha256-adf, current: sha256-md) -- producer and consumer used different API access methods. Skipping integrity check." and execution would proceed normally without blocking.)

## 7. Compare Hex Digests -- MISMATCH DETECTED

The stored hex digest and the computed hex digest do not match:

- **Expected (from digest comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## 8. Alert the User

The following message is displayed to the user:

> **Description integrity check failed.**
>
> The task description for TC-9201 was modified after plan-feature created it. The description digest recorded at planning time does not match the current description content.
>
> - **Expected digest (from plan-feature comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest (computed from current description):** `sha256-md:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
>
> Please choose how to proceed:
>
> 1. **Proceed** -- continue implementing with the current (modified) description as-is
> 2. **Stop** -- halt so you can re-run plan-feature to regenerate tasks from the updated feature description
>
> Choose (1/2):

## 9. Halt Execution

Execution stops immediately at this point. The skill does NOT proceed to Step 2 (Verify Dependencies), does NOT create an implementation plan, does NOT create a branch, and does NOT begin any code changes.

No further steps are taken until the user explicitly responds with their choice. If the user chooses option 1 (Proceed), implementation continues from Step 2 onward using the current description. If the user chooses option 2 (Stop), the skill terminates and the user is expected to re-run plan-feature before re-invoking implement-task.
