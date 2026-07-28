# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-99002 (rustls < 0.23.5):

| Version | rustls version | Affected? | Notes |
|---------|---------------|-----------|-------|
| 2.2.0 | 0.23.4 | YES | pinned commit v0.4.5 |
| 2.2.1 | 0.23.4 | YES | pinned commit v0.4.8 |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.23.4 | YES | pinned commit v0.4.11 |
| 2.2.4 | 0.23.4 | YES | pinned commit v0.4.12 |

**Fix threshold**: rustls >= 0.23.5
**Result**: All 2.2.x versions ship rustls 0.23.4, which is within the
affected range (< 0.23.5). All versions are technically affected.

---

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

First appeared: 2.2.0 (commit v0.4.5 added rustls as alternative TLS backend)
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

### Dependency Scope Classification

The dependency scope decision tree identifies rustls as a **feature-gated
optional dependency**:

- **rustls** is declared with `optional = true` in `[dependencies]`
- It is gated behind the `tls-rustls` feature flag
- The `tls-rustls` feature is **NOT** included in `default` features
- Default features are: `["tls-native"]`
- The product ships with `tls-native` enabled by default, meaning rustls
  code is NOT compiled into or executed by the default production binary

This classification triggers the **feature-gated optional dependency**
path in the dependency scope decision tree, which requires presenting a
VEX justification prompt to the engineer before proceeding with
remediation (see outputs/feature-gate-prompt.md).

### SBOM Verification

SBOM verification: not applicable -- rustls is a source dependency (Cargo
ecosystem), not an RPM system package. SBOM verification applies only to
container-level dependencies.
