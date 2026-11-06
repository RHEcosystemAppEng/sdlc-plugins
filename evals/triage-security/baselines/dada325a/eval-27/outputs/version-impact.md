# Step 2 – Version Impact Analysis: TC-8051 (CVE-2026-99002, rustls < 0.23.5)

Issue stream scope: **2.2.x**. Every supported version in every stream is still checked, per Rule 4.

## 2.1 – Supportability matrix (loaded)

Both stream matrices loaded and passed the format check: all required sections are present and the Ecosystem Mappings columns match the template.

| Stream | Konflux repo | Versions |
|--------|--------------|----------|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0 (`v0.3.8`), 2.1.1 (`v0.3.12`) |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0 (`v0.4.5`), 2.2.1 (`v0.4.8`), 2.2.2 (`v0.4.8`, backend retag of 2.2.1), 2.2.3 (`v0.4.11`), 2.2.4 (`v0.4.12`) |

## 2.2 – Development stream

No unreleased-version data was available (the eval does not allow Jira version metadata to be queried), and neither matrix has a stream newer than 2.2.x (Forward Pointer: "latest stream"). **No development stream row was evaluated.** If an unreleased RHTPA version exists, it should be checked at branch HEAD before final closure.

## 2.3 – Dependency versions (simulated `git show <tag>:Cargo.lock | grep -A2 'name = "rustls"'`)

## 2.4 – Version Impact Table

```
Version Impact for CVE-2026-99002 (rustls < 0.23.5):
```

| Version | Backend tag | rustls (Cargo.lock) | In affected range? | Shipped / executed by default? | Notes |
|---------|-------------|---------------------|--------------------|--------------------------------|-------|
| 2.1.0 | `v0.3.8` | not present | NO | N/A | Component not present; only native-tls existed in 2.1.x |
| 2.1.1 | `v0.3.12` | not present | NO | N/A | Component not present |
| 2.2.0 | `v0.4.5` | 0.23.4 | YES (lock file) | NO, feature-gated | Optional dep behind non-default `tls-rustls` feature |
| 2.2.1 | `v0.4.8` | 0.23.4 | YES (lock file) | NO, feature-gated | Optional dep behind non-default `tls-rustls` feature |
| 2.2.2 | `v0.4.8` | (same as 2.2.1) | YES (lock file) | NO, feature-gated | Retag of 2.2.1, result carried forward |
| 2.2.3 | `v0.4.11` | 0.23.4 | YES (lock file) | NO, feature-gated | Optional dep behind non-default `tls-rustls` feature |
| 2.2.4 | `v0.4.12` | 0.23.4 | YES (lock file) | NO, feature-gated | Optional dep behind non-default `tls-rustls` feature |
| dev | — | not evaluated | — | — | No development stream identified (see 2.2) |

**Summary**
- **2.1.x stream (outside scope):** not affected. rustls is absent from Cargo.lock, so the VEX justification there would be *Component not Present*. No Case A cross-stream impact.
- **2.2.x stream (in scope):** every released version (2.2.0–2.2.4) lists rustls 0.23.4 in Cargo.lock, which is inside the affected range (< 0.23.5). However, rustls is an **optional** dependency enabled only by the non-default `tls-rustls` feature. Cargo.lock records optional dependencies even when their feature is off, so lock-file presence does not mean rustls is compiled into the shipped product. The default build uses `tls-native` (native-tls).
- **Affects Versions note (input to Step 3):** PSIRT set only `RHTPA 2.2.0`. By lock-file evidence, 2.2.0–2.2.4 all carry the vulnerable version. The final correction depends on the feature-gate decision below. If the engineer picks VEX close (option 1), no Affects Versions expansion is needed.

## 2.3.5 – Dependency chain context

```
Dependency chain for rustls:
  backend (workspace) → rustls (direct optional dependency)
  Type: direct dependency
  Profile: feature-gated (optional = true, behind non-default feature "tls-rustls")
  Default features do NOT include "tls-rustls" — the product ships with
  the "tls-native" feature enabled by default

Feature declaration (backend/Cargo.toml, v0.4.5+):
  [dependencies]
  rustls = { version = "0.23.4", optional = true }

  [features]
  default = ["tls-native"]
  tls-native = ["dep:native-tls"]
  tls-rustls = ["dep:rustls"]

First appeared: 2.2.0 (backend v0.4.5, added as alternative TLS backend)
Not present in: 2.1.x (only native-tls was available)

Remediation (only if remediation proceeds): direct dependency, so bump rustls
to >= 0.23.5 in backend/Cargo.toml and Cargo.lock (cargo update -p rustls).
```

**Dependency scope decision:** this is a **feature-gated optional dependency**, not a dev-only or build-only one. Under the decision tree in version-impact-analysis.md, the engineer must be shown the VEX justification prompt (**Vulnerable Code not in Execute Path**) before any remediation tasks are created. See `feature-gate-prompt.md`. The `dev-dependency` label and the Normal-priority override do **not** apply.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | not available in fixture (simulated `git -C <rhtpa-backend> show release/0.4.z:Cargo.lock` not run) | Unknown |

The fixture has no `release/0.4.z` HEAD data. If the engineer chooses remediation (option 2), confirm upstream status before deciding between the "dependency bump + downstream" and "upstream backport + downstream" task pair.

---

Waiting for the engineer to confirm this table and answer the feature-gate prompt before Step 3.
