# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-99002 (rustls < 0.23.5):

| Version | Pinned Commit | rustls version | Affected? | Notes |
|---------|---------------|----------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.23.4 | YES | < 0.23.5 |
| 2.2.1 | `v0.4.8` | 0.23.4 | YES | < 0.23.5 |
| 2.2.2 | `v0.4.8` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 0.23.4 | YES | < 0.23.5 |
| 2.2.4 | `v0.4.12` | 0.23.4 | YES | < 0.23.5 |

All versions in the 2.2.x stream ship rustls 0.23.4, which is within the affected range (< 0.23.5).

---

## Step 2.3.5 -- Dependency Chain Context

```
Dependency chain for rustls:
  backend (workspace) -> rustls (direct optional dependency)
  Type: direct dependency (optional, feature-gated)
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

rustls is declared as an **optional dependency** (`optional = true`) in the `[dependencies]` section of the Cargo manifest. It is gated behind the **`tls-rustls`** feature flag, which is **not included in the default features**. The default features list is `["tls-native"]`, meaning the product ships with `native-tls` as the TLS backend, not `rustls`.

Since `tls-rustls` is a non-default feature:
- **Production builds using default features do NOT include rustls** in the compiled binary
- rustls is only compiled and linked when a user explicitly enables the `tls-rustls` feature flag
- The vulnerable code path (certificate validation in rustls) is not reachable in default builds

This triggers the **feature-gated optional dependency** path of the dependency scope decision tree. A VEX justification prompt is presented to the user (see outputs/feature-gate-prompt.md).
