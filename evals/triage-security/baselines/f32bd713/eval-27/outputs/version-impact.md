# Step 2 -- Version Impact Analysis: CVE-2026-99002

## Version Impact Table

Version Impact for CVE-2026-99002 (rustls versions before 0.23.5):

| Version | Stream | rustls | Affected? | Notes |
|---------|--------|--------|-----------|-------|
| 2.1.0 | 2.1.x | _(not present)_ | NO | rustls not in dependency tree |
| 2.1.1 | 2.1.x | _(not present)_ | NO | rustls not in dependency tree |
| 2.2.0 | 2.2.x | 0.23.4 | YES | Feature-gated (`tls-rustls`, non-default) |
| 2.2.1 | 2.2.x | 0.23.4 | YES | Feature-gated (`tls-rustls`, non-default) |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1; feature-gated |
| 2.2.3 | 2.2.x | 0.23.4 | YES | Feature-gated (`tls-rustls`, non-default) |
| 2.2.4 | 2.2.x | 0.23.4 | YES | Feature-gated (`tls-rustls`, non-default) |

All 2.2.x versions ship rustls 0.23.4, which is within the affected range (before 0.23.5).
However, rustls is an **optional dependency** gated behind the non-default `tls-rustls` feature flag.
The product ships with the `tls-native` feature enabled by default -- `tls-rustls` is NOT included in the default feature set.

All 2.1.x versions do NOT include rustls in the dependency tree at all (it was added in 2.2.0).

## Dependency Chain Context (Step 2.3.5)

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

### Dependency Scope Analysis

rustls is a **feature-gated optional dependency**:

- Declared in `[dependencies]` with `optional = true`
- Gated behind the `tls-rustls` feature flag
- The `tls-rustls` feature is **NOT** in the `default` feature list
- The default feature set uses `tls-native` (native-tls) instead
- The product ships with the default feature set -- `tls-rustls` is not enabled in production builds

This means the vulnerable code (rustls 0.23.4) is compiled into the binary **only** when a user explicitly enables the `tls-rustls` feature flag. Under default build configuration, rustls is not compiled and not present in the shipped artifact.

### Manifest Evidence

```toml
# backend/Cargo.toml (v0.4.5+)
[dependencies]
rustls = { version = "0.23.4", optional = true }

[features]
default = ["tls-native"]
tls-native = ["dep:native-tls"]
tls-rustls = ["dep:rustls"]
```

## Summary

- **2.1.x stream**: NOT affected -- rustls is not present in the dependency tree
- **2.2.x stream**: rustls 0.23.4 is present but gated behind non-default feature `tls-rustls`
  - All 2.2.x versions (2.2.0 through 2.2.4) ship rustls 0.23.4 (< 0.23.5 fix threshold)
  - The vulnerable code is **not in the default execution path** due to the feature gate
  - VEX justification prompt is required before proceeding with remediation decisions
