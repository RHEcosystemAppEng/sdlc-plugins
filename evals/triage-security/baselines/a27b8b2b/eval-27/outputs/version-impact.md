# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Loaded from security-matrix-mock.md for stream 2.2.x (rhtpa-release.0.4.z).

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Using pinned commit tags from the supportability matrix to extract rustls versions
from Cargo.lock via `git show <tag>:Cargo.lock | grep -A2 'name = "rustls"'`:

| Tag | rustls version |
|-----|----------------|
| `v0.4.5` | 0.23.4 |
| `v0.4.8` | 0.23.4 |
| `v0.4.9` | _(retag of v0.4.8)_ |
| `v0.4.11` | 0.23.4 |
| `v0.4.12` | 0.23.4 |

## Version Impact Table

Version Impact for CVE-2026-99002 (rustls < 0.23.5):

| Version | rustls | Affected? | Notes |
|---------|--------|-----------|-------|
| 2.2.0 | 0.23.4 | YES | |
| 2.2.1 | 0.23.4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.23.4 | YES | |
| 2.2.4 | 0.23.4 | YES | |

All versions in the 2.2.x stream ship rustls 0.23.4, which is within the affected
range (< 0.23.5).

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

First appeared: 2.2.0 (added as alternative TLS backend)
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

### Dependency Scope Analysis

The vulnerable dependency `rustls` is declared as an **optional dependency** gated
behind the **non-default** feature flag `tls-rustls`. The product's default feature
set is `["tls-native"]`, which does NOT include `tls-rustls`. This means:

- rustls is **compiled into the binary only when** the `tls-rustls` feature is
  explicitly enabled at build time
- The default production build does **not** include rustls code
- The vulnerable code path (certificate validation) is **not in the execute path**
  under the default feature configuration

This triggers the **feature-gated optional dependency** branch of the dependency
scope decision tree. A VEX justification prompt is presented to the user before
proceeding with remediation (see outputs/feature-gate-prompt.md).
