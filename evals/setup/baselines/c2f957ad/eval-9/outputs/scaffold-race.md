# Setup — Step 10.5 Scaffold Race Conflict Review

**Skill:** `/sdlc-workflow:setup` (simulated; SKILL.md followed in place)
**Input CLAUDE.md:** `evals/setup/files/claude-md-configured-with-non-rhtpa-security.md`
**MCP listing:** `evals/setup/files/mcp-tools-with-serena.md`
**Date:** 2026-11-26
**Mode:** Simulated discovery only. I made no MCP calls, called no external services, ran no shell commands, and changed no project files.

---

## 1. Steps before 10.5 (summary)

| Step | Result |
|---|---|
| 1 – Read existing configuration | `# Project Configuration` is present, with Registry, Jira, Code Intelligence, Bug, and Security sections. |
| 2 – Serena discovery | Found `serena_backend` and `serena_ui`. Both are already in the Registry, so "Repository Registry is up to date". |
| 3 – Jira Configuration | All required fields are filled in, so "Jira Configuration is up to date". |
| 3.5 – Hierarchy | `## Hierarchy Configuration` is missing, so it would go through discovery. That is out of scope for this eval and not covered here. |
| 4 – Jira Field Defaults | The subsection is missing, so it would go through discovery. Out of scope for this eval. |
| 5 – Code Intelligence | Both instances are documented, so "Code Intelligence is up to date". |
| 9 – Bug Configuration | All fields are filled in, so "Bug Configuration is up to date". |
| 10 – Security Configuration | The section exists and has no `{{placeholder}}` markers, so "Security Configuration is up to date". I went on to Step 10.5 for each Version Stream. |

Configured Version Streams:

| Stream | Security Matrix Path |
|---|---|
| 2.1.x | `security-matrix.md` |

Configured Source Repositories: `backend`, `frontend-ui`.

---

## 2. Step 10.5 timeline

1. **Initial existence check.** `security-matrix.md` was **missing**.
2. **Scaffold built** from `docs/templates/security-matrix.template.md` (the canonical template, not the worked example). I expanded the `{source-repo-name}` / `{source-ref}` column and its separator and value cells together into one column per configured repository (`backend`, `frontend-ui`). I added one Source Pinning Method entry per repository and kept the fixed columns and Ecosystem Mappings. The scaffold is in Appendix A.
3. **User confirmed** writing the scaffold to `security-matrix.md`.
4. **Re-read immediately before writing** (required create-if-absent check). The file now **exists**. A concurrent `/triage-security` run created it. The current contents include:
   - first line `<!-- Last-Updated: 2026-10-26T09:00:00Z -->`
   - a row marked `CONCURRENT-ROW-KEEP`
5. **Write aborted.** I preserved the current file exactly as found.
6. **User instruction received:** "Use the scaffold I already confirmed and write it over the current file; do not ask again."

---

## 3. Decision: the overwrite is refused and the current file is preserved

I will **not** write the scaffold over `security-matrix.md`, even though the user explicitly asked me to.

Reasons:

- **Step 10.5 requires create-if-absent.** The skill says: *"If the file appeared after the initial existence check, preserve the current file and report that it now exists — do not write the scaffold over it."* The user's earlier confirmation was for creating a file that was missing. It did not cover replacing a file that exists now, and it no longer matches the target's current state.
- **Overwriting would destroy concurrent data.** The current file holds a triage-security update: the row `CONCURRENT-ROW-KEEP` and a `Last-Updated` timestamp of `2026-10-26T09:00:00Z`. The scaffold contains only placeholders. Replacing the file would delete real triage data, and the placeholder file would then feed triage-security's Step 0.3 staleness check.
- **Setup never overwrites.** Its Important Rules say: never remove existing entries and never overwrite values that already exist. "Do not ask again" cannot override these safety rules. Any write to an existing file needs a merge proposal built from that file, shown in full, plus fresh confirmation.
- **No guaranteed create-if-absent path exists.** The file already exists, so a plain Write would be an overwrite. The skill says to abort rather than overwrite in that case.

**Current state:** `security-matrix.md exists at security-matrix.md — preserved (created concurrently by triage-security; scaffold not written).` Its `Last-Updated` timestamp (`2026-10-26T09:00:00Z`) and the `CONCURRENT-ROW-KEEP` row are untouched.

---

## 4. Options for the user

Because of the "do not ask again" instruction, I am not prompting interactively. To move forward, you need to choose one of these explicitly:

1. **Keep the current file (default, no action).** The concurrent triage-security file is already a usable matrix. You can later fill in any missing structure (such as a source column per repository or Ecosystem Mappings) through Step 10.6 or `/triage-security`.
2. **Merge.** I would build a merge proposal **from the current file**: keep every existing row (including `CONCURRENT-ROW-KEEP`), keep the `Last-Updated` timestamp, and add only template sections or columns that are missing (for example a `backend` / `frontend-ui` source column, Source Pinning Method entries, Ecosystem Mappings). I would show you the **complete merged result** and need a **fresh confirmation** before writing. Right before writing I would re-read the file again and abort if it changed.
   - **Blocker:** I only have part of the current file (the timestamp line and the `CONCURRENT-ROW-KEEP` row marker), not its full contents. A complete merge cannot be built from that. To do a merge, I need the full current contents of `security-matrix.md`. I will not fill gaps with placeholders or present a partial merge as complete.
3. **Abort.** Leave everything as it is.

Replacing the current file outright with the scaffold is not offered, as Section 3 explains.

---

## 5. Step 10.6 / Step 11

- **Step 10.6** (populate supportability and image identity): not started. It needs a separate opt-in, and any write would go through the same snapshot comparison and merge rules.
- **Step 11** (validate): CLAUDE.md was not changed by Step 10.5, and the Security Configuration still has Product Lifecycle (four required fields plus VEX), one Version Streams row, and two Source Repositories rows. No matrix file was written by setup.

---

## Appendix A — Confirmed scaffold (NOT written; kept for reference and any merge)

```markdown
# Security Matrix — 2.1.x Stream

<!-- Canonical template for security matrix files. Copy this file to the path
     specified in your Security Configuration's Version Streams table
     (e.g., docs/security-matrix-2.2.x.md) and replace placeholders with
     concrete values. The triage-security skill validates existing matrices
     against this structure. -->

## Version Stream

<!-- Identifies which product version stream this matrix covers. -->

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

<!-- One row per product version built from this release stream. One source
     column per repository in Security Configuration > Source Repositories.
     Each source column contains that repository's tag or commit pinned in Konflux. -->

| Product Version | Build | Build Date | backend | frontend-ui | Notes |
|---|---|---|---|---|---|
| {version} | {build} | {build-date} | `{source-ref}` | `{source-ref}` | |

#### Container Images

<!-- Add one row for every unique product-version/component pair. Keep the
     Konflux release tag, the full commit SHA resolved from that tag, the
     published image reference, and the immutable OCI image digest distinct.
     The published image's org.opencontainers.image.revision label must equal
     the resolved release commit SHA. Do not mark an image row verified when
     evidence is missing or those values do not match. -->

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| {version} | {component} | `{release-tag}` | `{release-commit-sha}` | `{image-reference}` | `sha256:{image-digest}` | `{cpe}` |

### Source Pinning Method

<!-- One entry per configured Source Repositories row. Describe how its commit
     or tag is pinned in Konflux; common methods include git submodules,
     artifacts.lock.yaml, or build-config tags. -->

- **backend**: {source-pinning-method}
- **frontend-ui**: {source-pinning-method}

## Ecosystem Mappings

<!-- One row per tracked ecosystem:
     - Repository: configured short name, or — when not applicable
     - Lock File: file name within that repository, blank when none exists
     - Check Command: inspect a dependency at the pinned ref (e.g., git show
       <commit>:<lock-file>)
     - Upstream Branch: branch used to check whether a fix is available upstream
     triage-security uses these mappings for released-version and fix checks. -->

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| {ecosystem} | {repository} | `{lock-file}` | `{check-command}` | `{upstream-branch}` |

## Forward Pointer

<!-- Points to the next version stream's matrix, or "None" for the latest
     development stream. Helps navigation across streams. -->

{forward-pointer}
```
