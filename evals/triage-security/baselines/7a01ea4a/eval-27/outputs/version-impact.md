# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-99002 (rustls < 0.23.5)

Scoped to stream **2.2.x** per issue suffix `[rhtpa-2.2]`.

| Version | rustls | Affected? | Notes |
|---------|--------|-----------|-------|
| 2.2.0 | 0.23.4 | YES | feature-gated (see dependency chain below) |
| 2.2.1 | 0.23.4 | YES | feature-gated (see dependency chain below) |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.23.4 | YES | feature-gated (see dependency chain below) |
| 2.2.4 | 0.23.4 | YES | feature-gated (see dependency chain below) |

All versions in the 2.2.x stream ship rustls 0.23.4 in the lock file, which is within the affected range (< 0.23.5). However, rustls is an **optional dependency** gated behind a non-default feature flag -- see dependency chain context below.

Note: rustls is not present in the 2.1.x stream (tags v0.3.8, v0.3.12) -- it was introduced in 2.2.0 as an alternative TLS backend.

## Step 2.3.5 -- Dependency Chain Context

```
Dependency chain for rustls:
  backend (workspace) -> rustls (direct optional dependency)
  Type: direct dependency (optional = true)
  Profile: feature-gated (optional = true, behind non-default feature "tls-rustls")
  Default features do NOT include "tls-rustls" -- the product ships with
  the "tls-native" feature enabled by default

Feature declaration:
  [features]
  default = ["tls-native"]
  tls-native = ["dep:native-tls"]
  tls-rustls = ["dep:rustls"]

Manifest evidence (backend/Cargo.toml v0.4.5+):
  [dependencies]
  rustls = { version = "0.23.4", optional = true }

First appeared: 2.2.0 (added as alternative TLS backend)
Not present in: 2.1.x (only native-tls was available)
```

The vulnerable dependency `rustls` is declared as `optional = true` in `backend/Cargo.toml` and is only activated when the `tls-rustls` feature is explicitly enabled. The default feature set includes `tls-native` (which depends on `native-tls`), not `tls-rustls`. The product ships with default features, meaning rustls code is **not compiled into or executed by** the production binary under default build configuration.

This qualifies for VEX justification consideration under the "Feature-gated optional dependencies" decision tree in Step 2.3.5.
