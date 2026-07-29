# Step 2 -- Version Impact Analysis: TC-8051

## Version Impact for CVE-2026-99002 (rustls < 0.23.5)

### Scoped stream: 2.2.x

| Version | rustls version | Affected? | Notes |
|---------|----------------|-----------|-------|
| 2.2.0   | 0.23.4         | YES       | first version with rustls (feature-gated) |
| 2.2.1   | 0.23.4         | YES       |       |
| 2.2.2   | --             | YES       | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3   | 0.23.4         | YES       |       |
| 2.2.4   | 0.23.4         | YES       |       |

All versions in the 2.2.x stream ship rustls 0.23.4, which is within the affected range (< 0.23.5).

**However**: rustls is an **optional dependency gated behind the non-default `tls-rustls` feature flag**. The product ships with the `tls-native` feature enabled by default. See the dependency chain context and feature-gate prompt below.

### Cross-stream check (Case A)

Since this issue is scoped to 2.2.x, we also check other configured streams for cross-stream impact:

| Stream | rustls present? | Notes |
|--------|-----------------|-------|
| 2.1.x  | No              | rustls not present in v0.3.8 or v0.3.12; only native-tls was available in 2.1.x |

The 2.1.x stream is **not affected** -- rustls was not introduced until 2.2.0. No cross-stream impact notice is needed.

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for rustls:
  backend (workspace) -> rustls (direct optional dependency)
  Type: direct dependency (optional)
  Profile: feature-gated (optional = true, behind non-default feature "tls-rustls")
  Default features do NOT include "tls-rustls" -- the product ships with
  the "tls-native" feature enabled by default

Feature declaration (from backend/Cargo.toml):
  [features]
  default = ["tls-native"]
  tls-native = ["dep:native-tls"]
  tls-rustls = ["dep:rustls"]

Manifest evidence (backend/Cargo.toml v0.4.5+):
  rustls = { version = "0.23.4", optional = true }

First appeared: 2.2.0 (added as alternative TLS backend)
Not present in: 2.1.x (only native-tls was available)
```

The vulnerable dependency `rustls` is declared as `optional = true` in the Cargo manifest and is only included when the `tls-rustls` feature is explicitly enabled. The default feature set is `["tls-native"]`, which does not include `tls-rustls`. This means:

- **Default builds** do not compile or link rustls -- the vulnerability is not reachable.
- **Only builds with `--features tls-rustls`** (or `--all-features`) would include the vulnerable code path.
- The product ships with the default feature set (`tls-native`), so production deployments are not affected unless a customer explicitly enables the `tls-rustls` feature.

This qualifies for the **feature-gated optional dependency** handling per the dependency scope decision tree. See `outputs/feature-gate-prompt.md` for the VEX justification prompt.
