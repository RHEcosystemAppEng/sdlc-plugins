# Step 2 – Version Impact Analysis: CVE-2026-99002 (rustls < 0.23.5)

Issue: TC-8051 — scoped to stream **2.2.x** (`[rhtpa-2.2]`).
Lock file data comes from the simulated `git show <tag>:Cargo.lock | grep -A2 'name = "rustls"'` output in `security-matrix-mock.md`. Manifest data comes from the mock dependency chain data in the issue fixture.

## Version Impact Table

All supported versions were checked (rule 4), not only the scoped stream.

| Version | Stream | backend tag | rustls (Cargo.lock) | In affected range? | Notes |
|---------|--------|-------------|---------------------|--------------------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | not present | NO | rustls not in lock file → not a dependency |
| 2.1.1 | 2.1.x | `v0.3.12` | not present | NO | rustls not in lock file → not a dependency |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.23.4 | YES (version) — **feature-gated** | optional dep behind non-default `tls-rustls` |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.23.4 | YES (version) — **feature-gated** | optional dep behind non-default `tls-rustls` |
| 2.2.2 | 2.2.x | `v0.4.8` | — | YES (version) — **feature-gated** | retag of 2.2.1 (same as 2.2.1; check skipped) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.23.4 | YES (version) — **feature-gated** | optional dep behind non-default `tls-rustls` |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.23.4 | YES (version) — **feature-gated** | optional dep behind non-default `tls-rustls` |
| dev stream | — | branch HEAD | not available | — | Step 2.2: no unreleased Jira version data available in the fixture; development stream could not be identified/checked |

**Summary**: Every 2.2.x version resolves rustls 0.23.4 in Cargo.lock, which is inside the affected range (< 0.23.5). However, rustls is an **optional** dependency enabled only by the non-default `tls-rustls` feature; the default build uses `tls-native` (native-tls). The 2.1.x stream does not contain rustls at all, so there is **no cross-stream impact** (Case A does not apply).

Note: Cargo.lock records optional dependencies regardless of which features are enabled, so lock-file presence alone does not prove that rustls is compiled into the shipped binary. The manifest evidence below shows it is not part of the default feature set.

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for rustls:
  backend (workspace) → rustls (direct optional dependency)
  Type: direct dependency
  Profile: feature-gated (optional = true, behind non-default feature "tls-rustls")
  Default features do NOT include "tls-rustls" — the product ships with
  the "tls-native" feature enabled by default (native-tls backend)

Feature declaration (backend/Cargo.toml, v0.4.5+):
  [dependencies]
  rustls = { version = "0.23.4", optional = true }

  [features]
  default = ["tls-native"]
  tls-native = ["dep:native-tls"]
  tls-rustls = ["dep:rustls"]

First appeared: 2.2.0 (added as alternative TLS backend)
Not present in: 2.1.x (only native-tls was available)

Remediation (if pursued): direct dependency — bump rustls to >= 0.23.5 in
backend/Cargo.toml and Cargo.lock.
```

### Dependency scope decision

Per the dependency scope decision tree in `version-impact-analysis.md`, this is a **feature-gated optional dependency** (Cargo `[dependencies]` with `optional = true`, gated behind a non-default feature). It is NOT a dev-only/build-only dependency, so the `dev-dependency` label / Normal-priority override does not apply. Instead, before any remediation tasks are created, the engineer must be presented with the VEX justification option (recommended: **Vulnerable Code not in Execute Path**). See `feature-gate-prompt.md`.

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Repository | Upstream Branch | rustls at HEAD | Fixed? |
|--------|-----------|------------|-----------------|----------------|--------|
| 2.2.x | Cargo | backend | `release/0.4.z` | not available | Unknown — no branch HEAD data in fixture (no `git show` executed) |

## Next Step

Awaiting engineer confirmation of this table and a decision on the feature-gate VEX prompt before proceeding to Step 3 (Affects Versions correction) and Step 8 (remediation vs. close).
