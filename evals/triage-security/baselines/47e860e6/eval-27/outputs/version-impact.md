# Step 2 – Version Impact Analysis: TC-8051

**Issue stream scope:** 2.2.x (from the `[rhtpa-2.2]` suffix). Every supported version in the matrix was checked, as the skill requires. Versions outside the scope are listed for cross-stream context only.

## 2.1 – Supportability Matrix (aggregated)

| Stream | Version | backend tag | Notes |
|--------|---------|-------------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | |
| 2.1.x | 2.1.1 | v0.3.12 | |
| 2.2.x | 2.2.0 | v0.4.5 | |
| 2.2.x | 2.2.1 | v0.4.8 | |
| 2.2.x | 2.2.2 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.x | 2.2.3 | v0.4.11 | |
| 2.2.x | 2.2.4 | v0.4.12 | |

The matrix format is valid: Supportability Matrix, Ecosystem Mappings, Source Pinning Method and Forward Pointer are all present. The matrix is stale (last updated 2026-06-28, 129 days ago). See data-extraction.md.

## 2.2 – Development Stream

Not determined. No Jira version metadata (unreleased `RHTPA` versions) was available in this eval, and no branch-HEAD lock data was supplied. In a live run this would come from `getJiraIssueTypeMetaWithFields` and `git show HEAD:Cargo.lock`.

## 2.3 / 2.4 – Version Impact Table

Version Impact for CVE-2026-99002 (rustls < 0.23.5):

| Version | rustls (Cargo.lock) | In affected range? | Shipped in default build? | Affected? | Notes |
|---------|---------------------|--------------------|---------------------------|-----------|-------|
| 2.1.0 | not present | NO | — | NO | out of scope (2.1.x); rustls not in lock file |
| 2.1.1 | not present | NO | — | NO | out of scope (2.1.x); rustls not in lock file |
| **2.2.0** | 0.23.4 | YES | NO (feature-gated) | **YES (feature-gated; see below)** | in scope; behind non-default `tls-rustls` feature |
| **2.2.1** | 0.23.4 | YES | NO (feature-gated) | **YES (feature-gated; see below)** | in scope; behind non-default `tls-rustls` feature |
| **2.2.2** | — | YES | NO (feature-gated) | **YES (feature-gated; see below)** | in scope; same as 2.2.1 (backend retag, v0.4.8) |
| **2.2.3** | 0.23.4 | YES | NO (feature-gated) | **YES (feature-gated; see below)** | in scope; behind non-default `tls-rustls` feature |
| **2.2.4** | 0.23.4 | YES | NO (feature-gated) | **YES (feature-gated; see below)** | in scope; behind non-default `tls-rustls` feature |
| dev | unknown | — | — | unknown | no dev-stream data available |

Lock-file result: rustls 0.23.4 is in `Cargo.lock` for every 2.2.x version. 0.23.4 is below the fixed version 0.23.5, so every 2.2.x version is **in the affected range**. rustls is absent from all 2.1.x versions, so 2.1.x is **not affected** and there is no cross-stream impact (Case A does not apply).

## 2.3.5 – Dependency Chain Context

```
Dependency chain for rustls:
  backend (workspace) → rustls
  Type: direct optional dependency
  Profile: feature-gated (optional = true, behind non-default feature "tls-rustls")
  Default features do NOT include "tls-rustls". The product ships with
  "tls-native" (native-tls) enabled by default.

Feature declaration (backend/Cargo.toml, v0.4.5+):
  [dependencies]
  rustls = { version = "0.23.4", optional = true }

  [features]
  default    = ["tls-native"]
  tls-native = ["dep:native-tls"]
  tls-rustls = ["dep:rustls"]

First appeared: 2.2.0 (added as alternative TLS backend)
Not present in: 2.1.x (only native-tls was available)

Remediation (if pursued): direct dependency. Bump rustls to >= 0.23.5 in
backend/Cargo.toml and Cargo.lock.
```

**Scope assessment (dependency scope decision tree):** rustls is a **feature-gated optional dependency**, not a dev-only or build-only one. The production default build turns on `tls-native` only, so the rustls code is not compiled into or run by the shipped product unless someone explicitly builds with `tls-rustls`. Following the decision tree, the engineer is offered a VEX justification of **Vulnerable Code not in Execute Path** before any remediation tasks are created (see feature-gate-prompt.md). The `dev-dependency` label and the Normal priority override are **not** applied, because those apply only to dev or build dependencies.

## 2.5 – Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | unknown (no HEAD data supplied) | unknown |

The latest released 2.2.x tag (v0.4.12) still pins rustls 0.23.4. If remediation goes ahead, the safe assumption is "not fixed upstream". That means an upstream backport (bump rustls to 0.23.5 on `release/0.4.z`) followed by downstream propagation in rhtpa-release.0.4.z, unless a `release/0.4.z` HEAD check shows the fix is already there.

## Summary

- In-scope stream 2.2.x: 2.2.0–2.2.4 all lock rustls 0.23.4, which is in the affected range, **but only behind the non-default `tls-rustls` feature**.
- 2.1.x: not affected (rustls not present). There is no cross-stream impact.
- Next action: show the engineer the feature-gate VEX prompt. If they choose to skip remediation (option 1), the outcome becomes Case C: close as Not a Bug with VEX Justification (`customfield_12345`) = "Vulnerable Code not in Execute Path". Affects Versions handling is covered in Step 3.
