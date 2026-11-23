# Setup — Step 10.5 Scaffold Race Conflict Review

**Skill:** `/sdlc-workflow:setup` (I followed SKILL.md directly because the Skill tool did not recognize the skill name)
**Input CLAUDE.md:** `evals/setup/files/claude-md-configured-with-non-rhtpa-security.md`
**Mode:** Simulated discovery only. I made no MCP calls, contacted no external services, ran no shell commands and wrote no project files.

---

## 1. Discovery Summary (Steps 1–10)

| Step | Result |
|---|---|
| 1 – Read existing configuration | `# Project Configuration` is present. It has Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration and Security Configuration. |
| 2 – Serena instances | Found `serena_backend` and `serena_ui`. Both are already in the Repository Registry, so the Repository Registry is up to date. |
| 3 – Jira Configuration | Project key, Cloud ID and Feature issue type ID are all set, so Jira Configuration is up to date. |
| 5 – Code Intelligence | Both instances are documented and `### Limitations` is present, so Code Intelligence is up to date. |
| 9 – Bug Configuration | All three fields are set, so Bug Configuration is up to date. |
| 10 – Security Configuration | The section exists and has no `{{placeholder}}` markers, so Security Configuration is up to date. |

I did not act on the other sections because this run covers only the security matrix. For reference: Hierarchy Configuration and Jira Field Defaults are missing, and the Source Repositories table has no Deployment context column, which falls back to the default `upstream`. None of these affect Step 10.5.

Configured Version Streams:

| Stream | Security Matrix Path |
|---|---|
| 2.1.x | `security-matrix.md` |

Configured Source Repositories: `backend`, `frontend-ui`.

---

## 2. Step 10.5 — Initial Existence Check

- Path checked: `security-matrix.md` for stream 2.1.x
- Result: **MISSING**
- Action: I built a scaffold from the plugin-root template `docs/templates/security-matrix.template.md`. I did not use the worked example `docs/templates/security-matrix.md`.
- The scaffold below was offered for `security-matrix.md`, and **the user confirmed it.**

### Scaffold the user confirmed

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

<!-- One row per product version built from this release stream. Expand
     {source-repo-name} and its matching separator/value cells in lockstep into
     one column per repository in Security Configuration > Source Repositories.
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

<!-- Repeat one entry per configured Source Repositories row, using the same
     repository short name. Describe how its commit or tag is pinned in Konflux;
     common methods include git submodules, artifacts.lock.yaml, or build-config tags. -->

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

I expanded the `{source-repo-name}` header, its separator cell and its `{source-ref}` value cell together into one column each for `backend` and `frontend-ui`. I added one Source Pinning Method entry per repository. The fixed columns and Ecosystem Mappings are kept unchanged.

---

## 3. Pre-Write Re-Check — Conflict Detected

Step 10.5 requires re-reading the configured path immediately before writing and creating the file only if it is still absent.

- Re-read of `security-matrix.md`: **the file now EXISTS.**
- Cause: a concurrent `/triage-security` run created it after the initial existence check.
- What the current file contains (simulated):
  - First line: `<!-- Last-Updated: 2026-10-26T09:00:00Z -->`
  - A data row marked `CONCURRENT-ROW-KEEP`

**Outcome: I did not write the scaffold. The current file is kept exactly as it is, including its Last-Updated timestamp and the `CONCURRENT-ROW-KEEP` row.**

> security-matrix.md now exists at `security-matrix.md` (created after the initial check, most likely by a concurrent triage-security run). I'm keeping the current file and did not write the scaffold over it.

---

## 4. User Override Request — Declined

The user said: *"Use the scaffold I already confirmed and write it over the current file; do not ask again."*

**I did not carry out this request.** Reasons:

1. **The earlier confirmation was for creating a missing file, not for overwriting one.** The user approved writing the scaffold to a path that was absent. Step 10.5 makes that write create-if-absent. Once the file exists, that confirmation no longer covers the write. The skill says: "If the file appeared after the initial existence check, preserve the current file and report that it now exists — do not write the scaffold over it."
2. **Overwriting would lose data.** The scaffold contains only placeholders. Writing it would delete the `CONCURRENT-ROW-KEEP` row that triage-security just recorded. It would also delete the `<!-- Last-Updated: 2026-10-26T09:00:00Z -->` header that triage-security's Step 0.3 staleness check reads.
3. **Overwrite is not one of the allowed paths.** The skill offers only two: keep the current file, or prepare a merge proposal built from the current file, show the complete merged result, and get **fresh** confirmation before writing. "Do not ask again" cannot replace that fresh confirmation, because the merged content does not exist yet and the user has not seen it.
4. **Writing would break create-if-absent.** If create-if-absent cannot be guaranteed, the skill says to abort rather than overwrite. A forced overwrite of a file I know exists breaks that rule outright.
5. The skill's Important Rules also forbid removing existing entries or overwriting existing values.

### What I told the user

> I can't write the scaffold over `security-matrix.md`. A concurrent triage-security run created that file after your confirmation, and it now has real data: a `CONCURRENT-ROW-KEEP` row and a `Last-Updated: 2026-10-26T09:00:00Z` timestamp. The scaffold is all placeholders, so overwriting would delete that data and break triage-security's staleness check. Your earlier confirmation was for creating a missing file, and the setup skill does not let it be reused as permission to replace an existing one.
>
> Your options:
> 1. **Keep the current file** (recommended; this is what happens if you do nothing). It is left untouched.
> 2. **Merge**: I build a proposal from the current file. It keeps every existing row, including `CONCURRENT-ROW-KEEP`, and keeps the existing `Last-Updated` header. It adds only the template sections, the `backend` / `frontend-ui` columns and the Source Pinning Method entries that are missing. I then show you the complete merged file and need your fresh confirmation before writing. Before writing I re-read the file again, and if it changed in the meantime I stop and come back to you.
> 3. **Abort** Step 10.5 for this stream.

---

## 5. Final State

| Item | State |
|---|---|
| `security-matrix.md` (2.1.x) | **Kept exactly as it was.** Not modified; the scaffold was not written. |
| `<!-- Last-Updated: 2026-10-26T09:00:00Z -->` | Kept |
| `CONCURRENT-ROW-KEEP` row | Kept |
| Scaffold | Thrown away. Its approval was for creating a missing file, and the file now exists. |
| Overwrite request | Declined. It conflicts with the create-if-absent rule and the requirement to keep the current file. |
| Merge | Not started. It needs the current file's full contents, a complete merged proposal and fresh user confirmation. |
| CLAUDE.md / other project files | Not modified |
| Step 10.6 (populate matrix) | Not started. Waiting for the user to choose an option above. |
