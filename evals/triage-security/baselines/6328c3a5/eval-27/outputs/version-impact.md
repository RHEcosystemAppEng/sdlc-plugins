# Step 2 -- Version Impact Analysis

## Scope

Stream-scoped to **2.2.x** (from issue suffix `[rhtpa-2.2]`).

## Version Impact for CVE-2026-99002 (rustls < 0.23.5)

| Version | Build | Tag | rustls version | Affected? | Notes |
|---------|-------|-----|----------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.23.4 | YES | < 0.23.5; feature-gated (see dependency chain) |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.23.4 | YES | < 0.23.5; feature-gated |
| 2.2.2 | 0.4.9 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.23.4 | YES | < 0.23.5; feature-gated |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.23.4 | YES | < 0.23.5; feature-gated |

All versions in the 2.2.x stream ship rustls 0.23.4, which is within the affected range (< 0.23.5).

**However**, rustls is an **optional dependency gated behind the non-default `tls-rustls` feature flag**. The product ships with the `tls-native` feature enabled by default. See the dependency chain context below for full details.

## Cross-stream note (2.1.x)

rustls is **not present** in the 2.1.x stream (tags `v0.3.8` and `v0.3.12`). It was first added in 2.2.0 as an alternative TLS backend. The 2.1.x stream is not affected.

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

Manifest evidence (backend/Cargo.toml v0.4.5+):
  [dependencies]
  rustls = { version = "0.23.4", optional = true }

First appeared: 2.2.0 (added as alternative TLS backend)
Not present in: 2.1.x (only native-tls was available)
```

### Impact Assessment

The vulnerable dependency `rustls` is present in the Cargo.lock for all 2.2.x versions at version 0.23.4 (below the fix threshold of 0.23.5). However, it is declared as an **optional dependency** gated behind the **non-default** `tls-rustls` feature flag. The default feature set is `["tls-native"]`, which activates `native-tls` instead of `rustls`.

This means:
- Builds using the default feature set do **not** compile or link rustls
- Only builds explicitly enabling `--features tls-rustls` would include the vulnerable code
- The product as shipped with default configuration is **not affected**

This classification triggers the **feature-gated optional dependency** decision tree from the skill's dependency scope analysis (see outputs/feature-gate-prompt.md for the VEX justification prompt).
