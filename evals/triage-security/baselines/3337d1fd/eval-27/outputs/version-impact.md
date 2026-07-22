# Step 2 -- Version Impact Analysis

## Stream Scope

Analysis scoped to **2.2.x** stream per issue suffix `[rhtpa-2.2]`.

## Version Impact Table

Version Impact for CVE-2026-99002 (rustls versions before 0.23.5):

| Version | rustls version | Affected? | Notes |
|---------|----------------|-----------|-------|
| 2.2.0 | 0.23.4 | YES | feature-gated (see dependency chain below) |
| 2.2.1 | 0.23.4 | YES | feature-gated (see dependency chain below) |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.23.4 | YES | feature-gated (see dependency chain below) |
| 2.2.4 | 0.23.4 | YES | feature-gated (see dependency chain below) |

All versions in the 2.2.x stream ship rustls 0.23.4, which is within the affected range (before 0.23.5). However, rustls is an **optional dependency gated behind a non-default feature flag** -- see dependency chain context below.

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for rustls:
  backend (workspace) -> rustls (direct optional dependency)
  Type: direct dependency (optional = true)
  Profile: feature-gated (behind non-default feature "tls-rustls")
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

**Key finding:** The vulnerable dependency `rustls` is declared as `optional = true` and is only included when the `tls-rustls` feature is explicitly enabled. The default feature set is `["tls-native"]`, which does NOT include `tls-rustls`. The product ships with `tls-native` enabled by default, meaning rustls code is not compiled into or executed by the default product build.

This qualifies as a **feature-gated optional dependency** per the dependency scope decision tree in the skill definition. Before proceeding with remediation, the user must be presented with a VEX justification option (see feature-gate-prompt.md).

## Cross-Stream Impact (2.1.x)

rustls is not present in the 2.1.x stream (only native-tls was available). No cross-stream impact for 2.1.x.
