# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-99002 (rustls < 0.23.5)

Triage scoped to 2.2.x stream per issue suffix `[rhtpa-2.2]`.

| Version | Build | Backend Tag | rustls version | Affected? | Notes |
|---------|-------|-------------|----------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.23.4 | YES (feature-gated) | rustls present but behind non-default `tls-rustls` feature |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.23.4 | YES (feature-gated) | rustls present but behind non-default `tls-rustls` feature |
| 2.2.2 | 0.4.9 | `v0.4.8` | 0.23.4 | YES (feature-gated) | retag of 2.2.1 |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.23.4 | YES (feature-gated) | rustls present but behind non-default `tls-rustls` feature |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.23.4 | YES (feature-gated) | rustls present but behind non-default `tls-rustls` feature |

All 2.2.x versions ship rustls 0.23.4 (< 0.23.5 fix threshold). However,
rustls is an **optional dependency gated behind the non-default `tls-rustls`
feature flag**. The product ships with the `tls-native` feature enabled by
default. The vulnerable code is only compiled and linked when a user
explicitly enables the `tls-rustls` feature.

## 2.1.x stream reference (out of scope for this issue)

rustls is not present in the 2.1.x stream at all (tags v0.3.8 and v0.3.12).
Only native-tls was available in 2.1.x.

## Step 2.3.5 -- Dependency Chain Context

```
Dependency chain for rustls:
  backend (workspace) -> rustls (direct optional dependency)
  Type: direct dependency (optional)
  Profile: feature-gated (optional = true, behind non-default feature "tls-rustls")
  Default features do NOT include "tls-rustls" -- the product ships with
  the "tls-native" feature enabled by default

Feature declaration (from backend/Cargo.toml):
  [dependencies]
  rustls = { version = "0.23.4", optional = true }

  [features]
  default = ["tls-native"]
  tls-native = ["dep:native-tls"]
  tls-rustls = ["dep:rustls"]

First appeared: 2.2.0 (added as alternative TLS backend)
Not present in: 2.1.x (only native-tls was available)

Remediation note: rustls is a direct optional dependency. If remediation
proceeds, bump rustls to >= 0.23.5 in backend/Cargo.toml. However, since
the feature is non-default and not enabled in production builds, VEX
justification "Vulnerable Code not in Execute Path" may apply.
```
