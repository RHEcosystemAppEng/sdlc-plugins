# Security Matrix Review — 2.1.x Stream (`security-matrix.md`)

> Simulation of `/sdlc-workflow:setup` Steps 10.5 and 10.6. No project files were changed,
> and no MCP tools, external services, or shell commands were called.

## 1. Discovery Summary (Steps 1–10)

| Section | Status |
|---|---|
| Repository Registry | Up to date. `serena_backend` and `serena_ui` were found in the tool listing, and both are already registered (`backend`, `frontend-ui`). |
| Jira Configuration | Up to date. Project key, Cloud ID, and Feature issue type ID are all set. |
| Code Intelligence | Up to date. Both Serena instances are covered, and Limitations are filled in. |
| Bug Configuration | Up to date. All three fields are set. |
| Security Configuration | Up to date. Product Lifecycle has all 4 required fields plus VEX. Version Streams has one row (2.1.x). Source Repositories has 2 rows (backend, frontend-ui). There are no `{{placeholder}}` markers. Deployment Context is not set, so the default `upstream` applies. |
| Hierarchy Configuration / Jira Field Defaults | Missing from the supplied CLAUDE.md. Not part of this request. See the changes log. |

Configured Version Stream:

| Stream | Konflux Release Repo | Local Path | Security Matrix Path |
|---|---|---|---|
| 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md |

## 2. Step 10.5 — Scaffold (the user confirmed)

`security-matrix.md` does not exist at the configured path. The scaffold below comes only from
`docs/templates/security-matrix.template.md`. The `{source-repo-name}` / `{source-ref}` cells
and their separator cells were expanded together into one column per configured Source
Repository (backend, frontend-ui). Source Pinning Method has one entry per repository. The
fixed columns and the Ecosystem Mappings section were kept.

Write semantics: re-read `security-matrix.md` immediately before writing and create it only if
it is still absent. If it has appeared since the existence check, keep the current file and
report that it now exists.

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

## 3. Step 10.6 — Population: Revision Label Checks

For each image, the published `org.opencontainers.image.revision` label was compared with the
full SHA resolved from its Konflux release tag.

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | `org.opencontainers.image.revision` | Result |
|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | MATCH: verified |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | MATCH: verified |
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | `fedcba9876543210fedcba9876543210fedcba98` | **MISMATCH: unresolved** |

### Blocking Issue: Population Not Applied

The published image `registry.example.test/trustify/api:2.1.1-rhel10`
(`sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc`) has revision label
`fedcba9876543210fedcba9876543210fedcba98`. That does not match
`89abcdef0123456789abcdef0123456789abcdef`, which is the commit resolved from release tag
`v0.3.13`.

Step 10.6.3 treats this as unresolved. **The matrix stays unchanged until verified evidence
arrives.** That means:

- the Supportability Matrix, Container Images, Source Pinning Method, or Ecosystem Mappings data is not written
- the `<!-- Last-Updated: ... -->` timestamp is not set
- the 2.1.1 / api-rhel10 row is not marked verified

**Corrected evidence needed from the user (one of these):**
1. The correct published image for 2.1.1 / api-rhel10 (reference + digest) whose revision label equals `89abcdef0123456789abcdef0123456789abcdef`, or
2. A corrected tag resolution showing that `v0.3.13` actually resolves to `fedcba9876543210fedcba9876543210fedcba98`. This would also need checking against the Supportability row (backend `v0.3.13`), or
3. Confirmation that the published image was built from the wrong commit. In that case, raise it with the release owners rather than recording the image as verified.

### Additional Questions (asking rather than inferring)

- **2.1.1 / api-rhel9**: There is release-tag and image evidence for api-rhel9 at 2.1.0 but not at 2.1.1. Was api-rhel9 not shipped in 2.1.1, or is evidence missing? No row will be added for it without evidence.
- **Forward Pointer**: Which stream comes after 2.1.x (for example a 2.2.x matrix path), or is it "None"? Nothing in the evidence answers this.
- **Retag status**: The release evidence says nothing about retags. Should the Notes cells stay blank?

## 4. Draft Populated Matrix (for review only, NOT applied)

This draft shows what would be written once the mismatch is resolved. The 2.1.1 / api-rhel10
image row is marked UNVERIFIED and must not be committed in this state. Every value is copied
exactly from the supplied evidence. The Konflux release tag, the resolved full SHA, the image
reference, the immutable digest, and the CPE are kept as separate values.

```markdown
<!-- Last-Updated: <set to current UTC time only at write, after verification> -->
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
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | UNVERIFIED: revision label mismatch (`fedcba98…`), pending corrected evidence | UNVERIFIED | UNVERIFIED |

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` download URL contains the release tag
- **frontend-ui**: Git submodule at `components/frontend-ui`

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| npm | frontend-ui | `package-lock.json` | `git show <commit>:package-lock.json` | `release/0.3.z` |

## Forward Pointer

<pending user answer>
```

## 5. Write Protocol (once evidence is verified)

1. Keep the exact contents read from `security-matrix.md` (the confirmed scaffold, or "absent") as the source snapshot for this proposal.
2. Show the complete final matrix and all revision checks, all marked MATCH, and get explicit confirmation.
3. Immediately before writing, re-read `security-matrix.md` and compare it with the snapshot.
   - If it is unchanged, write it and set line 1 to `<!-- Last-Updated: <current UTC ISO-8601> -->`. triage-security Step 0.3 uses this for its staleness check.
   - If it changed, keep the current contents and timestamp. Either build a complete merged proposal and get fresh confirmation, or abort and ask. Never write a stale proposal or an incomplete merge.
   - If it was absent and has now appeared, do not overwrite it.
4. If the user declines the review, the matrix stays unchanged.

**Current state: BLOCKED.** Waiting for corrected evidence for 2.1.1 / api-rhel10, plus answers on api-rhel9 at 2.1.1 and the Forward Pointer.
