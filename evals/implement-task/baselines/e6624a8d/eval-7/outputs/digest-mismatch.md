# Step 1.5 — Verify Description Integrity: Digest Mismatch Handling

## Context

Task: TC-9201 — "Add advisory severity aggregation service and endpoint"

After fetching and parsing the task description in Step 1, Step 1.5 verifies that the description has not been modified since plan-feature created it. The Jira issue has one comment posted by a previous plan-feature run with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

## Procedure

### 1. Retrieve Issue Comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the Digest Comment

Search the returned comments for any whose body starts with the marker string defined in `shared/description-digest-protocol.md`:

```
[sdlc-workflow] Description digest:
```

One comment is found matching this marker prefix. Its full body is:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

Since only one comment matches the marker, it is selected directly. (If multiple comments had matched, the most recent by `created` timestamp would be selected per the protocol's "Multiple Digest Comments" rule.)

### 3. Comment Edit Detection

Per the description-digest-protocol, compare the comment's `created` and `updated` timestamps to detect whether the digest comment itself was tampered with after posting. In this scenario, the `created` and `updated` timestamps are identical — the comment was **not edited** after initial posting. No edit warning is needed. Proceed to digest comparison.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`
- **Full stored digest:** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`

This is not a legacy untagged format (`sha256:<hex>`) — the `sha256-md` tag is present, so no legacy warning is needed and the integrity check proceeds normally.

### 5. Compute the Current Digest

Extract the current description from the TC-9201 issue response (as fetched in Step 1), write it to a temporary file, and compute its digest using the script:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is markdown text (not ADF JSON), the script strips leading and trailing whitespace, computes the SHA-256 hash, and outputs a format-tagged digest:

```
sha256-md:<computed-hex-digest>
```

If the script exits non-zero, we would warn and skip the integrity check without blocking execution. In this scenario, the script succeeds and returns the computed digest.

### 6. Compare Format Tags

Per the protocol, compare format tags before comparing hex digests:

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags **match** (both `sha256-md`), confirming that the producer (plan-feature) and consumer (implement-task) used the same Jira access method (markdown text). Proceed to compare the hex digests directly.

(If the tags had differed — e.g., stored `sha256-adf` vs computed `sha256-md` — a warning about different API access methods would be logged and the integrity check would be skipped entirely, proceeding normally without blocking.)

### 7. Compare Hex Digests — MISMATCH DETECTED

The hex digests do **not** match:

```
Expected (from digest comment): sha256-md:0000000000000000000000000000000000000000000000000000000000000000
Actual   (computed from current): sha256-md:<computed-hex-digest>
```

The stored digest (all zeros) does not equal the digest computed from the current description content. This indicates that the task description was modified after plan-feature originally created it.

### 8. Alert the User

Per Step 1.5(4)(e) of the SKILL.md, the following alert is displayed to the user:

---

**Warning: Task description modified after planning.**

The description of TC-9201 has been modified since plan-feature created this task. The stored digest does not match the digest computed from the current description.

- **Expected digest** (recorded by plan-feature): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual digest** (computed from current description): `sha256-md:<computed-hex-digest>`

Someone or something changed the description between the planning and implementation phases. The implementation plan may no longer be aligned with what was originally planned.

**How would you like to proceed?**

1. **Proceed** — Continue implementing with the current (modified) description as-is
2. **Stop** — Abort implementation so you can review the changes and re-run plan-feature to regenerate tasks from the updated feature description

Choose (1/2):

---

### 9. STOP Execution — Await User Response

**Execution halts immediately at this point.** No subsequent steps are performed until the user responds:

- Step 2 (Verify Dependencies) is NOT executed.
- Step 3 (Transition to In Progress and Assign) is NOT executed.
- Step 4 (Understand the Code) is NOT executed.
- Step 5 (Create Branch) is NOT executed.
- Steps 6-11 are NOT executed.
- No implementation planning, code changes, branching, commits, or Jira transitions occur.
- No plan.md is produced.

The skill waits for the user's explicit choice before taking any further action:

- If the user chooses **option 1 (Proceed):** execution resumes from Step 2, using the current (modified) description as the specification.
- If the user chooses **option 2 (Stop):** execution terminates entirely. The user can re-run plan-feature to regenerate tasks with a fresh digest that matches the updated description.

## Summary

| Check | Result |
|---|---|
| Digest comment found? | Yes -- one comment matches `[sdlc-workflow] Description digest:` marker |
| Legacy untagged format? | No -- tagged as `sha256-md`, not bare `sha256:` |
| Comment edited after posting? | No -- `created` equals `updated` |
| Format tags match? | Yes -- both `sha256-md` |
| Stored digest | `sha256-md:0000000000000000000000000000000000000000000000000000000000000000` |
| Computed digest | `sha256-md:<computed-hex-digest>` (different from stored) |
| Digests match? | **No -- MISMATCH** |
| Action | Alert user with expected vs actual digests, offer proceed/stop choice, halt execution until user responds |
