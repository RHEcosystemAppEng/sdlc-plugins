# Security Matrix Review — 2.1.x Stream (`security-matrix.md`)

> Eval simulation: nothing was written to project files. This document is the
> review the setup skill shows the user under Step 10.5 (Scaffold) and Step 10.6
> (Populate supportability and image identity).

## 1. Configuration Discovery (Steps 1–10, simulated)

| Section | Result |
|---|---|
| Repository Registry | Up to date. `serena_backend` and `serena_ui` were found in the MCP tool list and are already registered (backend, frontend-ui) |
| Jira Configuration | Up to date. Project key, Cloud ID and Feature issue type ID are all set |
| Code Intelligence | Up to date. Both Serena instances are documented, and `### Limitations` is present |
| Bug Configuration | Up to date. All three fields are set |
| Security Configuration | Up to date. All required Product Lifecycle fields, 1 Version Stream (2.1.x) and 2 Source Repositories (backend, frontend-ui) are set. Existing values are kept as they are |
| `security-matrix.md` (2.1.x) | **Missing**. The user confirmed scaffolding |

No changes to CLAUDE.md are proposed.

## 2. Scaffold Proposal (Step 10.5)

- The scaffold comes only from the canonical `docs/templates/security-matrix.template.md`.
  It is not copied from the worked example.
- `{source-repo-name}` / `{source-ref}` and their separator cells are expanded together
  into one column per configured Source Repository: **backend**, **frontend-ui**.
- There is one Source Pinning Method entry per repository. The fixed columns and the
  Ecosystem Mappings section are kept.
- Write semantics: **create-if-absent**. The path is re-read just before writing. If
  `security-matrix.md` has appeared in the meantime, it is kept and not overwritten.

## 3. Revision Label Verification (Step 10.6.3)

Each published image's `org.opencontainers.image.revision` is compared with the full SHA
resolved from that row's Konflux release tag.

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | `org.opencontainers.image.revision` | Result |
|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | MATCH: verified |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | MATCH: verified |
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | `fedcba9876543210fedcba9876543210fedcba98` | **MISMATCH: unresolved** |

### Blocking issue

For **2.1.1 / api-rhel10**, the published image
`registry.example.test/trustify/api:2.1.1-rhel10`
(`sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc`) has the revision
label `fedcba9876543210fedcba9876543210fedcba98`. Tag `v0.3.13` resolves to
`89abcdef0123456789abcdef0123456789abcdef`. The image therefore cannot be shown to come
from the release commit.

Per Step 10.6.3, a mismatch is unresolved. **The populated matrix will not be written**, and
the matrix stays unchanged until corrected evidence is verified. The skill does not pick
either SHA, and it does not leave out or soften the row to get past the check.

**Request to user:** please supply one of the following:
1. Corrected release-tag resolution for `v0.3.13`. Was the tag moved or retagged? Retag status is part of the release evidence.
2. A corrected image reference or digest for 2.1.1 api-rhel10 whose revision label equals the resolved SHA.
3. Confirmation of which build actually shipped as 2.1.1, with supporting evidence.

### Other evidence gaps (ask, do not infer)

- **2.1.1 / api-rhel9**: the evidence has no release tag, resolved SHA or published image.
  Does 2.1.1 ship an api-rhel9 image? If it does, please supply the evidence. If it does
  not, please confirm, and no row will be added.
- **Retag status**: the release evidence does not record retag status for `v0.3.12` or
  `v0.3.13`.
- **frontend-ui container images**: there is no image evidence for frontend-ui. The
  Supportability Matrix shows it only as a source ref (submodule commit). Please confirm
  that frontend-ui is built into the api image and not published as a separate component.
- **Forward Pointer**: the next stream's matrix, or "None" if 2.1.x is the latest stream,
  was not provided.

## 4. Complete Proposed Matrix (for review only, NOT writable yet)

Writing is blocked by the 2.1.1 / api-rhel10 revision mismatch. The first-line
`Last-Updated` timestamp is set only when an actual write happens. Source snapshot of the
target: **absent** (the file does not exist). If the file exists at write time, the
proposal is rebuilt as a merge against its current contents and confirmed again.

```markdown
<!-- Last-Updated: (set to current UTC ISO-8601 at write time, only after verification) -->
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

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` download URL contains the release tag
- **frontend-ui**: Git submodule at `components/frontend-ui`

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| npm | frontend-ui | `package-lock.json` | `git show <commit>:package-lock.json` | `release/0.3.z` |

## Forward Pointer

(pending user input: next stream's matrix path, or "None")
```

Notes on the proposal:
- The 2.1.1 / api-rhel10 row is shown as the evidence states it, so that it can be
  reviewed. It is **unverified** and blocks the write.
- Konflux release tag, resolved SHA, image reference, digest and CPE are kept as
  separate values. Image references are not used in place of digests, and tags are not
  used in place of SHAs.
- The Container Images table has one row for each unique Product Version / Component
  pair: 3 pairs in the evidence, with no duplicates.

## 5. Write Gate Status

| Gate | Status |
|---|---|
| User confirmed scaffold | Yes |
| User confirmed population | Requested. Complete proposal shown above |
| All revision labels verified | **No**: 2.1.1 / api-rhel10 mismatch |
| Missing evidence resolved | **No**: see Section 3 gaps |
| Final unchanged-target re-read | Not reached |
| **Decision** | **Do not write the populated matrix.** Matrix stays unchanged until corrected evidence is supplied and verified |

The only write this session could make is the confirmed bare scaffold, with
create-if-absent semantics and placeholders expanded only in structure. In this eval
simulation, no project files are written at all.
