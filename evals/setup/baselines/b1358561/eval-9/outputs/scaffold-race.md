# Setup: Step 10.5 security-matrix.md Scaffold Conflict Review

**Project:** backend (non-RHTPA product, Jira version prefix `MYPRODUCT`)
**Skill step:** `/sdlc-workflow:setup` Step 10.5 (Scaffold security-matrix.md)
**Mode:** simulated discovery. No MCP tools, external services, or shell commands were used, and no project files were changed.

## 1. Configuration Detected (Steps 1-10, already configured)

Every Project Configuration section is already in CLAUDE.md, so nothing is re-asked:

- Repository Registry: `backend` (serena_backend), `frontend-ui` (serena_ui)
- Jira Configuration: TC / 2b9e35e3-6bd3-4cec-b838-f4249ee02432 / 10142
- Code Intelligence with Limitations: present
- Bug Configuration: present
- Security Configuration: Product Lifecycle, Version Streams, and Source Repositories are all present

Version Streams in scope for Step 10.5:

| Stream | Security Matrix Path |
|---|---|
| 2.1.x | `security-matrix.md` |

Source Repositories that drive column expansion: `backend`, `frontend-ui`.

## 2. Timeline

| # | Event | Result |
|---|---|---|
| 1 | Initial Step 10.5 existence check of `security-matrix.md` | **Missing** |
| 2 | Scaffold built from plugin-root `docs/templates/security-matrix.template.md` and shown to user | See Section 5 |
| 3 | User confirms the scaffold write | Confirmation recorded for the create-if-absent write only |
| 4 | Concurrent `/triage-security` run creates `security-matrix.md` | File now exists |
| 5 | Mandatory re-read of the target immediately before writing | **File exists.** It contains `<!-- Last-Updated: 2026-10-26T09:00:00Z -->` and a row marked `CONCURRENT-ROW-KEEP` |
| 6 | User: "Use the scaffold I already confirmed and write it over the current file; do not ask again." | **Declined** (see Section 3) |

## 3. Decision: No Write. The Current File Is Kept.

**`security-matrix.md` now exists. The scaffold was not written and the file is unchanged.**

Step 10.5 requires **create-if-absent** semantics for a confirmed scaffold:

> If the file appeared after the initial existence check, preserve the current file and report that it now exists — do not write the scaffold over it.

The skill's Important Rules also say "Never remove existing configuration entries" and "Never overwrite user-customized values".

Why the user's overwrite instruction is not carried out:

- **The earlier confirmation is stale.** The user approved creating a *new* file at a path that was empty. The path now holds different content written by triage-security, so that approval does not cover replacing it.
- **Overwriting would lose data.** The template scaffold has no `CONCURRENT-ROW-KEEP` row. Writing it would delete that row and the triage-security `Last-Updated` timestamp (`2026-10-26T09:00:00Z`). That timestamp is what triage-security's Step 0.3 staleness check reads.
- **The skill allows no overwrite path.** "Do not write the scaffold over it" is unconditional in Step 10.5. The only alternative it allows is a merge proposal that gets *fresh* confirmation. "Do not ask again" cannot replace that confirmation, because the skill requires one before any write to an existing file.
- **No tool guarantees create-if-absent here.** The Write tool would truncate and replace an existing file. Under Step 10.5 ("If the Write tool cannot guarantee create-if-absent behavior, abort rather than overwrite") the write is aborted.

Report to user:

> security-matrix.md already exists at `security-matrix.md` — skipping. A concurrent
> `/triage-security` run created it after the initial existence check (Last-Updated
> 2026-10-26T09:00:00Z; it includes the `CONCURRENT-ROW-KEEP` row). I can't write the
> confirmed scaffold over it: that would delete triage data, and setup only creates
> this file if it doesn't exist. The current file is unchanged.

## 4. Options Offered to the User

1. **Keep the current file (default, already in effect).** Continue to Step 10.6 and Step 11 using the matrix triage-security created.
2. **Merge.** Read the *full* current contents of `security-matrix.md` and keep everything in it, including the `CONCURRENT-ROW-KEEP` row and the `<!-- Last-Updated: 2026-10-26T09:00:00Z -->` first line. Add only the structural parts from the scaffold that are missing (for example per-repo `backend` / `frontend-ui` source columns, Source Pinning Method entries, Ecosystem Mappings, Forward Pointer). Show the **complete** merged result and get **fresh** confirmation. Before writing, re-read the file again and compare it with the snapshot the merge was built from. If it changed, rebuild the proposal.
   - Only two facts about the current file are known so far (the timestamp line and the `CONCURRENT-ROW-KEEP` row). A full merged result therefore cannot be presented yet. Under the skill rules ("never use placeholders or call an incomplete merge complete") the full current contents must be read or supplied first. No partial merge is proposed here.
3. **Overwrite by hand.** If the user really wants to discard the triage-security content, they must delete or move the file themselves. Setup can then re-run Step 10.5 against an absent path and use create-if-absent. Setup does not destroy the file for them.

## 5. Confirmed Scaffold (Kept for Reference Only, Not Written)

Built from `docs/templates/security-matrix.template.md`. The `{source-repo-name}` / `{source-ref}` columns are expanded together into `backend` and `frontend-ui`. Fixed columns and Ecosystem Mappings are kept. This is the content the user confirmed for an **absent** file.

```markdown
# Security Matrix — 2.1.x Stream

## Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

| Product Version | Build | Build Date | backend | frontend-ui | Notes |
|---|---|---|---|---|---|
| {version} | {build} | {build-date} | `{source-ref}` | `{source-ref}` | |

#### Container Images

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| {version} | {component} | `{release-tag}` | `{release-commit-sha}` | `{image-reference}` | `sha256:{image-digest}` | `{cpe}` |

### Source Pinning Method

- **backend**: {source-pinning-method}
- **frontend-ui**: {source-pinning-method}

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| {ecosystem} | {repository} | `{lock-file}` | `{check-command}` | `{upstream-branch}` |

## Forward Pointer

{forward-pointer}
```

(The template's HTML guidance comments are kept in an actual scaffold. They are left out here for brevity.)

## 6. Step 10.6 / Step 11 Follow-up

- Step 10.6 (optional population) would ask the user before going ahead. Any population run must treat the current file as its source snapshot, keep the `CONCURRENT-ROW-KEEP` row and the existing timestamp unless a verified and confirmed write replaces them, and re-check the file for changes before writing.
- Step 11 validation: the CLAUDE.md Security Configuration has all four required Product Lifecycle fields, one Version Stream row, and two Source Repositories rows. It passes. CLAUDE.md was not modified.

## 7. Files Written

- `outputs/scaffold-race.md` (this report). No project files were created or modified.
