# Security Matrix Review — 2.1.x Stream (`security-matrix.md`)

> Eval simulation of `/sdlc-workflow:setup`, Steps 10.5–10.6. No project files were changed.
> Inputs: `claude-md-configured-with-security.md`, `mcp-tools-with-serena.md`,
> `security-matrix-image-identity.md`.

## Status Summary

| Item | Result |
|---|---|
| Project Configuration (Registry, Jira, Code Intelligence, Bug, Security) | Up to date. No CLAUDE.md changes |
| `security-matrix.md` (2.1.x stream) | Missing. Scaffold proposed from `docs/templates/security-matrix.template.md`; user confirmed |
| Scaffold write semantics | Create-if-absent. Re-read the path right before writing. If the file has appeared since the check, keep it and do not overwrite |
| Population from release/image evidence | **BLOCKED.** One image revision mismatch (2.1.1 / api-rhel10). The matrix is not populated until corrected evidence is verified |
| `<!-- Last-Updated: ... -->` timestamp | **Not set.** It is only set after a verified, confirmed write |

---

## Step 10.5 — Scaffold (confirmed by user, create-if-absent)

This scaffold comes from the plugin-root canonical template. The `{source-repo-name}` / `{source-ref}`
header, separator and value cells were expanded together into one column per configured
Source Repository (`backend`, `frontend-ui`). The Source Pinning Method section has one entry per repository.
The fixed columns and Ecosystem Mappings are kept.

```markdown
# Security Matrix — 2.1.x Stream

<!-- Canonical template for security matrix files. ... (template comment retained) -->

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

---

## Step 10.6 — Revision Checks (published image label vs resolved release commit)

Each row is keyed by a unique **Product Version / Component** pair. The Konflux release tag, the resolved full SHA,
the image reference, the immutable OCI digest and the CPE are kept as separate values.

| Product Version | Component | Konflux Release Tag | Resolved Release Commit SHA | `org.opencontainers.image.revision` | Result |
|---|---|---|---|---|---|
| 2.1.0 | api-rhel9 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | MATCH: verified |
| 2.1.0 | api-rhel10 | `v0.3.12` | `0123456789abcdef0123456789abcdef01234567` | `0123456789abcdef0123456789abcdef01234567` | MATCH: verified |
| 2.1.1 | api-rhel10 | `v0.3.13` | `89abcdef0123456789abcdef0123456789abcdef` | `fedcba9876543210fedcba9876543210fedcba98` | **MISMATCH: unresolved** |

### Unresolved: 2.1.1 / api-rhel10

The published image `registry.example.test/trustify/api:2.1.1-rhel10`
(`sha256:cccc…cccc`) has revision label `fedcba9876543210fedcba9876543210fedcba98`.
Tag `v0.3.13` resolves to `89abcdef0123456789abcdef0123456789abcdef`. The two do not match.
The image may have been built from a different commit, the tag may have moved, or the
digest/reference may belong to a different build.

Per Step 10.6.3 this row is **not verified**, and the matrix stays **unchanged** until
corrected evidence is supplied and verified. I did not guess which value is correct.

**Questions for the user:**
1. Please send corrected evidence for 2.1.1 / api-rhel10. Either:
   - the correct resolved commit SHA for tag `v0.3.13`, if the tag resolution was wrong, or
   - the correct published image reference, digest and revision label, if the wrong image was captured.
2. Is there an api-rhel9 image for 2.1.1? The release and image evidence only lists api-rhel10 for 2.1.1.
   If it exists, please send its tag, resolved SHA, image reference, digest, CPE and revision label.
   If it does not, please confirm that 2.1.1 shipped rhel10 only.
3. What is the Forward Pointer? The next stream's name and Konflux release repo, or "None" if 2.1.x is the latest stream.
   This is not in the evidence, so I will not infer it.
4. The Ecosystem Mappings Check Commands in the evidence are generic (`git show <tag>:Cargo.lock`,
   `git show <commit>:package-lock.json`). Should they stay generic, or be pinned to the latest
   release refs (`v0.3.13`, `deadbeef`)? I will not infer this.

---

## Proposed Populated Matrix (DRAFT — NOT WRITTEN)

This is shown for review only. It will be written only after:
(a) the 2.1.1 / api-rhel10 mismatch is resolved with verified evidence,
(b) the open questions above are answered,
(c) the user confirms the complete proposal, and
(d) a final re-read shows the target still matches the source snapshot.

At that point the first line becomes `<!-- Last-Updated: <current UTC ISO-8601> -->`.

Source snapshot: target `security-matrix.md` was **absent** at the time of reading. If it is still absent,
it will be created with create-if-absent semantics. If the confirmed scaffold has been written by then,
the scaffold contents above are the snapshot. If the file has changed or appeared from another source,
the current contents are kept and a merged proposal is shown for fresh confirmation.

```markdown
<!-- Last-Updated: (set at write time, only after verification and confirmation) -->
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
| 2.1.1 | api-rhel10 | **UNRESOLVED: revision mismatch, awaiting corrected evidence** | | | | |

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` download URL contains the release tag
- **frontend-ui**: Git submodule at `components/frontend-ui`

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| npm | frontend-ui | `package-lock.json` | `git show <commit>:package-lock.json` | `release/0.3.z` |

## Forward Pointer

(Awaiting user input. See question 3.)
```

## Notes

- Retag status: the evidence notes contain no retags, so the Notes column is empty.
- `frontend-ui` refs (`bb447eeb`, `deadbeef`) are short commit IDs, recorded as given in the release evidence.
- The CPEs for the 2.1.0 rhel9 and rhel10 images are the same in the evidence (`trustify_api:2.1.0`).
  They are recorded as given and not changed.
- Advisory (not changed, for idempotency): the CLAUDE.md `### Source Repositories` table has no
  optional `Deployment Context` column. Consumers default it to `upstream`. Add it manually if another context applies.
