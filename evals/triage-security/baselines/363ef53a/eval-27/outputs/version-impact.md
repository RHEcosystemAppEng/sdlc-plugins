# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-99002 (rustls < 0.23.5)

Scoped to stream **2.2.x** per issue suffix `[rhtpa-2.2]`.

| Version | Tag | rustls version | Affected? | Notes |
|---------|-----|----------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.23.4 | YES | 0.23.4 < 0.23.5 |
| 2.2.1 | v0.4.8 | 0.23.4 | YES | 0.23.4 < 0.23.5 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.23.4 | YES | 0.23.4 < 0.23.5 |
| 2.2.4 | v0.4.12 | 0.23.4 | YES | 0.23.4 < 0.23.5 |

All versions in the 2.2.x stream ship rustls 0.23.4, which is within the affected range (< 0.23.5).

## Cross-stream context (informational, outside issue scope)

The 2.1.x stream does **not** ship rustls at all (not present in Cargo.lock for v0.3.8 or v0.3.12). The rustls dependency was first introduced in 2.2.0 as an alternative TLS backend.

## Step 2.3.5 -- Dependency Chain Context

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

First appeared: 2.2.0 (commit v0.4.5 added as alternative TLS backend)
Not present in: 2.1.x (only native-tls was available)
```

### Manifest evidence

```toml
# backend/Cargo.toml (v0.4.5+)
[dependencies]
rustls = { version = "0.23.4", optional = true }

[features]
default = ["tls-native"]
tls-native = ["dep:native-tls"]
tls-rustls = ["dep:rustls"]
```

### Feature gate assessment

The vulnerable dependency `rustls` is declared as `optional = true` in the workspace manifest and is gated behind the `tls-rustls` feature flag. The default feature set is `["tls-native"]`, which does **not** include `tls-rustls`. The product ships with the default features enabled, meaning rustls is **not compiled into the production binary** unless a consumer explicitly enables the `tls-rustls` feature.

Although rustls 0.23.4 appears in the Cargo.lock (because the lock file records all resolvable dependencies including optional ones), it is not included in the default build output. The vulnerable code is not present in the execute path under the default feature configuration.
