# Step 1.5 — Verify Description Integrity: Digest Mismatch Handling

## Context

Task: TC-9201 — "Add advisory severity aggregation service and endpoint"

After fetching and parsing the task description in Step 1, Step 1.5 verifies description integrity before any implementation work begins. The Jira issue has one comment posted by a previous plan-feature run with the body:

```
[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000000
```

## Procedure

### 1. Retrieve Issue Comments

Fetch all comments on TC-9201:

```
jira.get_issue_comments("TC-9201")
```

### 2. Locate the Digest Comment Using the Marker String

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

Per the protocol, compare the comment's `created` and `updated` timestamps to detect post-hoc editing. In this scenario, the `created` and `updated` timestamps are identical — the comment was **not edited** after initial posting. No edit warning is needed. Proceed with digest comparison.

### 4. Extract the Stored Digest

Parse the tagged digest value from the comment body:

- **Format tag:** `sha256-md` (indicates the description was hashed as markdown text)
- **Hex digest:** `0000000000000000000000000000000000000000000000000000000000000000`
- **Full stored digest:** `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`

### 5. Compute the Current Digest

Write the current description of TC-9201 to a temporary file and compute its digest using the `scripts/sha256-digest.py` script, as required by the protocol:

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

The script auto-detects the input format. Since the description is markdown text (not ADF JSON), the script strips leading and trailing whitespace, computes the SHA-256 hash, and outputs a format-tagged digest:

```
sha256-md:<computed-hash>
```

The computed digest is a different 64-character hex value because the description content was modified after plan-feature created the task.

### 6. Compare Format Tags

Per the protocol, compare the format tags before comparing hex digests:

- **Stored tag:** `sha256-md`
- **Computed tag:** `sha256-md`

The format tags **match** (both `sha256-md`), meaning the producer and consumer used the same Jira access method (markdown text). Proceed to compare the hex digests directly.

(If the tags had differed — e.g., stored `sha256-adf` vs computed `sha256-md` — we would log a warning about different API access methods and skip the integrity check entirely, proceeding normally.)

### 7. Compare Hex Digests — MISMATCH DETECTED

The hex digests do **not** match:

```
Expected (from comment): sha256-md:0000000000000000000000000000000000000000000000000000000000000000
Actual (computed):        sha256-md:<computed-hash>
```

This indicates that the task description was modified after plan-feature originally created the task.

### 8. Alert the User

The following alert is displayed to the user:

---

**Warning: Task description modified after planning.**

The description of TC-9201 has been modified since plan-feature created this task. The description integrity check failed — the stored digest does not match the digest computed from the current description.

- **Expected digest** (recorded by plan-feature): `sha256-md:0000000000000000000000000000000000000000000000000000000000000000`
- **Actual digest** (computed from current description): `sha256-md:<computed-hash>`

The task description was changed after plan-feature generated it. The implementation plan may no longer be aligned with what was originally planned. Someone (or something) modified the description between planning and implementation.

**How would you like to proceed?**

1. **Proceed** — Continue implementing with the current (modified) description as-is
2. **Stop** — Abort implementation so you can review the changes and re-run plan-feature to regenerate tasks from the updated feature description

Choose (1/2):

---

### 9. STOP Execution — Await User Response

**Execution halts immediately at this point.** No subsequent steps are performed until the user responds:

- Step 2 (Verify Dependencies) is NOT executed.
- Step 3 (Transition to In Progress) is NOT executed.
- Step 4 (Understand the Code) is NOT executed.
- Step 5 (Create Branch) is NOT executed.
- No implementation planning, code changes, branching, commits, or Jira transitions occur.
- No plan.md is produced.

The skill waits for the user's explicit choice before taking any further action. This follows the same pause-and-ask pattern used for incomplete description handling — execution is blocked until the user responds.

- If the user chooses **option 1 (Proceed):** execution resumes from Step 2, using the current (modified) description.
- If the user chooses **option 2 (Stop):** execution terminates entirely. The user can re-run plan-feature to regenerate tasks with a fresh digest matching the updated description.

## Summary

| Check | Result |
|---|---|
| Digest comment found? | Yes -- one comment matches `[sdlc-workflow] Description digest:` marker |
| Comment edited after posting? | No -- `created` equals `updated` |
| Format tags match? | Yes -- both `sha256-md` |
| Stored digest | `sha256-md:0000000000000000000000000000000000000000000000000000000000000000` |
| Computed digest | `sha256-md:<computed-hash>` (different from stored) |
| Digests match? | **No -- MISMATCH** |
| Action | Alert user with expected vs actual digests, offer proceed/stop choice, halt execution |
