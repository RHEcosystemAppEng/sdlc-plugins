# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-99002 (rustls < 0.23.5)

### Scoped stream: 2.2.x

| Version | rustls | Affected? | Notes |
|---------|--------|-----------|-------|
| 2.2.0 | 0.23.4 | YES | |
| 2.2.1 | 0.23.4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.23.4 | YES | |
| 2.2.4 | 0.23.4 | YES | |

### Cross-stream check: 2.1.x

| Version | rustls | Affected? | Notes |
|---------|--------|-----------|-------|
| 2.1.0 | (not present) | NO | rustls not a dependency in 2.1.x |
| 2.1.1 | (not present) | NO | rustls not a dependency in 2.1.x |

rustls was first introduced in 2.2.0; the 2.1.x stream does not include it at all.

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

First appeared: 2.2.0 (added as alternative TLS backend)
Not present in: 2.1.x (only native-tls was available)
```

Manifest evidence:
```toml
# backend/Cargo.toml (v0.4.5+)
[dependencies]
rustls = { version = "0.23.4", optional = true }

[features]
default = ["tls-native"]
tls-native = ["dep:native-tls"]
tls-rustls = ["dep:rustls"]
```

### Feature Gate Analysis

The vulnerable dependency `rustls` is declared as `optional = true` in
`backend/Cargo.toml` and is only included when the `tls-rustls` feature is
explicitly enabled. The default feature set is `["tls-native"]`, which does
**not** include `tls-rustls`. The product ships with `tls-native` enabled by
default, meaning `rustls` is not compiled into or shipped with the default
build.

All 2.2.x versions (2.2.0 through 2.2.4) include rustls 0.23.4 in their
`Cargo.lock` (because it is declared as a dependency even if optional), but
the code is only compiled and linked when a consumer explicitly enables the
`tls-rustls` feature flag.

This qualifies for VEX justification: **Vulnerable Code not in Execute Path**.
