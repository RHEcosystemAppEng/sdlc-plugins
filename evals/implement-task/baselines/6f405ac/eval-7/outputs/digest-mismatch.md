# Step 1.5 — Verify Description Integrity: Digest Mismatch Handling

## Context

- **Task**: TC-9201 — Add advisory severity aggregation service and endpoint
- **Digest comment found**: `[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Comment timestamps**: `created` and `updated` are identical (comment was not edited after posting)
- **Format tags**: Both stored and computed digests use `sha256-md` (tags match)
- **Hex digests**: The stored hex hash (`0000...0000`) differs from the hex hash computed from the current task description

## Step-by-Step Verification Process

### 1. Retrieve issue comments

Fetch all comments on TC-9201 using:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the digest comment

Search all returned comments for bodies starting with the marker string `[sdlc-workflow] Description digest:`. One comment matches:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected (if multiple matched, the most recent by `created` timestamp would be selected).

### 3. Comment edit detection

Compare the comment's `created` and `updated` timestamps. They are identical, so the comment was not edited after initial posting. No warning is needed — proceed to digest comparison.

### 4. Extract the stored digest

Parse the tagged digest value from the comment body:

- **Format tag**: `sha256-md`
- **Hex digest**: `0000000000000000000000000000000000000000000000000000000000000000`

The format is not the legacy untagged format (`sha256:<hex>`) — it uses the current tagged format (`sha256-md:<hex>`), so no legacy warning is needed.

### 5. Compute the current digest

Extract the description field from the TC-9201 issue response (the markdown text of the description). Write it to a temp file and compute the digest:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input as markdown text and outputs a tagged digest, e.g.:

```
sha256-md:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890
```

### 6. Compare format tags

- **Stored tag**: `sha256-md`
- **Computed tag**: `sha256-md`

The format tags match. Both the producer (plan-feature) and consumer (implement-task) used the same Jira access method (both got markdown). Proceed to hex digest comparison.

### 7. Compare hex digests

- **Expected (from comment)**: `0000000000000000000000000000000000000000000000000000000000000000`
- **Actual (computed from current description)**: `abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890`

**MISMATCH** — the hex digests differ. The task description was modified after plan-feature created it.

## Action Taken: Alert User and Stop Execution

Because the format tags match but the hex digests differ, this is a confirmed description modification. The skill alerts the user and stops execution immediately, following the same pause-and-ask pattern used for incomplete descriptions.

The following message is presented to the user:

---

> **Description integrity check failed for TC-9201.**
>
> The task description has been modified since plan-feature created it. The digest recorded at planning time does not match the current description content.
>
> - **Expected digest** (from plan-feature comment): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
> - **Actual digest** (computed from current description): `sha256-md:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890`
>
> This means someone (or something) modified the task description after the planning phase produced it. The implementation may not match the original plan.
>
> **How would you like to proceed?**
>
> 1. **Proceed** — implement using the current (modified) description as-is
> 2. **Stop** — abort so you can re-run plan-feature to regenerate tasks from the updated feature description
>
> Please choose (1 or 2):

---

**Execution is stopped immediately.** No subsequent steps are performed — Step 2 (Verify Dependencies), Step 3 (Transition to In Progress), Step 4 (Understand the Code), Step 5 (Create Branch), Step 6 (Implement Changes), and all later steps are skipped until the user responds.

## Rationale

The description digest protocol exists to guard against silent tampering between planning and implementation phases. When the digest mismatches:

- The implementation might diverge from what was planned and reviewed
- The acceptance criteria or implementation notes may have changed in ways that invalidate the original plan
- The user needs to make an informed decision about whether to trust the modified description or re-plan

This mirrors the handling of incomplete descriptions (missing required sections) — in both cases, the skill stops and asks the user before proceeding, rather than silently continuing with potentially incorrect or unauthorized changes.

The comment's `created` and `updated` timestamps being identical confirms the digest comment itself was not tampered with — the modification occurred on the description only, which is the expected scenario this check is designed to catch.
