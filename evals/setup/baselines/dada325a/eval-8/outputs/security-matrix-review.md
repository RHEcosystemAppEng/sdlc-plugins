# Proposed security-matrix.md Scaffold — Review

## Context

- Skill: `/sdlc-workflow:setup` (executed from `plugins/sdlc-workflow/skills/setup/SKILL.md`)
- Input CLAUDE.md: `claude-md-configured-with-non-rhtpa-security.md`
- Security Configuration: already fully populated (Jira version prefix `MYPRODUCT`, no `{{placeholder}}` markers) — reported "Security Configuration is up to date"; no changes to CLAUDE.md.
- Version Stream: `2.1.x` → Security Matrix Path `security-matrix.md`
- Source Repositories (from Security Configuration): `backend`, `frontend-ui`
- Simulated existence check: `security-matrix.md` is **missing** → scaffold offered (Step 10.5)
- User response: **confirmed** scaffolding the missing matrix
- Template source: plugin-root `docs/templates/security-matrix.template.md` only (the worked example `docs/templates/security-matrix.md` was NOT used)

## Expansion Rules Applied

- `{source-repo-name}` header cell in the Supportability Matrix expanded in lockstep into one column per configured Source Repository: `backend`, `frontend-ui` (in Security Configuration order).
- Matching separator cell `|---|` duplicated once per expanded column.
- Matching value cell `` `{source-ref}` `` duplicated once per expanded column.
- `- **{source-repo-name}**: {source-pinning-method}` in Source Pinning Method expanded into one entry per repository (`backend`, `frontend-ui`); `{source-pinning-method}` left as a placeholder (no release evidence — population declined).
- Fixed columns (Product Version, Build, Build Date, Notes), the Container Images table, Ecosystem Mappings, Forward Pointer, and all template headings and comments are retained verbatim. No headings were rewritten (including the title heading, which keeps its template `{stream}` token; no product-specific or RHTPA-specific wording was introduced).
- No `<!-- Last-Updated: ... -->` line added: Step 10.6 population was declined, so no timestamp is set.

## Write Semantics (on confirmation)

Re-read `security-matrix.md` immediately before writing; create with create-if-absent semantics. If the file appeared after the initial check, preserve it and report it exists rather than overwriting. (In this eval, no actual project file is written.)

## Proposed File Content — `security-matrix.md`

````markdown
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
````

## Step 10.6 — Supportability / Image Population

Prompt: "Would you like me to populate the Supportability Matrix and Container Images table from release history and published-image evidence?"

User response: **declined**. Skipped to Step 11. No release tags, image digests, revision labels, or pinning methods were collected; remaining placeholders stay for later population by `/triage-security`.
