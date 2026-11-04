# Step 1.5 – Description Integrity Verification (TC-9201)

Protocol reference: `plugins/sdlc-workflow/shared/description-digest-protocol.md`

## 1. Retrieve issue comments

```
jira.get_issue_comments("TC-9201")
```

Result (simulated): one comment.

| Field | Value |
|---|---|
| Body | `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890` |
| created | T (identical to updated) |
| updated | T (identical to created) |

## 2. Locate the digest comment

I search for comments whose body starts with the fixed marker
`[sdlc-workflow] Description digest:`. Exactly one comment matches, so there is no
need to pick the most recent by `created` timestamp. The "no digest found"
backward-compatibility path does not apply.

## 3. Check for comment editing (4a)

`created` and `updated` are both present and identical. That means the comment has
not been edited since it was posted, so no "Digest comment was edited after initial
posting" warning is raised.

## 4. Extract the stored digest (4b)

- Full tagged value: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
- Format tag: `sha256-md` (the markdown/MCP path)
- Hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890` (64 lowercase hex chars, valid length)
- The digest is tagged, not the legacy untagged `sha256:<hex>` form, so the legacy-format skip does not apply.

## 5. Compute the current digest (4c)

I write the description field returned by `jira.get_issue("TC-9201")` to a temp file
and hash it with the project script. I do not compute SHA-256 by hand.

```bash
python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
```

- Exit code: 0, so no "skip integrity check" warning is needed.
- Output (assumed per eval scenario): `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`

## 6. Compare format tags (4d)

Stored `sha256-md` and computed `sha256-md` are the same, so there is no format
mismatch and I go on to compare the hex digests.

## 7. Compare hex digests (4e)

Stored hex equals computed hex: **MATCH**.

## Outcome

- The description is unchanged since plan-feature created it.
- I **proceed silently** to Step 2 (Verify Dependencies). There is no user prompt,
  no warning and no extra latency. I do not show the proceed/stop choice, because
  that choice is only for a hex mismatch.
- No Jira comment is posted for this step. The match produces no user-visible
  output except an optional internal log line, e.g. "Description digest verified
  (sha256-md) — integrity OK".
- Implementation continues with the full plan in `plan.md`.

### Contrast with the other branches (not taken here)

| Condition | Behavior |
|---|---|
| No digest comment | Warn "No description digest found — skipping integrity check..." and proceed |
| `updated` > `created` | Warn "Digest comment was edited after initial posting — integrity cannot be fully guaranteed." and still compare |
| Legacy `sha256:<hex>` | Warn "Legacy digest format — skipping integrity check" and proceed |
| Script exits non-zero | Warn and skip the check, without blocking |
| Tag mismatch (adf vs md) | Warn "Digest format mismatch — skipping integrity check" and proceed |
| Hex mismatch | Show expected vs actual digest, ask the user to Proceed or Stop, and **stop until the user answers** |
| **Hex match (this case)** | **Proceed silently** |
