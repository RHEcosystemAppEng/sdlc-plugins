# Proposed Scaffold Review — security-matrix.md (2.1.x stream)

## Context

- **Source CLAUDE.md:** `claude-md-configured-with-non-rhtpa-security.md`, which simulates the project's CLAUDE.md
- **Security Configuration status:** already present and fully populated (Product Lifecycle, Version Streams, Source Repositories). No changes are proposed to CLAUDE.md.
- **Jira version prefix:** `MYPRODUCT`. This is recorded for context only. The scaffold does not inject it into any heading.
- **Version Stream:** `2.1.x`
  - Konflux Release Repo: `git.downstream.example.com/my-org/product-release.2.1.z`
  - Local Path: `/home/user/product-release.2.1.z`
  - Security Matrix Path: `security-matrix.md`
- **Configured Source Repositories (in order):**
  1. `backend`: https://github.com/example/backend
  2. `frontend-ui`: https://github.com/example/frontend-ui

## Step 10.5: Existence check (simulated)

- Path checked: `security-matrix.md`, relative to the project working directory
- Result: **missing**
- Prompt: "security-matrix.md for stream 2.1.x does not exist. Scaffold it from `docs/templates/security-matrix.template.md` and write it to `security-matrix.md`?"
- User response: **Yes, confirm scaffolding.**

## Scaffold source and expansion rules applied

- Template: plugin-root `docs/templates/security-matrix.template.md`, and nothing else. The worked example `docs/templates/security-matrix.md` was NOT used.
- Expanded placeholders, and only these:
  - `{source-repo-name}` in the Supportability Matrix header row became two columns: `backend` and `frontend-ui`.
  - The matching `|---|` separator cell became two separator cells.
  - `` `{source-ref}` `` in the data row became two cells, in lockstep: `` `{source-ref}` `` for backend and `` `{source-ref}` `` for frontend-ui. Each keeps the per-repo value placeholder.
  - `- **{source-repo-name}**: {source-pinning-method}` under Source Pinning Method became one entry per repository: `backend` and `frontend-ui`.
- Left exactly as in the template:
  - All fixed headings, including `# Security Matrix — {stream} Stream`, `## Version Stream`, `## Supportability Matrix`, `#### Container Images`, `### Source Pinning Method`, `## Ecosystem Mappings` and `## Forward Pointer`. No heading was rewritten at runtime. No product-specific or RHTPA naming was introduced, and `MYPRODUCT` was not inserted into any heading.
  - Fixed columns: Product Version, Build, Build Date and Notes. Every Container Images column. Every Ecosystem Mappings column.
  - All other placeholders: `{stream}`, `{version}`, `{build}`, `{build-date}`, `{component}`, `{release-tag}`, `{release-commit-sha}`, `{image-reference}`, `{image-digest}`, `{cpe}`, `{source-pinning-method}`, `{ecosystem}`, `{repository}`, `{lock-file}`, `{check-command}`, `{upstream-branch}` and `{forward-pointer}`. These are filled later, either by the optional population step or by `/triage-security`.
  - All template HTML comments.

## Proposed file content: `security-matrix.md`

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

## Structural verification of the proposal

| Check | Result |
|---|---|
| Supportability header columns | 6: Product Version, Build, Build Date, backend, frontend-ui, Notes |
| Supportability separator cells | 6, matching the header |
| Supportability data cells | 6, matching the header. The source cells are in the same order as Source Repositories. |
| Source Pinning Method entries | 2, one each for backend and frontend-ui, using the configured short names |
| Container Images columns | 7, unchanged from the template |
| Ecosystem Mappings columns | 5, unchanged from the template and retained |
| Fixed headings | identical to the template, none rewritten |
| Other placeholders | left unexpanded |

## Write semantics (planned, NOT executed in this eval)

1. Immediately before writing, re-read `security-matrix.md`.
2. If it is still absent, create it using **create-if-absent** semantics.
3. If it has appeared since the first check, keep the current file, report "security-matrix.md now exists — not overwritten", and offer a merge proposal that needs fresh confirmation.
4. If create-if-absent cannot be guaranteed, abort rather than overwrite.

In this eval no project file was written. The proposal is recorded here only.

## Step 10.6: Optional supportability and image population

- Prompt: "Would you like me to populate the Supportability Matrix and Container Images table from release history and published-image evidence?"
- User response: **Declined.**
- Result: the population step is skipped. No release tags, SHAs, image digests or revision labels were gathered. The matrix stays a scaffold. `/triage-security` can populate it later on demand.
- The `<!-- Last-Updated: ... -->` timestamp line is not added, because the template has none and the population step did not run.
