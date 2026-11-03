# Security Matrix Review — 2.1.x Stream (`security-matrix.md`)

Simulated run of `/sdlc-workflow:setup` (Steps 1–11, focusing on Step 10.5 and Step 10.6).
No MCP tools, external services, or shell commands were invoked; discovery is simulated
from the supplied input files. No project files were modified.

---

## 1. Discovery summary (Steps 1–10)

| Step | Section | Result |
|---|---|---|
| 1 | Existing CLAUDE.md | Parsed `# Project Configuration` with Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration, Security Configuration |
| 2 | Serena instances | Discovered `serena_backend`, `serena_ui` — both already in Repository Registry. **Repository Registry is up to date** |
| 3 | Jira Configuration | Project key, Cloud ID, Feature issue type ID all present. **Jira Configuration is up to date** |
| 3.5 | Hierarchy Configuration | Section absent — out of scope for this request (security matrix only); not modified. Can be configured in a later `/setup` run |
| 4 | Jira Field Defaults | Subsection absent — out of scope for this request; not modified |
| 5 | Code Intelligence | Covers `serena_backend` and `serena_ui`, has `### Limitations`. **Code Intelligence is up to date** |
| 9 | Bug Configuration | All three fields populated. **Bug Configuration is up to date** |
| 10 | Security Configuration | Product Lifecycle (4 required + VEX), Version Streams (1 row), Source Repositories (2 rows) populated, no `{{placeholder}}` markers. **Security Configuration is up to date** (note: Source Repositories has no Deployment Context column; that field is optional and defaults to `upstream`, so no change is proposed) |
| 10.5 | `security-matrix.md` for stream 2.1.x | **Missing** at the configured path `security-matrix.md` → scaffold offered; user confirmed |
| 10.6 | Populate supportability / image identity | User accepted; evidence from `security-matrix-image-identity.md` evaluated below — **blocked by a revision-label mismatch** |

Configured inputs used:

- Stream: `2.1.x`
- Konflux release repo: `git.downstream.example.com/my-org/product-release.2.1.z`
- Security Matrix Path: `security-matrix.md`
- Source Repositories: `backend`, `frontend-ui` (in configured order)

---

## 2. Step 10.5 — Scaffold (confirmed by user)

Source: plugin-root `docs/templates/security-matrix.template.md` (the canonical template;
`docs/templates/security-matrix.md` is only a worked example and was not used as the
scaffold source). The `{source-repo-name}` / `{source-ref}` column and its separator and
value cells were expanded in lockstep into one column per configured Source Repository
(`backend`, `frontend-ui`), and the Source Pinning Method entry was repeated once per
repository. Fixed columns, Container Images table, and Ecosystem Mappings were retained.

Write semantics: re-read `security-matrix.md` immediately before writing and create it
**create-if-absent**. If the file has appeared since the initial existence check, preserve
it, report that it now exists, and do not write the scaffold over it (any merge requires a
complete merged proposal and fresh confirmation). If create-if-absent cannot be
guaranteed, abort rather than overwrite.

### Proposed scaffold content

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

<!-- One row per product version built from this release stream. One column per
     repository in Security Configuration > Source Repositories. Each source column
     contains that repository's tag or commit pinned in Konflux. -->

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

<!-- One entry per configured Source Repositories row. -->

- **backend**: {source-pinning-method}
- **frontend-ui**: {source-pinning-method}

## Ecosystem Mappings

<!-- One row per tracked ecosystem (Repository / Lock File / Check Command /
     Upstream Branch). triage-security uses these mappings for released-version
     and fix checks. -->

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| {ecosystem} | {repository} | `{lock-file}` | `{check-command}` | `{upstream-branch}` |

## Forward Pointer

<!-- Points to the next version stream's matrix, or "None" for the latest
     development stream. -->

{forward-pointer}
```

---

## 3. Step 10.6 — Revision checks (published image vs. resolved release commit)

Each published image's `org.opencontainers.image.revision` label is compared with the full
SHA resolved from its Konflux release tag. Rows are keyed by unique Product Version /
Component pair.

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | `org.opencontainers.image.revision` | Result |
|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | MATCH — verified |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | MATCH — verified |
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | `fedcba9876543210fedcba9876543210fedcba98` | **MISMATCH — unresolved** |

### Unresolved: 2.1.1 / api-rhel10

The published image `registry.example.test/trustify/api:2.1.1-rhel10`
(`sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc`) carries revision
label `fedcba9876543210fedcba9876543210fedcba98`, but tag `v0.3.13` resolves to
`89abcdef0123456789abcdef0123456789abcdef`. The image therefore cannot be shown to have been
built from the 2.1.1 release commit.

Per Step 10.6 item 3, this is unresolved: **the matrix is left unchanged until the evidence
is verified.** No populated content is written, the mismatched row is not recorded or
marked verified, and the `Last-Updated` timestamp is not set.

**Corrected evidence requested from the user** (any one resolves the blocker):

1. The correct resolved commit for tag `v0.3.13` (if the tag resolution is wrong), or
2. The correct published image reference / digest for 2.1.1 api-rhel10 whose revision label
   equals `89abcdef0123456789abcdef0123456789abcdef` (if the wrong image was cited), or
3. Confirmation that `v0.3.13` was moved/re-tagged, together with the authoritative release
   commit, so the row can be re-checked.

### Other gaps requiring user input (asked, not inferred)

- **Forward Pointer** — no next-stream information was supplied. Ask: is there a newer
  stream (name + Konflux release repo), or should this be `None`?
- **CPE values** — both 2.1.0 images (api-rhel9 and api-rhel10) share the identical CPE
  `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*`. Recorded exactly as supplied;
  please confirm this is intended (no per-platform CPE).
- **2.1.1 api-rhel9** — no tag-resolution or image evidence was supplied for an api-rhel9
  image in 2.1.1. No row is invented; confirm whether that image was not published or
  provide its evidence.

---

## 4. Proposed populated matrix (DRAFT — for review only; NOT writable yet)

This is the complete proposal built from the supplied evidence, shown so the user can review
everything else while the blocker is resolved. It is **not** approved for writing: the
2.1.1 / api-rhel10 image row is withheld pending corrected evidence, and the Forward Pointer
is pending a user answer. Once these are resolved, the full proposal will be re-presented
with the completed rows for confirmation.

Source snapshot retained for the final unchanged-target check: the target
`security-matrix.md` was **absent** at read time (snapshot = "file does not exist"); if a
scaffold is written first, the snapshot becomes the exact scaffold content in section 2.

```markdown
<!-- Last-Updated: <set to current UTC ISO-8601 time only at write, after confirmation> -->
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

<!-- 2.1.1 / api-rhel10 withheld: published revision label
     fedcba9876543210fedcba9876543210fedcba98 does not match the commit
     89abcdef0123456789abcdef0123456789abcdef resolved from v0.3.13.
     Awaiting corrected evidence. -->

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` download URL contains the release tag
- **frontend-ui**: Git submodule at `components/frontend-ui`

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| npm | frontend-ui | `package-lock.json` | `git show <commit>:package-lock.json` | `release/0.3.z` |

## Forward Pointer

<pending user answer — next stream or "None">
```

Notes on the draft:

- One supportability source column per configured repository (`backend`, `frontend-ui`) is
  preserved; refs copied exactly from release evidence.
- Release tag, resolved full SHA, image reference, immutable digest, and CPE are kept as
  distinct values; digests are not treated as tags or commits.
- Source Pinning Method and Ecosystem Mappings are taken verbatim from the supplied evidence;
  nothing was inferred.

---

## 5. Write procedure once evidence is verified

1. User supplies corrected 2.1.1 / api-rhel10 evidence and the Forward Pointer answer.
2. Re-run the revision check; all rows must MATCH.
3. Present the complete proposed matrix and revision checks again for confirmation.
4. After confirmation, re-read `security-matrix.md` immediately before writing and compare
   with the retained snapshot:
   - unchanged → write; set first line `<!-- Last-Updated: <current UTC ISO-8601> -->`
     (consumed by triage-security Step 0.3 staleness check);
   - target was absent → create with create-if-absent semantics; if it appeared, do not
     overwrite;
   - changed → preserve current contents and timestamp, build a complete merged proposal
     and get fresh confirmation, or abort and ask. Never write a stale proposal or use
     placeholders to complete a merge.
5. A declined review leaves the matrix unchanged.

## 6. Current status

**Matrix population: BLOCKED — awaiting corrected evidence for 2.1.1 / api-rhel10.**
No populated matrix has been written and no `Last-Updated` timestamp has been set.
CLAUDE.md requires no changes for this request.
