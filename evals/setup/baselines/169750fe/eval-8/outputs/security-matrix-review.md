# Security Matrix Scaffold Review

## Discovery Summary

**Source**: `docs/templates/security-matrix.template.md` (sole canonical scaffold)

The CLAUDE.md Security Configuration declares one Version Stream:

| Stream | Konflux Release Repo | Local Path | Security Matrix Path |
|---|---|---|---|
| 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md |

The configured Source Repositories are:

| Repository | URL |
|---|---|
| backend | https://github.com/example/backend |
| frontend-ui | https://github.com/example/frontend-ui |

**Jira version prefix**: MYPRODUCT

**Matrix file check**: `security-matrix.md` does not exist -- scaffold required.

## Proposed Scaffold

The following content will be written to `security-matrix.md`, expanded from `docs/templates/security-matrix.template.md`. The `{source-repo-name}` and `{source-ref}` placeholders have been expanded in lockstep into one column per configured Source Repository (backend, frontend-ui). All fixed template headings are carried through unchanged.

---

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

---

## User Decisions

- **Scaffold security-matrix.md for 2.1.x stream?** User confirmed: Yes.
- **Populate Supportability Matrix and Container Images from release history?** User declined. No data was fabricated; all data-row placeholders remain unfilled.

## Validation Notes

- The `Product Version` heading is carried unchanged from the canonical template. No relabeling or rewriting of fixed headings was performed.
- The Supportability Matrix has 6 header cells, 6 separator cells, and 6 data cells (Product Version, Build, Build Date, backend, frontend-ui, Notes) -- cell counts match.
- The Container Images table retains all 7 columns: Product Version, Component, Konflux Release Tag, Resolved Release Commit SHA, Image Reference, Image Digest, CPE.
- The Source Pinning Method section has one entry each for backend and frontend-ui.
- No actual MCP tools, external services, or shell commands were invoked (simulated discovery only).
