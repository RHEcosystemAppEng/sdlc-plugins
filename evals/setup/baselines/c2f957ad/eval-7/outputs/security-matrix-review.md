# Security Matrix Review — 2.1.x Stream (Simulated /sdlc-workflow:setup run)

> Eval simulation. No MCP tools, external services, or project files were touched.
> Target path (from CLAUDE.md > Security Configuration > Version Streams): `security-matrix.md`

## 1. Configuration status (Steps 1–10)

| Section | Status |
|---|---|
| Repository Registry | Up to date. Discovered Serena instances `serena_backend` and `serena_ui` are both registered already |
| Jira Configuration | Up to date. Project key, Cloud ID, and Feature issue type ID are all set |
| Hierarchy Configuration | Section is missing. Hierarchy discovery is out of scope for this matrix task and was not run |
| Jira Field Defaults | Subsection is missing. Not run, because this matrix task does not cover it |
| Code Intelligence | Up to date. It covers both Serena instances and has a Limitations subsection |
| Bug Configuration | Up to date. All three fields are populated |
| Security Configuration | Up to date. The 4 required Product Lifecycle fields, 1 Version Stream, and 2 Source Repositories are set. Deployment Context is optional and defaults to `upstream` |

No changes are proposed to CLAUDE.md.

## 2. Step 10.5: Scaffold the missing matrix

- Existence check: `security-matrix.md` for stream 2.1.x is **missing**.
- The scaffold source is `docs/templates/security-matrix.template.md`, the canonical template. The worked example `docs/templates/security-matrix.md` was **not** used as a source.
- `{source-repo-name}` / `{source-ref}` and their separator cells were expanded in lockstep into one column per configured Source Repository (`backend`, `frontend-ui`). There is one Source Pinning Method entry per repository. Fixed columns and Ecosystem Mappings were kept.
- The user confirmed the scaffold.
- Write semantics: **create-if-absent**. Re-read the path immediately before writing. If the file has appeared since the first check, keep it, report that it now exists, and do not overwrite it. (In this simulation nothing is written to the project.)

### Proposed scaffold (pre-population)

```markdown
# Security Matrix — 2.1.x Stream

## Version Stream

This Konflux release repo covers the **2.1.x** product version stream.

## Supportability Matrix

| Product Version | Build | Build Date | backend | frontend-ui | Notes |
|---|---|---|---|---|---|
| {version} | {build} | {build-date} | `{source-ref}` | `{source-ref}` | |

#### Container Images

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image Reference | Image Digest | CPE |
|---|---|---|---|---|---|---|
| {version} | {component} | `{release-tag}` | `{release-commit-sha}` | `{image-reference}` | `sha256:{image-digest}` | `{cpe}` |

### Source Pinning Method

- **backend**: {source-pinning-method}
- **frontend-ui**: {source-pinning-method}

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| {ecosystem} | {repository} | `{lock-file}` | `{check-command}` | `{upstream-branch}` |

## Forward Pointer

{forward-pointer}
```

(Template HTML guidance comments are kept in the real scaffold. They are left out here for brevity.)

## 3. Step 10.6: Populate from release and published-image evidence

### 3.1 Revision checks: `org.opencontainers.image.revision` vs the resolved release commit SHA

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Image revision label | Result |
|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | MATCH (verified) |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | MATCH (verified) |
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | `fedcba9876543210fedcba9876543210fedcba98` | **MISMATCH (unresolved)** |

**Blocking finding:** the published image `registry.example.test/trustify/api:2.1.1-rhel10` (`sha256:cccc…cccc`) has a revision label of `fedcba98…`. Tag `v0.3.13` resolves to `89abcdef…`. Because they differ, this row cannot be verified. Possible causes are a wrong digest, a retagged or rebuilt image, or a wrong tag resolution. Following Step 10.6.3, the **matrix stays unchanged until corrected evidence is supplied and verified**. No population write happens, and the `Last-Updated` timestamp is **not** set.

### 3.2 Request for corrected evidence

To finish the population, please provide one of the following:
1. The correct published image reference and digest for 2.1.1 / api-rhel10, with a revision label that equals `89abcdef0123456789abcdef0123456789abcdef`, or
2. A corrected Konflux release tag or SHA resolution for 2.1.1 / api-rhel10 that matches `fedcba9876543210fedcba9876543210fedcba98`, with an explanation (for example, a rebuild or retag that should be recorded in Notes).

Other open items. Per the "ask rather than infer" rule these were not filled in:
- **Forward Pointer**: the evidence names no next stream. Is it `None` (2.1.x is the latest stream), or the next stream's release repo?
- **Retag status**: the evidence has no retag notes, so the Notes cells are left blank. Please confirm that no 2.1.x release was a retag.
- **2.1.1 api-rhel9**: there is no tag or image evidence for it, so no row is proposed. Please confirm whether 2.1.1 shipped an rhel9 image.

### 3.3 Proposed populated matrix (for review only, NOT approved for writing)

This is the full proposal as it would look once the evidence is verified. The 2.1.1 / api-rhel10 row is marked UNRESOLVED. It must not be written as verified.

```markdown
<!-- Last-Updated: <set to current UTC time only at the actual write, after all checks pass> -->
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
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | UNRESOLVED: image revision label `fedcba98…` does not match | UNRESOLVED | UNRESOLVED |

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` download URL contains the release tag
- **frontend-ui**: Git submodule at `components/frontend-ui`

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| npm | frontend-ui | `package-lock.json` | `git show <commit>:package-lock.json` | `release/0.3.z` |

## Forward Pointer

<pending user answer — see 3.2>
```

Notes on distinct values: the Konflux release tag (`v0.3.x`), the full resolved commit SHA (40 hex characters), the image reference (registry:tag), the immutable digest (`sha256:…`), and the CPE are kept in separate columns and never stand in for one another. Both 2.1.0 images share one CPE string, which the evidence shows as is. Both are kept as separate rows because the Product Version / Component pairs differ.

### 3.4 Write protocol once verified

1. Keep a snapshot of the matrix exactly as it was read: the confirmed scaffold, or "absent" if the scaffold was not written.
2. Get corrected, verified evidence for 2.1.1 / api-rhel10 and answers to the open items. Then present the complete updated proposal for fresh confirmation.
3. Re-read `security-matrix.md` immediately before writing and compare it with the snapshot. If it changed, keep the current contents and timestamp, then present a merged proposal for new confirmation or abort. If the target is absent, use create-if-absent.
4. Only then write, setting line 1 to `<!-- Last-Updated: <current UTC ISO-8601> -->`. triage-security Step 0.3 uses this line for its staleness check.

## 4. Step 11: Validation summary

- CLAUDE.md is unchanged. The Security Configuration has Product Lifecycle (4 required fields plus VEX), 1 Version Stream row, and 2 Source Repository rows. It passes.
- `security-matrix.md`: the scaffold is confirmed (create-if-absent, simulated). **Population is BLOCKED** pending corrected 2.1.1 / api-rhel10 image evidence. The matrix stays at the scaffold state, and no `Last-Updated` timestamp is set.
