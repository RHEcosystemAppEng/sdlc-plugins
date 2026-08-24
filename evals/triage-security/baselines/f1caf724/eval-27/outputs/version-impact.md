# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-99002 (rustls < 0.23.5)

Scoped to stream **2.2.x** per issue suffix `[rhtpa-2.2]`.

| Version | Backend Tag | rustls version | Affected? | Notes |
|---------|-------------|----------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.23.4 | YES | feature-gated (see dependency chain below) |
| 2.2.1 | v0.4.8 | 0.23.4 | YES | feature-gated (see dependency chain below) |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.23.4 | YES | feature-gated (see dependency chain below) |
| 2.2.4 | v0.4.12 | 0.23.4 | YES | feature-gated (see dependency chain below) |

All 2.2.x versions ship rustls 0.23.4 in Cargo.lock, which is below the fix threshold of 0.23.5.

**However**: rustls is an **optional dependency** gated behind the non-default `tls-rustls` feature flag. The product ships with the `tls-native` feature enabled by default. See dependency chain context and feature-gate assessment below.

## Cross-stream Summary (informational, outside issue scope)

| Stream | rustls present? | Notes |
|--------|-----------------|-------|
| 2.1.x | No | rustls not present in 2.1.x (only native-tls was available) |
| 2.2.x | Yes (0.23.4) | Added in 2.2.0 as optional alternative TLS backend |

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for rustls:
  backend (workspace) -> rustls (direct optional dependency)
  Type: direct dependency (optional = true)
  Profile: feature-gated (optional = true, behind non-default feature "tls-rustls")

Feature declaration:
  [features]
  default = ["tls-native"]
  tls-native = ["dep:native-tls"]
  tls-rustls = ["dep:rustls"]

Default features do NOT include "tls-rustls" -- the product ships with
the "tls-native" feature enabled by default.

Manifest evidence (backend/Cargo.toml v0.4.5+):
  [dependencies]
  rustls = { version = "0.23.4", optional = true }

First appeared: 2.2.0 (added as alternative TLS backend)
Not present in: 2.1.x (only native-tls was available)
```

**Assessment**: rustls is present in the Cargo.lock for all 2.2.x versions at version 0.23.4, which is within the affected range (< 0.23.5). However, it is gated behind the `tls-rustls` feature flag which is **not** included in the default feature set. The product's default build uses `tls-native` (native-tls) instead of rustls.

This qualifies as a **feature-gated optional dependency** per the dependency scope decision tree. A VEX justification prompt must be presented to the user before proceeding with remediation (see outputs/feature-gate-prompt.md).
