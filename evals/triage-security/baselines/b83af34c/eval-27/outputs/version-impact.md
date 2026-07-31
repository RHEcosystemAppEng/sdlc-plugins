# Step 2 -- Version Impact Analysis: CVE-2026-99002 (rustls)

## Version Impact Table

Scoped to stream **2.2.x** per issue suffix `[rhtpa-2.2]`.

| Version | rustls version | Affected? | Notes |
|---------|---------------|-----------|-------|
| 2.2.0 | 0.23.4 | YES | Present in Cargo.lock but feature-gated (see dependency chain below) |
| 2.2.1 | 0.23.4 | YES | Present in Cargo.lock but feature-gated |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.23.4 | YES | Present in Cargo.lock but feature-gated |
| 2.2.4 | 0.23.4 | YES | Present in Cargo.lock but feature-gated |

All 2.2.x versions ship rustls 0.23.4, which is within the affected range (< 0.23.5).

**However**, rustls is a feature-gated optional dependency -- see dependency chain context below for VEX applicability.

## Cross-stream Check (informational, for Case A)

The 2.1.x stream does NOT ship rustls at all (not present in Cargo.lock at tags v0.3.8 and v0.3.12). Cross-stream impact does not apply for this library.

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

### Dependency Scope Analysis

The vulnerable dependency `rustls` is declared as `optional = true` in Cargo.toml
and is gated behind the `tls-rustls` feature flag. The default features are
`["tls-native"]`, which does NOT include `tls-rustls`. This means:

- When the product is built with default features (the standard build), rustls
  is NOT compiled into the binary and its code is never executed.
- rustls is only included when a user explicitly enables the `tls-rustls` feature
  flag at build time (e.g., `cargo build --features tls-rustls`).
- The product ships with the `tls-native` feature enabled by default, using
  native-tls as the TLS backend instead of rustls.

**Conclusion**: rustls is present in Cargo.lock (the resolver includes it for
completeness) but its code is NOT in the default execution path. This qualifies
for VEX justification "Vulnerable Code not in Execute Path" per the dependency
scope decision tree in the skill specification.
