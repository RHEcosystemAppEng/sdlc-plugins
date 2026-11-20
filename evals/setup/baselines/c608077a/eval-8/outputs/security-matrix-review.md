# Security Matrix Scaffold Review (simulated)

## Discovery summary (simulated, no MCP/shell calls made)

- **Step 1 – Existing configuration**: `# Project Configuration` is present. Repository Registry has `backend` (serena_backend) and `frontend-ui` (serena_ui). Jira, Code Intelligence, Bug Configuration and Security Configuration are all present.
- **Step 2 – Serena discovery**: `serena_backend` and `serena_ui` found in the MCP tool listing. Both match the existing registry, so nothing changes.
- **Step 10 – Security Configuration**: the section exists and has no `{{placeholder}}` markers. The report is: "Security Configuration is up to date". Nothing is re-asked and CLAUDE.md is not changed.
  - Product Lifecycle: Jira version prefix `MYPRODUCT`, Vulnerability issue type `10200`, component label pattern `pscomponent:`, product pages URL configured. These are kept as written. Nothing from RHTPA is added.
  - Version Streams: `2.1.x` → Security Matrix Path `security-matrix.md`
  - Source Repositories: `backend` (https://github.com/example/backend), `frontend-ui` (https://github.com/example/frontend-ui)
- **Step 10.5 – Matrix existence check**: no file exists at `security-matrix.md` (simulated). The matrix is **missing**, so a scaffold is proposed.

## Scaffold source and expansion rules applied

- Source: plugin-root `docs/templates/security-matrix.template.md` only. The worked example `docs/templates/security-matrix.md` was **not** used.
- Expanded: only `{source-repo-name}`, `{source-ref}` and their matching `|---|` separator cells. These were expanded together into one column per Source Repository (`backend`, `frontend-ui`), plus one Source Pinning Method entry per repository.
- Left exactly as in the template:
  - all fixed headings, including `# Security Matrix — {stream} Stream` (not rewritten at runtime)
  - the fixed columns (Product Version, Build, Build Date, Notes)
  - the Container Images table
  - Ecosystem Mappings
  - Forward Pointer
  - HTML guidance comments
  - all other placeholders (`{stream}`, `{version}`, `{build}`, `{build-date}`, `{source-pinning-method}`, `{ecosystem}`, `{forward-pointer}`, and so on)
- No `<!-- Last-Updated -->` header was added. That header is set only when the matrix is populated (Step 10.6), and that step was declined.

## User decisions (simulated)

- Scaffold the missing matrix at `security-matrix.md` for stream `2.1.x`: **confirmed**.
- Write semantics: re-read the path immediately before writing and create it only if it is still absent. If the file appeared in the meantime, keep it and report that it now exists. Abort rather than overwrite.
- Step 10.6, fill in the supportability and image data: **declined**. The matrix stays a skeleton. `/triage-security` can fill it in later.

## Proposed file: `security-matrix.md` (not written to the project)

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

## Diff vs. template

```diff
-| Product Version | Build | Build Date | {source-repo-name} | Notes |
-|---|---|---|---|---|
-| {version} | {build} | {build-date} | `{source-ref}` | |
+| Product Version | Build | Build Date | backend | frontend-ui | Notes |
+|---|---|---|---|---|---|
+| {version} | {build} | {build-date} | `{source-ref}` | `{source-ref}` | |
@@
-- **{source-repo-name}**: {source-pinning-method}
+- **backend**: {source-pinning-method}
+- **frontend-ui**: {source-pinning-method}
```

## Step 11 – Validation (simulated)

- CLAUDE.md is unchanged. The required sections are present: Project Configuration, Repository Registry (4 columns), Jira Configuration (key, Cloud ID, Feature type ID), Code Intelligence with the `mcp__<instance>__<tool>` convention and Limitations, Bug Configuration, and Security Configuration with Product Lifecycle, at least one Version Stream and at least one Source Repository.
- The scaffold has a separate source column for each of `backend` and `frontend-ui`. Separator cell count (6) matches the header column count (6). There is one pinning entry per repository.
