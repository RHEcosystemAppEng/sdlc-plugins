# Step 1.5 – Description Integrity Verification (TC-9201)

Protocol: `shared/description-digest-protocol.md`

## 1. Retrieve issue comments

```
jira.get_issue_comments(TC-9201)
```

Result (as given by the scenario): one comment.

| Field | Value |
|---|---|
| Body | `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890` |
| created | T |
| updated | T (identical to created) |

## 2. Locate the digest comment

The body starts with the fixed marker `[sdlc-workflow] Description digest:`, so it is the
digest comment. Only one comment matches, so the "pick the most recent by `created`" rule
for multiple matches does not come into play. This comment is selected.

## 3. No-digest fallback

Not applicable. A digest comment exists, so the "No description digest found" warning is
not emitted.

## 4. Digest comment found

### 4a. Comment edit check

`created` and `updated` are both present and equal, so the comment has not been edited since
it was posted. No "Digest comment was edited after initial posting" warning is emitted.

### 4b. Extract the stored digest

- Tagged value: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Format tag: `sha256-md` (markdown, the MCP access path)
- Hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890` (64 hex chars)
- The value is tagged, not the legacy `sha256:<hex>` form, so the legacy-format skip does
  not apply.

### 4c. Compute the current digest

Take the description field from the `jira.get_issue(TC-9201)` response, write it to a temp
file, and hash it with the project script. Do not compute SHA-256 by hand.

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

- Check the exit code. A non-zero exit would mean: warn and skip the integrity check
  without blocking. Here, per the scenario, the script exits 0.
- Script output (per the scenario):
  `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

### 4d. Compare format tags

Stored tag `sha256-md` equals computed tag `sha256-md`. Both sides used the same
representation (markdown), so the "Digest format mismatch" skip does not apply and the hex
digests are compared directly.

### 4e. Compare hex digests

Stored hex equals computed hex, so the digests **match**.

## Outcome

- **The digests match. Proceed silently.** The description has not changed since
  plan-feature created it.
- No warning is logged, the user gets no prompt or confirmation question, and the
  expected/actual digests are not shown. The match path adds no latency.
- The proceed/stop choice (Proceed as-is vs. Stop and re-run plan-feature) is **not**
  offered. That choice exists only for a hex mismatch.
- No Jira comment is posted for this check, and the digest comment is left unchanged.
- Execution continues straight to **Step 2 – Verify Dependencies**. TC-9201 lists
  "Depends on: None", so that check passes trivially. Then Step 3 (assign and move to
  In Progress) and the rest of the workflow run, as laid out in `plan.md`.
