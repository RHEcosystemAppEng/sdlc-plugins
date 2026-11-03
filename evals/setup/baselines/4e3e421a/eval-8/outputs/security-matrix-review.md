# Security Matrix Scaffold Review (Step 10.5)

## Context (simulated discovery)

- Input CLAUDE.md: `claude-md-configured-with-non-rhtpa-security.md`
- Security Configuration: present and fully populated (no `{{placeholder}}` markers) — "Security Configuration is up to date"
- Jira version prefix (Product Lifecycle): **MYPRODUCT** (preserved as configured; non-RHTPA product)
- Version Streams:

  | Stream | Konflux Release Repo | Local Path | Security Matrix Path |
  |---|---|---|---|
  | 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md |

- Source Repositories (in configured order): `backend`, `frontend-ui`
- Existence check for `security-matrix.md`: **missing** (simulated) — scaffold required

## Scaffold source

- Template used: plugin-root `docs/templates/security-matrix.template.md` (canonical template only)
- NOT used: `docs/templates/security-matrix.md` (worked example, reference only)
- Expansion performed: only `{source-repo-name}` / `{source-ref}` placeholders and their matching separator cells, expanded in lockstep into one column per Source Repository and one Source Pinning Method entry per Source Repository.
- Not rewritten: fixed template headings and fixed column headers (e.g., the product-neutral `Product Version` header is carried through unchanged; the `# Security Matrix — {stream} Stream` title and all other placeholders such as `{stream}`, `{version}`, `{build}`, `{component}`, `{ecosystem}`, `{forward-pointer}` are left as-is for later population).
- Retained: Container Images table (all 7 columns), Source Pinning Method section, Ecosystem Mappings table, Forward Pointer section.

### Column-count check (Supportability Matrix)

| Row | Cells |
|---|---|
| Header | 6 (Product Version, Build, Build Date, backend, frontend-ui, Notes) |
| Separator | 6 |
| Data | 6 |

## Proposed file: `security-matrix.md` (stream 2.1.x)

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

## User decisions

- Scaffold offer: "security-matrix.md is missing for stream 2.1.x. Write the scaffold above to `security-matrix.md`?" — **User confirmed.**
- Write semantics (simulated): re-read the configured path immediately before writing; still absent, so create with create-if-absent semantics. If it had appeared, the existing file would be preserved and the scaffold skipped. In this eval no project file is actually written.
- Step 10.6 offer: "Would you like me to populate the Supportability Matrix and Container Images table from release history and published-image evidence?" — **User declined.** Supportability rows, Container Images rows, Source Pinning Method values, and Ecosystem Mappings remain as template placeholders; no `Last-Updated` timestamp is set. The matrix can be populated later by `/triage-security`.
