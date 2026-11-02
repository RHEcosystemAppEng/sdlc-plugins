# Step 2 — Version Impact Analysis

## Version Impact for CVE-2026-99002 (rustls < 0.23.5)

Scoped to stream **2.2.x** per issue suffix `[rhtpa-2.2]`.

| Version | rustls | Affected? | Notes |
|---------|--------|-----------|-------|
| 2.2.0 | 0.23.4 | YES | Pinned commit `v0.4.5` |
| 2.2.1 | 0.23.4 | YES | Pinned commit `v0.4.8` |
| 2.2.2 | — | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.23.4 | YES | Pinned commit `v0.4.11` |
| 2.2.4 | 0.23.4 | YES | Pinned commit `v0.4.12` |

All 2.2.x versions ship rustls 0.23.4, which is within the affected range (< 0.23.5).

---

## Step 2.3.5 — Dependency Chain Context

```
Dependency chain for rustls:
  backend (workspace) → rustls (direct optional dependency)
  Type: direct dependency (optional, feature-gated)
  Profile: feature-gated (optional = true, behind non-default feature "tls-rustls")
  Default features: ["tls-native"]
  The feature "tls-rustls" is NOT in the default feature set.
  The product ships with "tls-native" enabled by default.

Feature declaration (from Cargo.toml):
  [features]
  default = ["tls-native"]
  tls-native = ["dep:native-tls"]
  tls-rustls = ["dep:rustls"]

First appeared: 2.2.0 (added as alternative TLS backend via v0.4.5)
Not present in: 2.1.x (only native-tls was available)
```

### Dependency Scope Classification

rustls is declared as:
```toml
[dependencies]
rustls = { version = "0.23.4", optional = true }
```

It is an **optional dependency** gated behind the **non-default** `tls-rustls` feature flag. The default feature set is `["tls-native"]`, which does NOT include `tls-rustls`. Therefore, in default builds, rustls code is not compiled or shipped.

**Decision tree result**: Feature-gated optional dependency → present VEX justification prompt to the engineer (see `outputs/feature-gate-prompt.md`).
