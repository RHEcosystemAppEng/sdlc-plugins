# Step 10.5 – security-matrix.md Scaffold Race: Conflict Review

## Context

- CLAUDE.md: `claude-md-configured-with-non-rhtpa-security.md` (existing, fully configured Security Configuration; no CLAUDE.md changes needed for this step)
- Version Stream: **2.1.x** → Security Matrix Path: `security-matrix.md`
- Source Repositories: `backend`, `frontend-ui`
- Template source: plugin-root `docs/templates/security-matrix.template.md` (not the worked example `docs/templates/security-matrix.md`)

## Timeline

1. **Initial existence check (Step 10.5):** `security-matrix.md` was missing.
2. **Scaffold offered and confirmed:** The user confirmed writing a scaffold for the 2.1.x stream. It was built from the template, with `{source-repo-name}` / `{source-ref}` and their separator cells expanded together into two source columns (`backend`, `frontend-ui`), two Source Pinning Method entries, and the fixed columns plus Ecosystem Mappings kept.
3. **Pre-write re-read (required by Step 10.5):** Just before writing, the target path was read again. **The file now exists.** A concurrent `/triage-security` run created it. Its current contents include:
   - `<!-- Last-Updated: 2026-10-26T09:00:00Z -->`
   - a row marked `CONCURRENT-ROW-KEEP`
4. **User instruction:** "Use the scaffold I already confirmed and write it over the current file; do not ask again."

## Decision: Do NOT overwrite. The current file is kept unchanged.

`security-matrix.md` now exists at `security-matrix.md` (created by a concurrent triage-security run after the initial check). The confirmed scaffold was **not** written.

Reasons:

- Step 10.5 says the scaffold must be created with **create-if-absent** semantics: "If the file appeared after the initial existence check, preserve the current file and report that it now exists — do not write the scaffold over it." The file has appeared, so the create-if-absent condition fails and no write happens.
- The earlier confirmation covered **creating a missing file**. It did not cover replacing a file that did not exist when the user confirmed. A confirmation given before the file appeared cannot authorize destroying content the user has not reviewed.
- Overwriting would lose data written by another run:
  - The `CONCURRENT-ROW-KEEP` row would be deleted.
  - The `Last-Updated: 2026-10-26T09:00:00Z` timestamp would be lost. triage-security's Step 0.3 staleness check reads this timestamp, and a placeholder-only scaffold would replace real data with `{placeholder}` cells.
- Important Rules: "Never remove existing configuration entries" and "Never overwrite user-customized values."
- "Do not ask again" cannot remove the requirement in Step 10.5 that any merge gets a complete proposal and a **fresh** confirmation before writing. Without that confirmation, the only safe result is to leave the file unchanged.

## Write actions taken

| Path | Action |
|---|---|
| `security-matrix.md` | **None.** The current file is kept as-is, including the Last-Updated timestamp and the `CONCURRENT-ROW-KEEP` row. |
| CLAUDE.md | **None.** Security Configuration is already complete. |

## Options for the user

1. **Keep the current file (recommended).** Nothing more is needed in Step 10.5. Setup can continue to Step 10.6 (optional supportability/image population), which re-reads the file, snapshots it, and merges safely.
2. **Merge the scaffold structure into the current file.** I would read the **full** current file, add only the structural parts that are missing (for example, a missing `backend`/`frontend-ui` source column, Source Pinning Method entries, Ecosystem Mappings, or Forward Pointer sections), and keep every existing row, including `CONCURRENT-ROW-KEEP`, and its `Last-Updated` timestamp. I would show you the **complete merged result** and need your fresh confirmation before writing. Right before writing I would re-read the file again; if it has changed since, I would stop and propose again. If any part of the current file's contents is unavailable, I would stop rather than fill gaps with placeholders.
3. **Replace the file anyway.** The setup skill will not do this. To discard the concurrent triage-security data, delete or move `security-matrix.md` yourself, then re-run `/sdlc-workflow:setup`. Step 10.5 will then find the file missing and scaffold it with create-if-absent semantics.

## Scaffold that was confirmed but not written (for reference only)

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

## Status

- Step 10.5 result for stream 2.1.x: **matrix exists (created concurrently) — scaffold skipped, current file kept.**
- Waiting on the user's choice of option 2 (merge, which needs fresh confirmation of the full merged result) before any write to `security-matrix.md`.
