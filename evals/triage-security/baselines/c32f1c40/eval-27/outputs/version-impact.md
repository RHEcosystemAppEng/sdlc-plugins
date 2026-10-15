# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Loaded from security-matrix.md for the 2.2.x stream (rhtpa-release.0.4.z).

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Extracted rustls versions from `Cargo.lock` at each pinned commit tag:

| Tag | rustls version |
|-----|----------------|
| `v0.4.5` | 0.23.4 |
| `v0.4.8` | 0.23.4 |
| `v0.4.9` | _(retag of v0.4.8)_ |
| `v0.4.11` | 0.23.4 |
| `v0.4.12` | 0.23.4 |

## 2.3.5 -- Dependency Chain Context

```
Dependency chain for rustls:
  backend (workspace) -> rustls (direct optional dependency)
  Type: direct dependency (optional)
  Profile: feature-gated (optional = true, behind non-default feature "tls-rustls")
  Default features do NOT include "tls-rustls" -- the product ships with
  the "tls-native" feature enabled by default

Feature declaration:
  [features]
  default = ["tls-native"]
  tls-native = ["dep:native-tls"]
  tls-rustls = ["dep:rustls"]

First appeared: 2.2.0 (commit v0.4.5 added rustls as alternative TLS backend)
Not present in: 2.1.x (only native-tls was available)
```

**Manifest evidence:**
```toml
# backend/Cargo.toml (v0.4.5+)
[dependencies]
rustls = { version = "0.23.4", optional = true }

[features]
default = ["tls-native"]
tls-native = ["dep:native-tls"]
tls-rustls = ["dep:rustls"]
```

### Dependency Scope Classification

rustls is declared as `optional = true` in `[dependencies]` and is gated behind the `tls-rustls` feature flag, which is **not** in the `default` features list. The product ships with `default = ["tls-native"]`, meaning `tls-rustls` (and therefore rustls) is not compiled into or shipped with the production binary unless explicitly enabled by the consumer.

This is a **feature-gated optional dependency** per the dependency scope decision tree in `version-impact-analysis.md`. The VEX justification prompt applies (see `outputs/feature-gate-prompt.md`).

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-99002 (rustls < 0.23.5):

| Version | rustls | Affected? | Notes |
|---------|--------|-----------|-------|
| 2.2.0 | 0.23.4 | YES | feature-gated (tls-rustls, non-default) |
| 2.2.1 | 0.23.4 | YES | feature-gated (tls-rustls, non-default) |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.23.4 | YES | feature-gated (tls-rustls, non-default) |
| 2.2.4 | 0.23.4 | YES | feature-gated (tls-rustls, non-default) |

All versions in the 2.2.x stream ship rustls 0.23.4, which falls within the affected range (< 0.23.5). However, rustls is a feature-gated optional dependency behind the non-default `tls-rustls` feature -- the vulnerable code is not compiled into or executed by the default product build.

## 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Library | Notes |
|--------|-----------|-----------------|---------|-------|
| 2.2.x | Cargo | release/0.4.z | rustls | Upstream fix status to be verified via `git show release/0.4.z:Cargo.lock` |

Upstream fix check deferred pending engineer decision on VEX justification (see feature-gate-prompt.md). If the engineer chooses to proceed with remediation (option 2), the upstream branch will be inspected to determine whether the fix is already available.
