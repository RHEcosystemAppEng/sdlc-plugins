# Step 2 -- Version Impact Analysis

## Version Impact Table

The issue is scoped to the 2.2.x stream. Using pinned commit tags from the supportability matrix for each version.

Version Impact for CVE-2026-99002 (rustls < 0.23.5):

| Version | rustls | Affected? | Notes |
|---------|--------|-----------|-------|
| 2.2.0 | 0.23.4 | YES | tag v0.4.5 |
| 2.2.1 | 0.23.4 | YES | tag v0.4.8 |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.23.4 | YES | tag v0.4.11 |
| 2.2.4 | 0.23.4 | YES | tag v0.4.12 |

All versions in the 2.2.x stream ship rustls 0.23.4, which is within the affected range (< 0.23.5).

**Note**: rustls is not present in the 2.1.x stream (tags v0.3.8, v0.3.12 show "not present"). The `tls-rustls` feature was added starting with version 2.2.0.

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

### Dependency Scope Decision Tree

rustls is declared as an `optional = true` dependency gated behind the non-default `tls-rustls` feature flag. The default features are `["tls-native"]`, which means `tls-rustls` is NOT enabled in standard builds.

**Classification**: Feature-gated optional dependency -- the vulnerable code is only compiled and included when the `tls-rustls` feature is explicitly enabled. The product ships with `tls-native` by default.

This triggers the VEX justification prompt (see feature-gate-prompt.md output).
