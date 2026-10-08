# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-99002 (rustls < 0.23.5)

Issue is scoped to stream **2.2.x** per suffix `[rhtpa-2.2]`.

| Version | backend tag | rustls version | Affected? | Notes |
|---------|-------------|----------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.23.4 | YES | 0.23.4 < 0.23.5 (fix threshold) |
| 2.2.1 | v0.4.8 | 0.23.4 | YES | 0.23.4 < 0.23.5 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.23.4 | YES | 0.23.4 < 0.23.5 |
| 2.2.4 | v0.4.12 | 0.23.4 | YES | 0.23.4 < 0.23.5 |

All 2.2.x versions ship rustls 0.23.4, which is within the affected range (< 0.23.5).

### Cross-stream context (informational, not in scope for this issue)

rustls is **not present** in the 2.1.x stream (v0.3.8, v0.3.12). The dependency was first introduced in 2.2.0.

## Step 2.3.5 -- Dependency Chain Context

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

### Dependency scope assessment

- **Type**: direct dependency (optional)
- **Profile**: feature-gated -- `rustls` is declared with `optional = true` and is only included when the non-default feature `tls-rustls` is explicitly enabled
- **Default build**: the default feature set is `["tls-native"]`, which does **not** include `tls-rustls`. The product ships with the `tls-native` feature enabled by default.
- **Implication**: in the default build configuration, rustls is **not compiled into the binary** and its code is not present in the shipped artifact. The vulnerable code path is not in the execute path unless a consumer explicitly enables the `tls-rustls` feature.
