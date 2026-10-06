# Step 2 -- Version Impact Analysis: TC-8051

## CVE-2026-99002 (rustls < 0.23.5)

### Version Impact Table (scoped to 2.2.x stream)

| Version | Build | backend tag | rustls version | Affected? | Notes |
|---------|-------|-------------|----------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.23.4 | YES | feature-gated (tls-rustls, non-default) |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.23.4 | YES | feature-gated (tls-rustls, non-default) |
| 2.2.2 | 0.4.9 | `v0.4.8` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.23.4 | YES | feature-gated (tls-rustls, non-default) |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.23.4 | YES | feature-gated (tls-rustls, non-default) |

All 2.2.x versions ship rustls 0.23.4, which is within the affected range (< 0.23.5). However, rustls is an **optional dependency gated behind the non-default `tls-rustls` feature flag**. The product ships with `default = ["tls-native"]`, which does NOT include `tls-rustls`.

### Cross-stream check (informational, outside issue scope)

| Stream | rustls present? | Notes |
|--------|-----------------|-------|
| 2.1.x | No | rustls not present in any 2.1.x version (only native-tls was available) |

The 2.1.x stream is **not affected** -- rustls was not yet introduced.

## Step 2.3.5 -- Dependency Chain Context

```
Dependency chain for rustls:
  backend (workspace) -> rustls (direct optional dependency)
  Type: direct dependency (optional)
  Profile: feature-gated (optional = true, behind non-default feature "tls-rustls")
  Default features do NOT include "tls-rustls" -- the product ships with
  the "tls-native" feature enabled by default

Feature declaration (from backend/Cargo.toml):
  [features]
  default = ["tls-native"]
  tls-native = ["dep:native-tls"]
  tls-rustls = ["dep:rustls"]

Manifest evidence:
  [dependencies]
  rustls = { version = "0.23.4", optional = true }

First appeared: 2.2.0 (added as alternative TLS backend)
Not present in: 2.1.x (only native-tls was available)

Remediation: bump rustls to >= 0.23.5 in backend/Cargo.toml
  (if remediation proceeds despite feature gate)
```

### Key Finding

The vulnerable library `rustls` is present in the Cargo.lock at version 0.23.4 (vulnerable), but it is an **optional dependency** gated behind the **non-default** feature flag `tls-rustls`. The default feature set enables `tls-native` instead. This means the production binary, when built with default features, does **not** include or execute the rustls code path.

This qualifies for VEX justification: **Vulnerable Code not in Execute Path**.

A feature-gate prompt must be presented to the user before proceeding with remediation (see outputs/feature-gate-prompt.md).
