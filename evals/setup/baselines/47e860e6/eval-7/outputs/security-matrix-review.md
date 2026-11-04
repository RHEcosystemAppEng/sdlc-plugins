# Security Matrix Review — 2.1.x Stream (`security-matrix.md`)

Simulated `/sdlc-workflow:setup` run, Steps 10.5 and 10.6. No MCP tools, external
services, or shell commands were invoked. No project files were modified.

## 1. Configuration status (Step 1 / Step 10)

`## Security Configuration` exists and contains no `{{placeholder}}` markers:

- Product Lifecycle: all four required fields set (Product pages URL, Jira version prefix
  `MYPRODUCT`, Vulnerability issue type ID `10200`, Component label pattern `pscomponent:`),
  plus VEX Justification custom field `customfield_12345`. The other optional fields are
  absent. That is allowed.
- Version Streams: one row, `2.1.x` -> `git.downstream.example.com/my-org/product-release.2.1.z`,
  local path `/home/user/product-release.2.1.z`, matrix path `security-matrix.md`.
- Source Repositories: `backend`, `frontend-ui`. There is no Deployment Context column. That
  column is optional and defaults to `upstream`.

Result: **Security Configuration is up to date.** It was not changed. Existing values are
never overwritten.

## 2. Step 10.5 — Scaffold `security-matrix.md`

- Existence check: `security-matrix.md` is **missing** (as described in the scenario).
- Scaffold source: plugin-root `docs/templates/security-matrix.template.md`, the canonical
  template. `docs/templates/security-matrix.md` is a worked example and was not used as
  the scaffold.
- Expansion: the `{source-repo-name}` / `{source-ref}` cells and their separator cells were
  expanded together, giving one column per configured Source Repository (`backend`,
  `frontend-ui`). There is one Source Pinning Method entry per repository. The fixed columns,
  Container Images table, and Ecosystem Mappings section are kept.
- User confirmation: **confirmed** (per task).
- Write semantics: re-read `security-matrix.md` immediately before writing and create it only
  if it is still absent. If the file had appeared in the meantime, the scaffold would not be
  written and the current file would be kept. In this simulation the file is still absent at
  the re-read, so the scaffold below is the proposed new file content (not actually written).

### Proposed scaffold (create-if-absent)

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

## 3. Step 10.6 — Populate supportability and image identity

The user accepted population using the evidence in `security-matrix-image-identity.md`.

### 3.1 Container Images — revision-label verification

There is one row per unique Product Version / Component pair. The Konflux release tag,
resolved full SHA, image reference, immutable digest, and CPE are kept as separate values.

| # | Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | `org.opencontainers.image.revision` | Result |
|---|---|---|---|---|---|---|
| 1 | 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | MATCH (verified) |
| 2 | 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | MATCH (verified) |
| 3 | 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | `fedcba9876543210fedcba9876543210fedcba98` | **MISMATCH (unresolved)** |

**Row 3 is unresolved.** The published image
`registry.example.test/trustify/api:2.1.1-rhel10`
(`sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc`) has a revision label
of `fedcba9876543210fedcba9876543210fedcba98`. The full SHA resolved from Konflux release tag
`v0.3.13` is `89abcdef0123456789abcdef0123456789abcdef`. The two do not match, so this image
cannot be shown to be built from the tagged release commit.

Other observations (informational, not blocking):
- Release evidence has no 2.1.1 `api-rhel9` image. Rows are only added for pairs that have
  evidence. The setup skill does not infer a missing row. Please confirm whether 2.1.1 shipped
  a rhel9 image.
- Both 2.1.0 images share CPE `cpe:2.3:a:example:trustify_api:2.1.0:...`. Their digests differ,
  so the rows are still distinct. They are recorded exactly as published.

### 3.2 Proposed populated matrix (PENDING — NOT WRITTEN)

This proposal is shown for review only. Under Step 10.6.3, a mismatch leaves the matrix
unchanged until corrected evidence is verified. Nothing will be written: not the populated
content, not a partial subset of the verified rows, and not the `Last-Updated` timestamp.
Row 3 is shown with its evidence values and flagged. It would only be committed after
verification.

```markdown
<!-- Last-Updated: <set to current UTC ISO-8601 time at write; NOT set — write blocked> -->
# Security Matrix — 2.1.x Stream

## Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

| Product Version | Build | Build Date | backend | frontend-ui | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 0.3.12 | 2026-06-15 | `v0.3.12` | `bb447eeb` | |
| 2.1.1 | 0.3.13 | 2026-06-20 | `v0.3.13` | `deadbeef` | |

#### Container Images

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.0-rhel9` | `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `registry.example.test/trustify/api:2.1.0-rhel10` | `sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | `registry.example.test/trustify/api:2.1.1-rhel10` | `sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc` | `cpe:2.3:a:example:trustify_api:2.1.1:*:*:*:*:*:*:*` |
<!-- ^ UNRESOLVED: image revision label fedcba9876543210fedcba9876543210fedcba98 != resolved SHA 89abcdef0123456789abcdef0123456789abcdef -->

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` download URL contains the release tag
- **frontend-ui**: Git submodule at `components/frontend-ui`

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| npm | frontend-ui | `package-lock.json` | `git show <commit>:package-lock.json` | `release/0.3.z` |

## Forward Pointer

{forward-pointer}
```

Population notes:
- Supportability Matrix: there is one source column per configured repository (`backend`,
  `frontend-ui`). Values are copied verbatim from the release evidence. No retag notes are
  recorded because the evidence has none.
- Source Pinning Method: both entries come directly from the release evidence.
- Ecosystem Mappings: copied from the evidence. `<tag>` / `<commit>` in Check Command are kept
  as they were supplied. They are not invented.
- Forward Pointer: **missing**. The evidence does not say whether a later stream exists. Per
  Step 10.6.4 (ask, do not infer), please give the next stream's repo, or confirm `None`.

### 3.3 Source snapshot and write gate

- Source snapshot kept for the proposal: the Step 10.5 scaffold above, because the matrix was
  absent before scaffolding.
- Write gate status:
  - Confirmation of the full proposal: not yet requested. It is blocked by unverified evidence.
  - Evidence verified: **NO** (row 3 mismatch).
  - Final unchanged-target check: not reached.
- Outcome: **the matrix is left unchanged** (the scaffold only, if the scaffold was created).
  `Last-Updated` is not set, so triage-security's Step 0.3 staleness check will not treat this
  stream as freshly populated.

## 4. Questions for the user

1. **Corrected evidence for 2.1.1 / api-rhel10:** please provide one of the following:
   - (a) the correct published image (reference + digest) whose
     `org.opencontainers.image.revision` equals `89abcdef0123456789abcdef0123456789abcdef`, or
   - (b) the correct Konflux release tag / resolved SHA if `v0.3.13` is wrong, e.g. if the
     image was built from `fedcba9876543210fedcba9876543210fedcba98`.

   Once the corrected evidence is verified, I will present the complete proposal again for
   confirmation. I will then re-read `security-matrix.md`, compare it with the snapshot, and
   write only if it is unchanged.
2. Was a 2.1.1 `api-rhel9` image published? If yes, please provide its tag, resolved SHA,
   image reference, digest, CPE, and revision label.
3. Forward Pointer: what is the next stream's release repo, or is it `None`?

## 5. Other sections (not part of this request)

- Repository Registry: up to date (`serena_backend`, `serena_ui` are already registered).
- Jira Configuration: up to date.
- Code Intelligence: up to date. Both instances are documented with limitations.
- Bug Configuration: up to date.
- `### Jira Field Defaults` and `## Hierarchy Configuration` are not present in this CLAUDE.md.
  This request only covered the security matrix, so they were not changed. Run setup again to
  configure them.
