# Step 2 -- Version Impact Analysis: TC-8051

## CVE-2026-99002 (rustls < 0.23.5)

Scoped to the **2.2.x** stream per issue suffix `[rhtpa-2.2]`.

## Version Impact Table

| Version | rustls version | Affected? | Notes |
|---------|----------------|-----------|-------|
| 2.2.0 | 0.23.4 | YES | Pinned at v0.4.5 |
| 2.2.1 | 0.23.4 | YES | Pinned at v0.4.8 |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 0.23.4 | YES | Pinned at v0.4.11 |
| 2.2.4 | 0.23.4 | YES | Pinned at v0.4.12 |

All 2.2.x versions ship rustls 0.23.4, which is below the fix threshold of 0.23.5.

## Cross-Stream Note (informational, not in scope for this issue)

The 2.1.x stream does **not** include rustls at all (it was introduced in 2.2.0). The 2.1.x stream is not affected by this CVE.

| Version | rustls version | Affected? | Notes |
|---------|----------------|-----------|-------|
| 2.1.0 | (not present) | NO | rustls not a dependency in 2.1.x |
| 2.1.1 | (not present) | NO | rustls not a dependency in 2.1.x |

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

### Dependency Scope Assessment

The vulnerable dependency `rustls` is declared as `optional = true` in the Cargo manifest and is gated behind the `tls-rustls` feature flag. The default features list is `["tls-native"]`, which does **not** include `tls-rustls`. This means:

- The product ships with `tls-native` (native-tls) enabled by default
- The `rustls` crate is only compiled and linked when a consumer explicitly enables the `tls-rustls` feature
- Under the default build configuration, `rustls` code is **not present** in the shipped binary

This qualifies as a **feature-gated optional dependency** per the skill's dependency scope decision tree. Before creating remediation tasks, the user must be presented with a VEX justification prompt (see outputs/feature-gate-prompt.md).
