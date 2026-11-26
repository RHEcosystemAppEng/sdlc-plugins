# Step 1.5 – Description Integrity Verification (TC-9201)

Protocol reference: `plugins/sdlc-workflow/shared/description-digest-protocol.md`

## Preconditions (Steps 0 and 1)

- **Step 0:** The project CLAUDE.md (`claude-md-mock.md`) has `## Repository Registry` (trustify-backend -> `serena_backend`, path `./`), `## Jira Configuration` (Project key TC, Cloud ID, Feature issue type ID 10142), and `## Code Intelligence` (tool naming convention `mcp__<serena-instance>__<tool>`). Validation passes.
- **Step 1:** TC-9201 is fetched with `jira.get_issue(TC-9201)`. All required sections are present: Repository, Target Branch (`main`), Description, Files to Modify, Files to Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies. There is no Target PR and no Bookend Type, so this runs the default flow.

## Step 1.5 procedure

1. **Get comments:** `jira.get_issue_comments(TC-9201)` returns one comment.

2. **Find the digest comment:** the body starts with the fixed marker `[sdlc-workflow] Description digest:`, so it counts as a digest comment:
   ```
   [sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
   ```
   Only one comment matches, so no tie-break by most recent `created` timestamp is needed.

3. **No-digest branch:** does not apply because a digest comment exists. The backward-compatibility warning is not shown.

4. **Digest comment found:**
   - **a. Check whether the comment was edited:** `created` and `updated` are identical, so the comment has not been edited since it was posted. No "Digest comment was edited after initial posting" warning is shown.
   - **b. Read the stored digest:** it uses the tagged format, not the legacy `sha256:<hex>` form, so the legacy-format skip does not apply.
     - Format tag: `sha256-md`
     - Hex digest: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890` (64 hex characters)
   - **c. Compute the current digest:** write the description field from the `get_issue` response to `/tmp/desc-TC-9201.txt` and run:
     ```bash
     python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
     ```
     The exit code is 0. The input is markdown (the MCP path), so the script strips leading and trailing whitespace before hashing and prints `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`, as the scenario specifies.
   - **d. Compare format tags:** stored `sha256-md` equals computed `sha256-md`. The tags match, so the format-mismatch skip does not apply.
   - **e. Compare hex digests:** the stored and computed hex values are the same, so the result is a **MATCH**.

## Outcome

- The description has not changed since plan-feature created it, and the digest comment was never edited.
- Following the skill's rule for a match, the skill **continues silently**: it does not prompt the user, does not ask "proceed or stop", shows no warning, and adds no delay.
- Execution goes straight to **Step 2 – Verify Dependencies**. TC-9201 lists "Depends on: None", so there is nothing to check, and the skill continues to Step 3 (assign to current user, transition to In Progress) and the rest of the implementation (see `plan.md`).

## Branches not taken (for reference)

| Condition | Action | Applies? |
|---|---|---|
| No digest comment | Warn "No description digest found — skipping integrity check..." and continue | No |
| `updated` > `created` | Warn "Digest comment was edited after initial posting — integrity cannot be fully guaranteed." and still compare | No (timestamps identical) |
| Legacy `sha256:<hex>` | Warn "Legacy digest format — skipping integrity check" and continue | No |
| Script exits non-zero | Warn and skip the check without blocking | No |
| Tag mismatch (md vs adf) | Warn "Digest format mismatch — skipping integrity check" and continue | No |
| Hex mismatch | Show expected vs actual digest, ask Proceed/Stop, **stop until the user answers** | No |
| **Hex match** | **Continue silently** | **Yes** |
