# Step 2 -- Version Impact Analysis: TC-8051

## Version Impact for CVE-2026-99002 (rustls < 0.23.5)

Scope: 2.2.x stream only (issue scoped by `[rhtpa-2.2]` suffix).

| Version | rustls version | Affected? | Notes |
|---------|----------------|-----------|-------|
| 2.2.0 | 0.23.4 | YES | feature-gated (optional, non-default) |
| 2.2.1 | 0.23.4 | YES | feature-gated (optional, non-default) |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.23.4 | YES | feature-gated (optional, non-default) |
| 2.2.4 | 0.23.4 | YES | feature-gated (optional, non-default) |

All versions in the 2.2.x stream ship rustls 0.23.4, which is within the affected range (< 0.23.5). However, rustls is an optional dependency gated behind the non-default `tls-rustls` feature flag.

Note: rustls is not present in the 2.1.x stream at all (not a dependency in v0.3.8 or v0.3.12).

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for rustls:
  backend (workspace) -> rustls (direct optional dependency)
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

### Key Findings

- **Type**: direct optional dependency
- **Profile**: feature-gated -- `optional = true`, behind non-default feature `tls-rustls`
- **Default features**: `["tls-native"]` -- the product ships with native-tls, NOT rustls
- **Implication**: rustls is only compiled and linked when a consumer explicitly enables the `tls-rustls` feature flag. Under default build configuration (which is how the product is shipped), rustls code is not included in the binary.
