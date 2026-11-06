# Security Matrix Review — 2.1.x Stream (`security-matrix.md`)

Eval simulation of `/sdlc-workflow:setup`, Steps 10.5 and 10.6. I did not call any
MCP tools, external services, or shell commands, and I did not modify any project files.

## Context

- Security Configuration exists in CLAUDE.md, and all required fields are populated
  with no `{{placeholder}}` markers. Result: **Security Configuration is up to date.**
- Version Stream: `2.1.x`
  - Konflux Release Repo: `git.downstream.example.com/my-org/product-release.2.1.z`
  - Local Path: `/home/user/product-release.2.1.z`
  - Security Matrix Path: `security-matrix.md`
- Source Repositories: `backend`, `frontend-ui`.
- Simulated existence check: `security-matrix.md` is **missing**.

---

## Part 1 — Step 10.5: Scaffold (user confirmed)

Source: the plugin-root `docs/templates/security-matrix.template.md`, which is the canonical
scaffold. I did not use the `docs/templates/security-matrix.md` worked example as a source.
`{source-repo-name}` / `{source-ref}` and their separator cells were expanded together
into one column per configured Source Repository (`backend`, `frontend-ui`). The
Source Pinning Method section got one entry per repository. The fixed columns, the
Container Images table, and Ecosystem Mappings are kept.

Write semantics: re-read `security-matrix.md` right before writing and create it
**only if it is still absent** (create-if-absent). If the file has appeared since the
first check, keep it, report that it now exists, and do not write the scaffold over it.
If the Write tool cannot guarantee create-if-absent, abort instead of overwriting.

### Proposed scaffold content (written only on confirmed create-if-absent)

```markdown
# Security Matrix — 2.1.x Stream

<!-- Canonical template for security matrix files. ... -->

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

I kept the scaffold's existing HTML guidance comments from the template; the block above
abbreviates them.

---

## Part 2 — Step 10.6: Populate supportability and image identity

The user agreed to populate from the evidence in `security-matrix-image-identity.md`.

### Revision label checks (`org.opencontainers.image.revision` vs resolved release commit SHA)

There is one Container Images row per unique Product Version / Component pair. For
each row, the Konflux release tag, resolved full SHA, image reference, immutable
digest, and CPE are kept as separate values.

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | Published `org.opencontainers.image.revision` | Result |
|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | MATCH — verified |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | MATCH — verified |
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | `fedcba9876543210fedcba9876543210fedcba98` | **MISMATCH — UNRESOLVED** |

### Blocking finding

For **2.1.1 / api-rhel10**, the published image
`registry.example.test/trustify/api:2.1.1-rhel10`
(`sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc`) has a
revision label of `fedcba9876543210fedcba9876543210fedcba98`. That label does **not** equal
`89abcdef0123456789abcdef0123456789abcdef`, the full SHA resolved from Konflux release tag
`v0.3.13`.

Under Step 10.6.3, a mismatch is unresolved. **I will leave the matrix unchanged until
this is verified.** I will not write the populated matrix, set the `Last-Updated`
timestamp, or mark any image row verified. The file stays as the confirmed scaffold
from Part 1, or is not created at all if create-if-absent fails.

**Question for the user:** please provide corrected evidence for 2.1.1 / api-rhel10.
Any one of these resolves it:
1. Confirmation of the correct commit that Konflux tag `v0.3.13` points to. The label
   may indicate the tag was moved or resolved incorrectly.
2. The correct published image reference or digest for 2.1.1 rhel10, if the listed image
   was built from a different commit.
3. An explanation of the discrepancy, such as a rebuild or retag, with evidence that the
   label and tag resolve to the same commit.

### Other gaps that need user input (ask rather than infer)

- **2.1.1 / api-rhel9**: the evidence has no release-tag resolution and no published
  image for this pair. I will not add a row by inferring from 2.1.0. Please confirm
  whether 2.1.1 shipped an rhel9 image, and if so provide its tag, SHA, image, digest,
  CPE, and revision label.
- **Component naming**: the image components (`api-rhel9`, `api-rhel10`) do not use the
  configured Source Repository names (`backend`, `frontend-ui`). Please confirm whether
  `api-*` images are built from `backend`, and whether `frontend-ui` ships as its own image
  (no image evidence was supplied for it).
- **Forward Pointer**: the evidence does not name a next stream. Please supply the next
  stream and its release repo, or confirm `None`.
- **Retag status**: the evidence has no retag notes, so the Notes cells stay empty. Please
  confirm that no 2.1.x release was a retag.

### Complete proposed matrix (FOR REVIEW ONLY — NOT WRITTEN)

The proposal below contains only the values that the supplied evidence supports. The
mismatched 2.1.1 / api-rhel10 row is shown, flagged UNRESOLVED, for review. It must not
be written until corrected evidence verifies it. The `Last-Updated` line is set only at
write time, after confirmation, verified evidence, and a final unchanged-target check.

```markdown
<!-- Last-Updated: <set to current UTC ISO-8601 time at write; NOT SET — write blocked> -->
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
<!-- ^ UNRESOLVED: published revision label fedcba9876543210fedcba9876543210fedcba98 != resolved SHA 89abcdef0123456789abcdef0123456789abcdef. Not verified; blocks write. -->

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` (download URL contains the release tag, e.g., `v0.3.13`)
- **frontend-ui**: git submodule at `components/frontend-ui`

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| npm | frontend-ui | `package-lock.json` | `git show <commit>:package-lock.json` | `release/0.3.z` |

## Forward Pointer

<!-- PENDING USER INPUT: next stream not provided in evidence. -->
```

### Write procedure once evidence is verified (not executed in this run)

1. Retain the exact contents of `security-matrix.md` as read at proposal time (the
   scaffold, or absent) as the **source snapshot**.
2. Present the complete corrected proposal and its revision checks, and get the user's
   confirmation.
3. Re-read `security-matrix.md` immediately before writing and compare it with the snapshot.
   - Unchanged: write the populated matrix and set the first line to
     `<!-- Last-Updated: <current UTC ISO-8601> -->`. triage-security Step 0.3 uses this
     line for its staleness check.
   - Changed: keep the current contents and timestamp. Build a merged proposal and present
     it in full for fresh confirmation, or abort and ask the user. Never write a stale
     proposal over a concurrent update. Never use placeholders to finish an incomplete merge.
   - Absent: create it with create-if-absent semantics. If it has appeared in the meantime,
     do not overwrite it.
4. If the user declines the review, leave the matrix unchanged.

## Status

- Scaffold (Step 10.5): confirmed. It is written with create-if-absent semantics only.
- Population (Step 10.6): **BLOCKED** by the 2.1.1 / api-rhel10 revision label mismatch.
  The matrix stays unchanged and no `Last-Updated` timestamp is set. I am waiting for
  corrected evidence and the answers to the open questions above.
