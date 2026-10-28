# Security Matrix Scaffold Review -- 2.1.x Stream

## Scaffold Source

Canonical template: `docs/templates/security-matrix.template.md`

No other template or fallback was used. The scaffold below is produced
entirely by expanding that template.

## Discovery Summary

**Simulated discovery only -- no MCP tools, external services, or shell
commands were invoked.**

Configuration read from the project CLAUDE.md:

- **Stream**: 2.1.x
- **Konflux Release Repo**: git.downstream.example.com/my-org/product-release.2.1.z
- **Local Path**: /home/user/product-release.2.1.z
- **Security Matrix Path**: security-matrix.md
- **Jira version prefix**: MYPRODUCT
- **Source Repositories**: backend, frontend-ui

The matrix file at `security-matrix.md` was not found (simulated). The
user confirmed scaffolding the missing matrix from the canonical template.

The user **declined** optional supportability and container-image data
population. No supportability rows, image rows, or ecosystem mapping data
have been fabricated. All data-row placeholders are preserved verbatim from
the template.

## Expansions Applied

Only the following template placeholders were expanded; all fixed headings
(including `Product Version`) are carried through unchanged from the
canonical template:

| Placeholder | Expansion |
|---|---|
| `{stream}` (title and body text) | 2.1.x |
| `{source-repo-name}` (Supportability Matrix header) | Two columns: `backend`, `frontend-ui` |
| Supportability Matrix separator row | Extended to match the expanded header (6 cells) |
| `{source-ref}` (Supportability Matrix data row) | Duplicated to two cells: `` `{source-ref}` `` per source repo |
| `{source-repo-name}` (Source Pinning Method) | Two entries: `backend`, `frontend-ui` |

No heading text was rewritten at runtime. The `Product Version` column
label comes directly from the template and is used as-is.

## Proposed Scaffold

The following content would be written to `security-matrix.md` in the
release repository:

---

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

---

## Validation Checklist

- [x] Template source is `docs/templates/security-matrix.template.md` (canonical)
- [x] `Product Version` heading used as-is from template (not `RHTPA Version`)
- [x] Jira version prefix `MYPRODUCT` preserved in configuration
- [x] Supportability Matrix has dynamic columns for both source repos (backend, frontend-ui)
- [x] Header row (6 cells), separator row (6 cells), and data row (6 cells) all match
- [x] Container Images table retained with all 7 columns: Product Version, Component, Konflux Release Tag, Resolved Release Commit SHA, Image Reference, Image Digest, CPE
- [x] Source Pinning Method has one entry for backend and one for frontend-ui
- [x] User declined optional population -- no data fabricated
- [x] No fixed headings rewritten at runtime
- [x] No actual project file written before user confirmation
