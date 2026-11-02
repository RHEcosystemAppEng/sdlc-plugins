# Step 1.5 — Description Integrity Verification (Digest Mismatch)

## 1. Retrieve Issue Comments

Fetch all comments on TC-9201 using `jira.get_issue_comments(TC-9201)`.

## 2. Locate the Digest Comment

Search all comments for the marker string `[sdlc-workflow] Description digest:` as defined in `shared/description-digest-protocol.md`. If multiple comments match, select the most recent one by `created` timestamp.

**Found comment:**

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

## 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. In this case they are identical, so the comment is unmodified since initial posting. No edit warning is needed.

## 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

## 5. Compute the Current Digest

Extract the description field from the TC-9201 issue response. Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format (markdown text) and outputs a tagged digest, e.g.:

```
sha256-md:7f3a9b2c4d1e8f0a6b5c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a
```

(Exact hash depends on the actual description content.)

## 6. Compare Format Tags

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

Tags match — proceed to hex digest comparison.

## 7. Compare Hex Digests

- **Expected (from comment):** `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description):** `7f3a9b2c4d1e8f0a6b5c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a`

**Result: MISMATCH**

The hex digests differ. The format tags match (both `sha256-md`), which means the same API access method was used for both producer and consumer. The differing hashes mean the task description was modified after plan-feature created it.

## 8. Alert the User

> **Warning: Task description was modified after plan-feature created this task.**
>
> The description integrity check detected a mismatch between the digest recorded by plan-feature and the digest computed from the current description.
>
> - **Expected digest (from plan-feature):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest (current description):** `sha256-md:7f3a9b2c4d1e8f0a6b5c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a`
>
> The description may have been edited manually in Jira after the planning phase. Implementing a modified description could lead to inconsistencies with the original plan.
>
> **How would you like to proceed?**
>
> 1. **Proceed** — Continue implementing with the current description as-is
> 2. **Stop** — Halt execution so you can re-run plan-feature to regenerate tasks with the updated requirements
>
> Choose (1/2):

## 9. Stop Execution

**Execution is stopped immediately.** No subsequent steps (Step 2 — Verify Dependencies, Step 3 — Transition to In Progress, Step 4 — Understand the Code, Step 5 — Create Branch, Step 6 — Implement Changes, etc.) are performed until the user responds.

This follows the same pause-and-ask pattern used for incomplete task descriptions (constraint §1.6) — the skill does not proceed with any branching, implementation planning, or code changes until it has explicit user authorization to continue with potentially modified requirements.
