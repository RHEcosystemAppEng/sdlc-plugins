# Step 2 -- Version Impact Analysis: TC-8051

## CVE-2026-99002 (rustls < 0.23.5)

Stream scope: **2.2.x only** (from issue suffix `[rhtpa-2.2]`)

### Version Impact Table

| Version | Build Tag | rustls version | Affected? | Notes |
|---------|-----------|----------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.23.4 | YES | < 0.23.5 |
| 2.2.1 | `v0.4.8` | 0.23.4 | YES | < 0.23.5 |
| 2.2.2 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 0.23.4 | YES | < 0.23.5 |
| 2.2.4 | `v0.4.12` | 0.23.4 | YES | < 0.23.5 |

All released versions in the 2.2.x stream ship rustls 0.23.4, which is within the affected range (< 0.23.5).

### Cross-stream Note (informational)

The issue is scoped to 2.2.x. For reference, the 2.1.x stream does **not** include rustls at all (it was introduced in 2.2.0 as an alternative TLS backend). The 2.1.x stream is not affected by this CVE.

### 2.3.5 -- Dependency Chain Context

```
Dependency chain for rustls:
  backend (workspace) -> rustls (direct optional dependency)
  Type: direct dependency (optional = true)
  Profile: feature-gated (optional = true, behind non-default feature "tls-rustls")

  Feature declaration (from backend/Cargo.toml):
    [features]
    default = ["tls-native"]
    tls-native = ["dep:native-tls"]
    tls-rustls = ["dep:rustls"]

  Default features do NOT include "tls-rustls". The product ships with the
  "tls-native" feature enabled by default. The rustls dependency is only
  compiled and linked when a consumer explicitly enables the "tls-rustls"
  feature flag.

  First appeared: 2.2.0 (added as alternative TLS backend)
  Not present in: 2.1.x (only native-tls was available)

  Manifest evidence:
    # backend/Cargo.toml (v0.4.5+)
    [dependencies]
    rustls = { version = "0.23.4", optional = true }
```

**Dependency scope assessment:** The vulnerable dependency `rustls` is declared
as `optional = true` and gated behind the non-default feature flag `tls-rustls`.
The default feature set is `["tls-native"]`, which does NOT include `tls-rustls`.
This means the default product build does not compile, link, or ship rustls.

Per the skill's dependency scope decision tree for **feature-gated optional
dependencies**, before creating remediation tasks the engineer must be presented
with a VEX justification option. The recommended VEX justification is
**Vulnerable Code not in Execute Path**.

See `outputs/feature-gate-prompt.md` for the full prompt.
