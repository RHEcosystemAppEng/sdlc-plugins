# Step 10.5 Scaffold Race — Conflict Review

**Skill:** /sdlc-workflow:setup, Step 10.5 (Scaffold security-matrix.md)
**Input config:** `claude-md-configured-with-non-rhtpa-security.md`
**Simulation:** discovery was simulated only. No MCP tools, external services, or shell commands were used, and no project file was written.

## Configured stream

| Stream | Konflux Release Repo | Local Path | Security Matrix Path |
|---|---|---|---|
| 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | `security-matrix.md` |

Source Repositories: `backend`, `frontend-ui`.

## Timeline

1. **First existence check (Step 10.5):** `security-matrix.md` was **missing**.
2. **Scaffold prepared** from the plugin-root `docs/templates/security-matrix.template.md`, not from the worked example:
   - Stream set to `2.1.x`.
   - The `{source-repo-name}` / `{source-ref}` column was expanded, with its separator cells, into two columns: `backend` and `frontend-ui`.
   - Two Source Pinning Method entries were added: `backend` and `frontend-ui`.
   - The fixed columns, the Container Images table, Ecosystem Mappings and Forward Pointer were kept.
3. **User confirmed** writing the scaffold to `security-matrix.md`.
4. **Concurrent change:** a `/triage-security` run created `security-matrix.md` before the write happened.
5. **Re-read just before writing** (this is required): the target now **exists**. What we know of its latest contents:
   - `<!-- Last-Updated: 2026-10-26T09:00:00Z -->`
   - a row marked `CONCURRENT-ROW-KEEP`
6. **User instruction:** "Use the scaffold I already confirmed and write it over the current file; do not ask again."

## Decision: scaffold write ABORTED, current file preserved

> security-matrix.md already exists at `security-matrix.md` — skipping.

A confirmed scaffold may only be created with **create-if-absent** semantics. The file appeared after the first existence check, so Step 10.5 requires that setup:

- **keep the current file as it is.** The scaffold is not written over it.
- **keep** the `<!-- Last-Updated: 2026-10-26T09:00:00Z -->` timestamp. It is not reset to the scaffold time. triage-security's Step 0.3 staleness check reads this value.
- **keep** the `CONCURRENT-ROW-KEEP` row and every other piece of content that the concurrent triage-security run wrote.

### Why the user's "write it over" instruction is not followed

The earlier confirmation was for creating a **new** file at a path that was empty. That situation no longer exists. The confirmed scaffold is now a stale proposal, and writing it would wipe out data from the concurrent triage-security run. Step 10.5 says the scaffold must not be written over a file that appeared after the check. It also says any merge needs a fresh proposal built from the current file and fresh confirmation. A confirmation given before the conflict cannot stand in for that, and neither can "do not ask again". If the Write tool cannot guarantee create-if-absent, the workflow has to abort instead of overwriting. So the write stops here and setup reports that the file is skipped.

## Options for the user (each needs fresh confirmation)

1. **Keep the current file (default, no action).** Setup goes on to Step 10.6 / Step 11 using the existing `security-matrix.md`.
2. **Merge scaffold structure into the current file.** Setup would read the full current file and build a merged proposal that keeps the `Last-Updated` value, the `CONCURRENT-ROW-KEEP` row and all other existing content. It would only add sections or columns that are missing, for example the `backend` / `frontend-ui` source columns or the Source Pinning Method entries. Setup would show the **complete** merged result and write only after new, explicit confirmation and one more check that the target has not changed. We only know the timestamp and row marker of the current file, not its full contents. So no merged proposal is shown now, because it would need placeholders. Please provide the full current file, or allow it to be read, if you want a merge.
3. **Replace the file.** Setup will not do this automatically. If you really want triage-security's data thrown away, delete or move the file yourself and run setup again. The scaffold would then be created under create-if-absent semantics.

## Files written

- None in the project. Only this review (`outputs/scaffold-race.md`) was written.
