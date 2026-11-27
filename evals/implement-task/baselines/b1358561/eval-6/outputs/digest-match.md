# Step 1.5 – Description Integrity Verification (TC-9201)

Simulated run. No Jira, git, or Serena calls were made. This follows
`plugins/sdlc-workflow/skills/implement-task/SKILL.md` Step 1.5 and
`plugins/sdlc-workflow/shared/description-digest-protocol.md`.

## Preconditions

- Step 0 (Project Configuration): passed. The mock CLAUDE.md has a Repository Registry
  (trustify-backend / serena_backend), Jira Configuration (Project key TC, Cloud ID,
  Feature issue type ID 10142), and Code Intelligence with the
  `mcp__<serena-instance>__<tool>` naming convention.
- Step 1 (Fetch and Parse): `jira.get_issue("TC-9201")` returned a description with
  every required section (Repository, Target Branch = `main`, Description, Files to
  Modify, Files to Create, API Changes, Implementation Notes, Acceptance Criteria,
  Test Requirements, Dependencies). There is no Target PR or Bookend Type, so the mode
  is **default**.

## Procedure

1. **Retrieve comments**: `jira.get_issue_comments("TC-9201")` returns one comment:

   ```
   [sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890
   ```

2. **Locate the digest comment**: the body starts with the fixed marker
   `[sdlc-workflow] Description digest:`. Exactly one comment matches, so the
   "most recent by `created`" tie-break isn't needed. It is selected.

3. **No-digest fallback**: doesn't apply, because a digest comment exists.

4. **Digest comment found**:
   a. **Comment edit check**: the comment's `created` and `updated` timestamps are
      identical, so the comment was not edited after posting. No edit warning.
   b. **Extract the stored digest**: the value is tagged (not legacy `sha256:<hex>`).
      - Format tag: `sha256-md`
      - Hex: `a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
        (64 lowercase hex characters, a well-formed SHA-256)
   c. **Compute the current digest**: write the description field from the
      `get_issue` response to `/tmp/desc-TC-9201.txt` and run:

      ```bash
      python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
      ```

      The script exits 0. MCP returned the description as markdown, so the script
      emits `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.
      The digest is computed only with the script, never by hand.
   d. **Compare format tags**: stored `sha256-md` equals computed `sha256-md`. There
      is no format-mismatch warning.
   e. **Compare hex digests**: they are identical, so the result is a **match**.

## Outcome

- **Result: MATCH.** The description is unchanged since plan-feature created it.
- Per Step 4e, I **continue silently**: no user prompt, no warning, no extra latency.
  I don't show expected-versus-actual digests and don't offer the Proceed/Stop choice,
  because that only happens on a mismatch.
- Nothing is posted to Jira for this step, and the digest comment stays as it is.
- Execution goes straight to **Step 2 – Verify Dependencies**. Dependencies are
  "None", so it continues to Step 3 and the rest of the default-mode flow (see
  `plan.md`).

## Contrast: what would have changed the behavior

| Condition | Behavior |
|---|---|
| No digest comment | Warn "No description digest found — skipping integrity check..." and continue |
| `updated` later than `created` | Warn "Digest comment was edited after initial posting — integrity cannot be fully guaranteed." and still compare |
| Legacy `sha256:<hex>` | Warn "Legacy digest format — skipping integrity check" and continue |
| Script exits non-zero | Warn and skip the check, without blocking |
| Tag mismatch (e.g. stored `sha256-adf`, computed `sha256-md`) | Warn "Digest format mismatch — skipping integrity check" and continue |
| Hex mismatch with the same tag | Show expected and actual digests, ask Proceed or Stop, and **stop until the user answers** |
| **Hex match with the same tag (this case)** | **Continue silently** |
