# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-99002 (rustls < 0.23.5)

Stream scope: **2.2.x** (from issue suffix [rhtpa-2.2])

| Version | rustls version | Affected? | Notes |
|---------|---------------|-----------|-------|
| 2.2.0 | 0.23.4 | YES | feature-gated (optional, non-default) |
| 2.2.1 | 0.23.4 | YES | feature-gated (optional, non-default) |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.23.4 | YES | feature-gated (optional, non-default) |
| 2.2.4 | 0.23.4 | YES | feature-gated (optional, non-default) |

All 2.2.x versions ship rustls 0.23.4, which is within the affected range (< 0.23.5). However, rustls is an **optional dependency gated behind a non-default feature flag** -- see dependency chain context below.

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

### Key Finding

The vulnerable dependency `rustls` is declared as `optional = true` in `backend/Cargo.toml` and is gated behind the `tls-rustls` feature flag. The default feature set is `["tls-native"]`, which does **not** include `tls-rustls`. This means the product ships with the `tls-native` feature enabled by default, and `rustls` is only compiled and linked when a consumer explicitly enables the `tls-rustls` feature.

Because the default build configuration does not include `rustls`, the vulnerable code is not present in the default product build. This qualifies for a VEX justification of **Vulnerable Code not in Execute Path**.
