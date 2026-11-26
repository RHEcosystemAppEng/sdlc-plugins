# Security Matrix Scaffold Review (Simulated)

## Context

- Source CLAUDE.md: `evals/setup/files/claude-md-configured-with-non-rhtpa-security.md`
- MCP tool listing: `evals/setup/files/mcp-tools-with-serena.md`
- Skill: `/sdlc-workflow:setup`, Step 10 (Security Configuration) -> Step 10.5 (Scaffold security-matrix.md) -> Step 10.6 (Optional population)

## Pre-scaffold Status (Steps 1-10.4, simulated)

| Step | Result |
|---|---|
| 1 – Read existing configuration | `# Project Configuration` present; all sections parsed |
| 2 – Serena discovery | Discovered `serena_backend`, `serena_ui` (simulated from tool listing) — both already in Repository Registry. "Repository Registry is up to date" |
| 3 – Jira Configuration | Project key, Cloud ID, Feature issue type ID all present. "Jira Configuration is up to date" |
| 5 – Code Intelligence | Naming convention, example, and Limitations for both instances present. "Code Intelligence is up to date" |
| 9 – Bug Configuration | All three fields populated. "Bug Configuration is up to date" |
| 10 – Security Configuration | Product Lifecycle (Product pages URL, Jira version prefix `MYPRODUCT`, Vulnerability issue type ID, Component label pattern, VEX field), Version Streams, and Source Repositories all populated; no `{{placeholder}}` markers. "Security Configuration is up to date" — no CLAUDE.md changes |

Note: Hierarchy Configuration and Jira Field Defaults are absent from the input CLAUDE.md; they are out of scope for this task (security matrix setup only) and are not proposed here.

## Step 10.5 – Security Matrix Existence Check

Configured Version Streams:

| Stream | Security Matrix Path | Exists? | Action |
|---|---|---|---|
| 2.1.x | `security-matrix.md` | No (missing, simulated) | Offer scaffold |

Prompt shown to the user:

> "security-matrix.md for stream **2.1.x** is missing at `security-matrix.md`. Would you like me to scaffold it from `docs/templates/security-matrix.template.md`?"

User response: **Yes** — confirmed scaffolding.

### Scaffold Source and Expansion Rules

- Template: plugin-root `docs/templates/security-matrix.template.md` only (the worked example `docs/templates/security-matrix.md` was NOT used).
- Configured Source Repositories (order preserved): `backend`, `frontend-ui`.
- Expanded in lockstep, one per Source Repository:
  - Supportability Matrix header cell `{source-repo-name}` -> `backend`, `frontend-ui`
  - Matching separator cell `---` -> two separator cells
  - Matching value cell `` `{source-ref}` `` -> two `` `{source-ref}` `` cells (one per repository column; the ref value itself stays a placeholder until populated)
  - Source Pinning Method entry `- **{source-repo-name}**: {source-pinning-method}` -> one entry per repository
- Retained unchanged: fixed columns (Product Version, Build, Build Date, Notes), Container Images table, Ecosystem Mappings table, Forward Pointer, all HTML comments, and all fixed headings — including the template's literal `# Security Matrix — {stream} Stream` heading and `{stream}` body text, which are not rewritten at runtime.
- No other placeholders (`{version}`, `{build}`, `{component}`, `{ecosystem}`, etc.) were filled — population was declined (see Step 10.6).

### Proposed Scaffold — `security-matrix.md` (stream 2.1.x)

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

### Structural Verification

- Supportability header: 6 cells; separator: 6 cells; value row: 6 cells — consistent.
- Source columns (`backend`, `frontend-ui`) match Source Repositories names exactly, in configured order.
- Source Pinning Method entries: 2, matching the 2 source columns.
- Container Images (7 columns) and Ecosystem Mappings (5 columns) unchanged from template.
- No `Last-Updated` timestamp line added (only set after a confirmed population write, per Step 10.6).

### Write Semantics (would apply in a real run)

Immediately before writing, re-read `security-matrix.md` and create it with create-if-absent semantics. If the file appeared after the initial check, preserve it, report that it now exists, and do not overwrite. If create-if-absent cannot be guaranteed, abort. In this eval, no project file is written — the scaffold is captured only in this review.

## Step 10.6 – Optional Supportability / Image Population

Prompt shown to the user:

> "Would you like me to populate the Supportability Matrix and Container Images table from release history and published-image evidence?"

User response: **No** — declined. Matrix remains a scaffold with placeholders; it can be populated later on demand by `/triage-security`. No release tags, image digests, or revision labels were read.

## Step 11 – Validation (simulated)

- `# Project Configuration` heading exists — PASS
- Repository Registry table with required columns — PASS
- Jira Configuration minimum fields — PASS
- Code Intelligence naming convention + `### Limitations` — PASS
- Bug Configuration three fields — PASS
- Security Configuration `### Product Lifecycle` required fields — PASS
- `### Version Streams` has at least one row (2.1.x) — PASS
- `### Source Repositories` has at least one row (backend, frontend-ui) — PASS
- Security matrix for 2.1.x — scaffold proposed and confirmed (simulated; not written to project files)
