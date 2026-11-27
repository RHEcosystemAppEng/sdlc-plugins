# Security Matrix Scaffold Review (setup skill, Step 10.5)

## Context

- Source configuration: `claude-md-configured-with-non-rhtpa-security.md` (simulated project CLAUDE.md)
- Jira version prefix (Security Configuration > Product Lifecycle): **MYPRODUCT** (preserved as configured; non-RHTPA product)
- Version Stream: **2.1.x**
  - Konflux Release Repo: `git.downstream.example.com/my-org/product-release.2.1.z`
  - Local Path: `/home/user/product-release.2.1.z`
  - Security Matrix Path: `security-matrix.md`
- Source Repositories (in configured order): `backend`, `frontend-ui`

## Existence check

- `security-matrix.md` (configured path for stream 2.1.x): **missing** (simulated) → scaffold proposed.

## Template used

- Sole canonical scaffold: plugin-root `docs/templates/security-matrix.template.md`.
- `docs/templates/security-matrix.md` is a worked example only and was **not** used as a template or fallback.

## Expansion rules applied

- Expanded only `{source-repo-name}` / `{source-ref}` and their matching separator cells, in lockstep, into one column per configured source repository (`backend`, `frontend-ui`), and one Source Pinning Method entry per repository.
- Fixed template headings and column labels are carried through unchanged (including the product-neutral `Product Version` header). No heading was relabeled or rewritten.
- All other placeholders (`{stream}`, `{version}`, `{build}`, `{component}`, `{source-pinning-method}`, `{ecosystem}`, `{forward-pointer}`, etc.) are left as-is; no supportability, image, or ecosystem data was fabricated.
- Container Images table and Ecosystem Mappings table retained.
- Cell-count check: Supportability Matrix header / separator / data rows each have 6 cells. Container Images header / separator / data rows each have 7 cells.

## Proposed scaffold for `security-matrix.md`

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

## User decisions

- Scaffold `security-matrix.md` for stream 2.1.x: **confirmed** by the user (after this review was shown).
- Write procedure on confirmation: re-read the configured path right before writing and create with create-if-absent semantics; if the file has appeared since the initial check, keep it, report it now exists, and do not write the scaffold over it.
- Step 10.6 (populate Supportability Matrix and Container Images from release history / published-image evidence): **declined** by the user. Placeholders stay unpopulated, no data was fabricated, and the `Last-Updated` timestamp was not set. `/triage-security` can populate the matrix later when needed.

## Simulation note

This is an eval simulation. No project file (including `security-matrix.md` or CLAUDE.md) was written; the proposed scaffold exists only in this review.
