# Proposed security-matrix.md Scaffold — Review

## Context

- Source CLAUDE.md: `claude-md-configured-with-non-rhtpa-security.md` (simulated project CLAUDE.md)
- Security Configuration status: present and fully populated (no `{{placeholder}}` markers) — Product Lifecycle (Jira version prefix `MYPRODUCT`), Version Streams, Source Repositories
- Version Stream: `2.1.x`
- Configured Security Matrix Path: `security-matrix.md`
- Existence check (simulated): `security-matrix.md` is **missing**
- Template used: plugin-root `docs/templates/security-matrix.template.md` (the canonical template only; `docs/templates/security-matrix.md` is a worked example and was NOT used)
- Configured Source Repositories (in table order): `backend`, `frontend-ui`

## Expansion Rules Applied

- `{source-repo-name}` header cell in the Supportability Matrix expanded into one column per Source Repository: `backend`, `frontend-ui`.
- The matching `|---|` separator cell was expanded in lockstep (one per repository column).
- The matching `` `{source-ref}` `` value cell was expanded in lockstep (one per repository column); it remains a placeholder value to be filled from release evidence.
- `- **{source-repo-name}**: {source-pinning-method}` expanded into one Source Pinning Method entry per repository, using the configured short names; `{source-pinning-method}` stays as a placeholder.
- Everything else is retained verbatim from the template: fixed columns (Product Version, Build, Build Date, Notes), the Container Images table, Ecosystem Mappings, Forward Pointer, all fixed headings (including `# Security Matrix — {stream} Stream`), and all HTML comments. No fixed template heading was rewritten.
- No Supportability, Container Images, Ecosystem, or pinning data was inferred or populated (user declined optional Step 10.6 population).
- No `<!-- Last-Updated: ... -->` timestamp line is added, since that is only set after a confirmed population in Step 10.6.

## Proposed File Content (`security-matrix.md`)

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

## Confirmation and Write Semantics

- User prompt (Step 10.5): "`security-matrix.md` for stream 2.1.x is missing. Write the scaffold above to `security-matrix.md`?" — **User confirmed.**
- Write procedure (would be applied on a real run): re-read `security-matrix.md` immediately before writing; create with **create-if-absent** semantics. If the file appeared after the initial check, preserve it, report that it now exists, and do not overwrite. If create-if-absent cannot be guaranteed, abort rather than overwrite.
- In this eval run, the scaffold was NOT written to any project file; it is presented here only.

## Optional Population (Step 10.6)

- Prompt: "Would you like me to populate the Supportability Matrix and Container Images table from release history and published-image evidence?"
- **User declined.** The matrix remains a scaffold; it can be populated later on demand by `/triage-security` during CVE investigation. No release tags, image digests, or revision labels were read.
