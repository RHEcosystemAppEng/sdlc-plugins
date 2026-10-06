# Step 2 -- Version Impact Analysis: CVE-2026-99002

## Version Impact Table

Scope: 2.2.x stream only (issue is scoped to `[rhtpa-2.2]`)

Version Impact for CVE-2026-99002 (rustls < 0.23.5):

| Version | rustls version | Affected? | Notes |
|---------|----------------|-----------|-------|
| 2.2.0   | 0.23.4         | YES       | First version with rustls (feature-gated) |
| 2.2.1   | 0.23.4         | YES       |       |
| 2.2.2   | --             | YES       | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3   | 0.23.4         | YES       |       |
| 2.2.4   | 0.23.4         | YES       |       |

All versions in the 2.2.x stream ship rustls 0.23.4, which is within the affected range (< 0.23.5).

## Cross-stream Context (informational, outside issue scope)

The 2.1.x stream is **not affected** -- rustls is not present in any 2.1.x version (only `native-tls` was available in the 2.1.x stream).

| Version | rustls version | Affected? | Notes |
|---------|----------------|-----------|-------|
| 2.1.0   | (not present)  | NO        | rustls not a dependency in 2.1.x |
| 2.1.1   | (not present)  | NO        | rustls not a dependency in 2.1.x |

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

The vulnerable dependency `rustls` is declared as `optional = true` in `backend/Cargo.toml` and is gated behind the `tls-rustls` feature flag. The default feature set is `["tls-native"]`, which does **not** include `tls-rustls`. This means:

- The default product build does **not** compile or link rustls
- rustls is only included when a consumer explicitly enables the `tls-rustls` feature
- The product ships with `tls-native` (native-tls) as the default TLS backend

This triggers the **feature-gated optional dependency** handling from the dependency scope decision tree (Step 2.3.5). Before creating remediation tasks, the user must be prompted with a VEX justification option.
