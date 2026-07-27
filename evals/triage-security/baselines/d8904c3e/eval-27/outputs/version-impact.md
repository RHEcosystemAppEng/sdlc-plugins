# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-99002 (rustls < 0.23.5)

Stream scope: **2.2.x** only (per issue suffix `[rhtpa-2.2]`)

| Version | rustls | Affected? | Notes |
|---------|--------|-----------|-------|
| 2.2.0 | 0.23.4 | YES | feature-gated (optional, behind non-default `tls-rustls` feature) |
| 2.2.1 | 0.23.4 | YES | feature-gated (optional, behind non-default `tls-rustls` feature) |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.23.4 | YES | feature-gated (optional, behind non-default `tls-rustls` feature) |
| 2.2.4 | 0.23.4 | YES | feature-gated (optional, behind non-default `tls-rustls` feature) |

All 2.2.x versions ship rustls 0.23.4 which is below the fix threshold of 0.23.5.
However, rustls is an **optional dependency** gated behind the non-default `tls-rustls`
feature flag. The product ships with the `tls-native` feature enabled by default.

### Cross-stream check (informational, outside issue scope)

The 2.1.x stream is **not affected** -- rustls was not present in 2.1.x versions
(only native-tls was available).

| Version | rustls | Affected? | Notes |
|---------|--------|-----------|-------|
| 2.1.0 | _(not present)_ | NO | rustls not a dependency in 2.1.x |
| 2.1.1 | _(not present)_ | NO | rustls not a dependency in 2.1.x |

## Step 2.3.5 -- Dependency Chain Context

```
Dependency chain for rustls:
  backend (workspace) -> rustls (direct optional dependency)
  Type: direct dependency (optional)
  Profile: feature-gated (optional = true, behind non-default feature "tls-rustls")

  Default features do NOT include "tls-rustls" -- the product ships with
  the "tls-native" feature enabled by default.

  Feature declaration:
    [features]
    default = ["tls-native"]
    tls-native = ["dep:native-tls"]
    tls-rustls = ["dep:rustls"]

  Manifest evidence:
    # backend/Cargo.toml (v0.4.5+)
    [dependencies]
    rustls = { version = "0.23.4", optional = true }

  First appeared: 2.2.0 (added as alternative TLS backend)
  Not present in: 2.1.x (only native-tls was available)
```

**Key finding**: The vulnerable dependency `rustls` is present in the Cargo.lock for
all 2.2.x versions at version 0.23.4 (below the 0.23.5 fix threshold), but it is
gated behind the non-default `tls-rustls` feature flag. The default build
configuration (`default = ["tls-native"]`) does not enable this feature, meaning
the rustls code is not compiled into or executed by the default product binary.

This triggers the **feature-gated optional dependency** path from Step 2.3.5,
which requires presenting a VEX justification prompt to the user before creating
remediation tasks (see outputs/feature-gate-prompt.md).
