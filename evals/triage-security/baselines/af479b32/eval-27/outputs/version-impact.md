# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-99002 (rustls versions before 0.23.5)

Triage scoped to stream **2.2.x** per issue suffix `[rhtpa-2.2]`.

| Version | Stream | rustls version | Affected? | Notes |
|---------|--------|----------------|-----------|-------|
| 2.1.0 | 2.1.x | _(not present)_ | NO | rustls not a dependency in 2.1.x |
| 2.1.1 | 2.1.x | _(not present)_ | NO | rustls not a dependency in 2.1.x |
| 2.2.0 | 2.2.x | 0.23.4 | YES | 0.23.4 < 0.23.5 (fix threshold) |
| 2.2.1 | 2.2.x | 0.23.4 | YES | 0.23.4 < 0.23.5 (fix threshold) |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.23.4 | YES | 0.23.4 < 0.23.5 (fix threshold) |
| 2.2.4 | 2.2.x | 0.23.4 | YES | 0.23.4 < 0.23.5 (fix threshold) |

All versions in the 2.2.x stream ship rustls 0.23.4, which is within the affected range (before 0.23.5).

The 2.1.x stream does not include rustls at all -- it was introduced in 2.2.0 as an alternative TLS backend. No cross-stream impact.

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

Manifest evidence (backend/Cargo.toml v0.4.5+):

```toml
[dependencies]
rustls = { version = "0.23.4", optional = true }

[features]
default = ["tls-native"]
tls-native = ["dep:native-tls"]
tls-rustls = ["dep:rustls"]
```

**Key finding:** The vulnerable dependency `rustls` is an **optional dependency** gated behind the **non-default** feature flag `tls-rustls`. The default build configuration uses `tls-native` (native-tls). The `tls-rustls` feature must be explicitly enabled at compile time for rustls to be included in the binary. Under the default feature set, the rustls code is not compiled into the product.

This qualifies as a **feature-gated optional dependency** per the dependency scope decision tree. A VEX justification prompt must be presented to the user before creating remediation tasks.
