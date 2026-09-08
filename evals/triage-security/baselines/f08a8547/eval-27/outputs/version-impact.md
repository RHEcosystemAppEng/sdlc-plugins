# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-99002 (rustls < 0.23.5)

Scoped to stream **2.2.x** per issue suffix `[rhtpa-2.2]`.

| Version | rustls | Affected? | Notes |
|---------|--------|-----------|-------|
| 2.2.0 | 0.23.4 | YES | feature-gated (optional, behind non-default "tls-rustls") |
| 2.2.1 | 0.23.4 | YES | feature-gated (optional, behind non-default "tls-rustls") |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.23.4 | YES | feature-gated (optional, behind non-default "tls-rustls") |
| 2.2.4 | 0.23.4 | YES | feature-gated (optional, behind non-default "tls-rustls") |

All 2.2.x versions ship rustls 0.23.4, which is below the fix threshold of 0.23.5.
However, rustls is an **optional dependency** gated behind the non-default `tls-rustls`
feature flag. The default features enable `tls-native` only.

### Cross-stream context (out of scope for this issue)

| Version | rustls | Affected? | Notes |
|---------|--------|-----------|-------|
| 2.1.0 | (not present) | NO | rustls not a dependency in 2.1.x |
| 2.1.1 | (not present) | NO | rustls not a dependency in 2.1.x |

The 2.1.x stream does not include rustls at all (only native-tls was available).

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

**Dependency type:** Direct optional dependency
**Profile:** Feature-gated -- rustls is only included when the `tls-rustls` feature is explicitly enabled. The default build does not include rustls.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.2.x | Cargo | release/0.4.z | Upstream fix PR: rustls/rustls#2100 |
