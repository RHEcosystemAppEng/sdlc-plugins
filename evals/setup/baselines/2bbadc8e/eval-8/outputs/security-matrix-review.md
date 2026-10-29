# Security Matrix Scaffold Review — 2.1.x Stream

## Scaffold Source

Canonical template: `docs/templates/security-matrix.template.md`

> `docs/templates/security-matrix.md` is a worked example and was **not** used as a source or fallback.

## Configuration Context

- **Jira version prefix:** MYPRODUCT
- **Version Stream:** 2.1.x
- **Konflux Release Repo:** git.downstream.example.com/my-org/product-release.2.1.z
- **Security Matrix Path:** security-matrix.md
- **Source Repositories:** backend, frontend-ui

## User Decisions

- Scaffolding confirmed: **yes**
- Optional supportability/image population: **declined** — no supportability or image data was fabricated

## Proposed Scaffold

The following content would be written to `security-matrix.md`. The `Product Version` heading is carried unchanged from the canonical template — no relabeling was performed at runtime.

---

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

---

## Scaffold Notes

- The `{source-repo-name}` placeholder in the Supportability Matrix header and separator was expanded in lockstep into two columns: **backend** and **frontend-ui**.
- The Supportability Matrix header row has 6 cells, the separator row has 6 cells, and the data row has 6 cells — all matching.
- The `Product Version` column header is the canonical template's neutral label, carried through unchanged. It does **not** contain `RHTPA Version`.
- The Container Images table retains all 7 columns: Product Version, Component, Konflux Release Tag, Resolved Release Commit SHA, Image Reference, Image Digest, CPE.
- The Source Pinning Method section has one entry per configured source repository (backend, frontend-ui).
- Remaining `{placeholder}` markers in value cells are intentional — the user declined population, so no data was fabricated.
- **No actual project matrix file was written.** This is a review-only proposal; the matrix will be written only after the user confirms this scaffold.
