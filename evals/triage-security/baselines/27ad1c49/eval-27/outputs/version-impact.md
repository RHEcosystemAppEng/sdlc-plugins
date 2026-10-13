# Step 2 -- Version Impact Analysis for CVE-2026-99002

## Version Impact Table

Version Impact for CVE-2026-99002 (rustls < 0.23.5):

| Version | Stream | Source Tag | rustls version | Affected? | Notes |
|---------|--------|------------|----------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | -- (not present) | NO | rustls not in lock file |
| 2.1.1 | 2.1.x | `v0.3.12` | -- (not present) | NO | rustls not in lock file |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.23.4 | YES* | feature-gated (see dependency chain) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.23.4 | YES* | feature-gated (see dependency chain) |
| 2.2.2 | 2.2.x | `v0.4.9` | 0.23.4 | YES* | retag of 2.2.1 (same as 2.2.1); feature-gated |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.23.4 | YES* | feature-gated (see dependency chain) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.23.4 | YES* | feature-gated (see dependency chain) |

`*` = The vulnerable dependency is present in the lock file and within the affected range, but it is an optional dependency gated behind the non-default `tls-rustls` feature flag. The default feature set does NOT include `tls-rustls`. See dependency chain context below for VEX justification assessment.

## Dependency Chain Context (Step 2.3.5)

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

### Feature-gate analysis

The vulnerable dependency `rustls` is declared as `optional = true` in the workspace's
`Cargo.toml` and is only included when the `tls-rustls` feature is explicitly enabled.
The default features are `["tls-native"]`, which does **not** include `tls-rustls`.

This means:
- In the default build configuration (what the product ships), rustls is **not compiled
  into the binary** and its code is not present in the final artifact.
- rustls only becomes a dependency when a consumer explicitly opts in via
  `--features tls-rustls` or `features = ["tls-rustls"]`.
- The lock file contains rustls because Cargo resolves all possible dependencies
  (including optional ones), but the feature gate prevents it from being included in
  production builds unless explicitly enabled.

### Scope summary

- **2.1.x stream**: rustls is not present at all (not affected -- Component not Present)
- **2.2.x stream**: rustls 0.23.4 is in the lock file but gated behind non-default
  `tls-rustls` feature flag (present in lock file, but not compiled into default builds)
