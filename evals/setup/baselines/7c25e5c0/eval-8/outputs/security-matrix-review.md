# Security Matrix Scaffold Review

**Canonical scaffold source:** `docs/templates/security-matrix.template.md`

> `docs/templates/security-matrix.md` is a worked example and was NOT used as a template or fallback.

**Configured Jira version prefix:** MYPRODUCT

**Configured stream:** 2.1.x

**Configured source repositories:** backend, frontend-ui

The user confirmed scaffolding the missing matrix. The user declined optional supportability and image population — no data has been fabricated.

The `Product Version` heading below is carried unchanged from the canonical template `docs/templates/security-matrix.template.md`. It was not relabeled or rewritten at runtime.

---

## Proposed Scaffold: `security-matrix.md`

Below is the complete proposed scaffold. No actual project matrix file is written until the user confirms.

---

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

---

**Status:** Scaffold prepared for review. No project matrix file has been written. The user declined optional supportability and image population — placeholder tokens remain for future population by `/triage-security` or manual entry.
