# Step 2 – Version Impact Analysis: TC-8051 (CVE-2026-99002, rustls < 0.23.5)

Sources:
- 2.1 Supportability matrix: `security-matrix-mock.md` (Last-Updated 2026-06-28, flagged as stale in Step 0.3)
- 2.3 Lock file data: the simulated `git show <tag>:Cargo.lock | grep -A2 'name = "rustls"'` output in the matrix fixture
- 2.3.5 Manifest data: the simulated `backend/Cargo.toml` evidence in the issue fixture

Issue scope: **2.2.x**. Per the rules, every supported version was checked, and 2.1.x is
included for cross-stream context.

## 2.2 – Development stream

The fixture has no Jira version metadata (no unreleased `RHTPA` versions), so no
development stream could be identified. No branch HEAD data was checked, and no
development-stream row is included. This is noted rather than invented.

## 2.4 – Version Impact Table

Version Impact for CVE-2026-99002 (rustls < 0.23.5):

| Version | Stream | backend tag | rustls (Cargo.lock) | In affected range? | Shipped by default build? | Notes |
|---------|--------|-------------|---------------------|--------------------|---------------------------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | not present | NO | n/a | out of issue scope; only native-tls existed |
| 2.1.1 | 2.1.x | v0.3.12 | not present | NO | n/a | out of issue scope; only native-tls existed |
| 2.2.0 | 2.2.x | v0.4.5 | 0.23.4 | YES | NO (feature-gated) | rustls first appeared here |
| 2.2.1 | 2.2.x | v0.4.8 | 0.23.4 | YES | NO (feature-gated) | |
| 2.2.2 | 2.2.x | v0.4.8 | — | YES | NO (feature-gated) | same as 2.2.1 (backend retag, so no lock check) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.23.4 | YES | NO (feature-gated) | |
| 2.2.4 | 2.2.x | v0.4.12 | 0.23.4 | YES | NO (feature-gated) | |

**Lock-file result:** every 2.2.x version resolves rustls 0.23.4, which is below the 0.23.5 fix.
2.1.x does not contain rustls, so there is no cross-stream impact (Case A does not apply).

**Important caveat:** `Cargo.lock` lists optional dependencies even when their feature is
off. Being in the lock file shows that rustls 0.23.4 is in the dependency graph. It does
not show that rustls is compiled into the shipped binary. The dependency chain below shows
that it is not compiled in under default features.

## 2.3.5 – Dependency Chain Context

```
Dependency chain for rustls:
  backend (workspace) → rustls (direct optional dependency)
  Type: direct dependency
  Profile: feature-gated (optional = true, behind non-default feature "tls-rustls")
  Default features do NOT include "tls-rustls". The product ships with
  the "tls-native" feature (native-tls) enabled by default.

Feature declaration (backend/Cargo.toml, v0.4.5+):
  [dependencies]
  rustls = { version = "0.23.4", optional = true }

  [features]
  default    = ["tls-native"]
  tls-native = ["dep:native-tls"]
  tls-rustls = ["dep:rustls"]

First appeared: 2.2.0 (backend v0.4.5, added as alternative TLS backend)
Not present in: 2.1.x (only native-tls was available)

Remediation (if pursued): direct dependency, so bump rustls to >= 0.23.5 in
backend/Cargo.toml (rustls = { version = "0.23.5", optional = true }) and
run cargo update -p rustls.
```

**Dependency scope decision tree:** the dependency is a feature-gated optional dependency.
It is not dev-only or build-only, so the `dev-dependency` label and Normal-priority
override do NOT apply. Before any remediation tasks are created, the engineer gets the
VEX justification prompt (see `feature-gate-prompt.md`), with
**Vulnerable Code not in Execute Path** as the recommended justification.

## 2.5 – Upstream Fix Status

The 2.2.x Upstream Branch is `release/0.4.z` (Cargo, backend). The fixture has no HEAD
lock-file data for that branch, so its status cannot be determined and is not invented.

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | unknown (no data available) | unknown |

If the engineer chooses to remediate, this must be checked
(`git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock | grep -A2 'name = "rustls"'`)
to choose between the backport and dependency-bump task variants.

## Preliminary Step 3 implication (not executed)

PSIRT set Affects Versions to RHTPA 2.2.0 only. The lock-file evidence puts rustls in the
range for 2.2.0 through 2.2.4. If the engineer chooses remediation (option 2), the
correction would add 2.2.1, 2.2.2, 2.2.3, and 2.2.4. If the engineer accepts the VEX
justification (option 1), every in-scope version is not affected, which is Case C: close
as Not a Bug with VEX `customfield_12345` = "Vulnerable Code not in Execute Path".

Waiting for the engineer to confirm this table before Step 3.
