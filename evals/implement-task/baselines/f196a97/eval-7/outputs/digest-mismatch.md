# Step 1.5 — Description Integrity Verification: Digest Mismatch Handling

## 1. Retrieve Issue Comments

After fetching TC-9201 in Step 1, retrieve all comments on the issue:

```
jira.get_issue_comments("TC-9201")
```

## 2. Locate the Digest Comment

Search all returned comments for bodies starting with the marker string:

```
[sdlc-workflow] Description digest:
```

One matching comment is found with body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

If multiple comments matched the marker, the most recent one by `created` timestamp would be selected. In this case there is only one.

## 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this scenario they are identical, meaning the comment has not been edited after initial posting. No warning is needed — proceed to digest comparison.

(If `updated` were later than `created`, a warning would be surfaced: "Digest comment was edited after initial posting — integrity cannot be fully guaranteed." The comparison would still proceed.)

## 4. Extract the Stored Digest

Parse the tagged digest from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

This is not a legacy untagged format (`sha256:<hex>`), so legacy handling does not apply.

## 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response (the markdown description text). Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as markdown text and outputs a tagged digest:

```
sha256-md:a3b1f9c8e2d74a6b50c8f1e3d9a7b2c4e6f80123456789abcdef0123456789ab
```

(This is the actual digest of the current description content.)

## 6. Compare Format Tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags match. Both producer and consumer used the same Jira access method (markdown). Proceed to hex digest comparison.

(If the tags differed — e.g., stored `sha256-adf` vs computed `sha256-md` — a warning would be logged about different API access methods and the integrity check would be skipped. That is not the case here.)

## 7. Compare Hex Digests — MISMATCH DETECTED

- **Expected (from digest comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `sha256-md:a3b1f9c8e2d74a6b50c8f1e3d9a7b2c4e6f80123456789abcdef0123456789ab`

The hex digests do NOT match. This means the task description was modified after plan-feature created it.

## 8. Alert the User

The following alert is presented to the user:

---

> **Description integrity check: MISMATCH**
>
> The description of TC-9201 has been modified since plan-feature created it. The digest recorded at planning time does not match the current description content.
>
> **Expected digest (from plan-feature comment):**
> `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
>
> **Actual digest (computed from current description):**
> `sha256-md:a3b1f9c8e2d74a6b50c8f1e3d9a7b2c4e6f80123456789abcdef0123456789ab`
>
> The description may have been manually edited in Jira after planning. Implementing a modified description risks diverging from the original plan.
>
> How would you like to proceed?
>
> 1. **Proceed** — implement using the current (modified) description as-is
> 2. **Stop** — halt implementation so you can re-run plan-feature to regenerate tasks from the updated feature description
>
> Please choose (1/2):

---

## 9. STOP EXECUTION

Execution halts immediately at this point. No subsequent steps are performed — no dependency verification (Step 2), no Jira transition (Step 3), no code inspection (Step 4), no branch creation (Step 5), no implementation (Step 6), no tests (Step 7), and no commit (Step 10).

The skill waits for the user's explicit response before taking any further action:

- **If the user chooses 1 (Proceed):** Implementation continues from Step 2 using the current description content, accepting the risk that it differs from what was originally planned.
- **If the user chooses 2 (Stop):** The skill terminates. The user can re-run plan-feature to regenerate tasks that reflect the updated feature description, then re-invoke implement-task on the newly created task.
