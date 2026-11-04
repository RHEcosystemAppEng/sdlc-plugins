# Security Matrix Scaffold Review — Step 10.5

## Context

- Source of configuration: `## Security Configuration` in the existing CLAUDE.md
  (`claude-md-configured-with-non-rhtpa-security.md`)
- Jira version prefix: `MYPRODUCT` (non-RHTPA product; no product-specific naming is
  injected into the matrix)
- Version Streams configured: 1

| Stream | Konflux Release Repo | Local Path | Security Matrix Path |
|---|---|---|---|
| 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md |

- Source Repositories configured (in table order): `backend`, `frontend-ui`
- Scaffold source: plugin-root `docs/templates/security-matrix.template.md` (the canonical
  template only; `docs/templates/security-matrix.md` is a worked example and was NOT used)

## Existence check

| Stream | Configured path | Status | Action |
|---|---|---|---|
| 2.1.x | `security-matrix.md` | Missing | Scaffold offered — user **confirmed** |

## Expansion rules applied

- Only `{source-repo-name}` and `{source-ref}` were expanded, in lockstep with their
  header, separator, and value cells — one column per configured Source Repository,
  in Source Repositories table order (`backend`, then `frontend-ui`).
- `### Source Pinning Method`: the single `{source-repo-name}` entry was repeated once per
  configured Source Repository, using the same short names. `{source-pinning-method}`
  remains a placeholder (populated later from release evidence).
- Fixed columns (Product Version, Build, Build Date, Notes) retained.
- `#### Container Images` table retained verbatim (not population-time data).
- `## Ecosystem Mappings` table retained verbatim.
- Fixed template headings were NOT rewritten — including `# Security Matrix — {stream} Stream`,
  `## Version Stream`, `## Supportability Matrix`, `#### Container Images`,
  `### Source Pinning Method`, `## Ecosystem Mappings`, `## Forward Pointer`.
- All other placeholders (`{stream}`, `{version}`, `{build}`, `{build-date}`, `{component}`,
  `{release-tag}`, `{release-commit-sha}`, `{image-reference}`, `{image-digest}`, `{cpe}`,
  `{source-pinning-method}`, `{ecosystem}`, `{repository}`, `{lock-file}`, `{check-command}`,
  `{upstream-branch}`, `{forward-pointer}`) are left untouched.
- No `<!-- Last-Updated: ... -->` line added: that timestamp is only set by Step 10.6
  after a verified population, which the user declined.

## Write semantics (for the confirmed scaffold)

- Re-read `security-matrix.md` immediately before writing; create with **create-if-absent**
  semantics. If the file has appeared since the initial check, preserve it, report that
  it now exists, and do not overwrite. If create-if-absent cannot be guaranteed, abort.
- In this eval, the write is simulated only — no project file was created.

## Proposed file: `security-matrix.md` (stream 2.1.x)

```markdown
# Security Matrix — {stream} Stream

<!-- Canonical template for security matrix files. Copy this file to the path
     specified in your Security Configuration's Version Streams table
     (e.g., docs/security-matrix-2.2.x.md) and replace placeholders with
     concrete values. The triage-security skill validates existing matrices
     against this structure. -->

## Version Stream

<!-- Identifies which product version stream this matrix covers. -->

This Konflux release repo covers the **{stream}** product version stream.

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

## Structural checks

| Check | Result |
|---|---|
| Supportability header / separator / value cells each have 6 cells | Pass |
| One source column per Source Repository (`backend`, `frontend-ui`) | Pass |
| One Source Pinning Method entry per Source Repository | Pass |
| Container Images table unchanged from template (7 columns) | Pass |
| Ecosystem Mappings table unchanged from template (5 columns) | Pass |
| Fixed headings identical to template | Pass |
| No product-specific (e.g., RHTPA) names introduced | Pass |
| No Last-Updated timestamp (population not performed) | Pass |

## Step 10.6 — Populate supportability and image identity

> "Would you like me to populate the Supportability Matrix and Container Images table
> from release history and published-image evidence?"

User response: **declined**. Population skipped; the matrix can be populated later on
demand by `/triage-security` during CVE investigation.
