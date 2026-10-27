# Step 1.5 — Description Integrity Verification (Digest Mismatch)

## 1. Retrieve Issue Comments

After fetching the task TC-9201 via `jira.get_issue(TC-9201)` and parsing the structured description in Step 1, proceed to Step 1.5 by retrieving all comments on the issue:

```
jira.get_issue_comments(TC-9201)
```

## 2. Locate the Digest Comment

Search the returned comments for any whose body starts with the marker string defined in `shared/description-digest-protocol.md`:

```
[sdlc-workflow] Description digest:
```

One matching comment is found with body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

If multiple comments matched the marker, the most recent one by `created` timestamp would be selected. In this case there is only one.

## 3. Comment Edit Detection

Compare the comment's `created` and `updated` timestamps. They are identical, so the comment has not been edited after posting. No warning is needed — proceed with digest comparison.

## 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md`
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`

The format is not the legacy untagged format (`sha256:<hex>`) — it uses the current tagged format (`sha256-md:<hex>`), so we proceed with full verification.

## 5. Compute the Current Digest

Extract the description field from the Jira issue response, write it to a temp file, and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as markdown text and outputs a tagged digest:

```
sha256-md:<actual-64-char-hex-digest>
```

## 6. Compare Format Tags

- Stored tag: `sha256-md`
- Computed tag: `sha256-md`

The format tags match — both are `sha256-md`. This means the producer and consumer used the same Jira access method (MCP/markdown). Proceed to hex digest comparison.

## 7. Compare Hex Digests

- **Expected (stored):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed):** `sha256-md:<actual-computed-digest>`

**Result: MISMATCH.** The format tags match (`sha256-md`) but the hex digests differ. This means the task description was modified after plan-feature created it.

## 8. Alert the User

> **⚠️ Description integrity check failed — digest mismatch detected.**
>
> The task description for TC-9201 has been modified since plan-feature created it.
>
> - **Expected digest (from plan-feature comment):** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest (computed from current description):** `sha256-md:<computed-hex-digest>`
>
> The description content has changed between planning and implementation. This could mean the task scope, acceptance criteria, or implementation notes were altered after the plan was reviewed and approved.
>
> **How would you like to proceed?**
>
> 1. **Proceed** — Continue implementing with the current (modified) description as-is
> 2. **Stop** — Abort implementation so you can re-run plan-feature to regenerate tasks with the updated description
>
> Please choose (1 or 2):

## 9. Stop Execution

**Execution is halted at Step 1.5.** No subsequent steps (Step 2 — Verify Dependencies, Step 3 — Transition to In Progress, Step 4 — Understand the Code, Step 5 — Create Branch, Step 6 — Implement Changes, etc.) are executed until the user responds with their decision.

- If the user chooses **1 (Proceed)**: continue to Step 2 and beyond using the current description.
- If the user chooses **2 (Stop)**: terminate the skill run entirely so the user can re-run plan-feature to regenerate task descriptions that reflect the current state.
