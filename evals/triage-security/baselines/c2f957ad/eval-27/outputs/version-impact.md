# Step 2 – Version Impact Analysis: CVE-2026-99002 (rustls < 0.23.5)

**Issue stream scope:** 2.2.x (from summary suffix `[rhtpa-2.2]`). Following Important Rule 4, every supported version in both configured streams was checked so that cross-stream impact (Case A) can be judged.

**Evidence source:** the "rustls versions by tag" table in the mock lock-file data, standing in for `git show <tag>:Cargo.lock | grep -A2 'name = "rustls"'` in the `backend` repo. The Ecosystem Mappings row is Cargo, `backend`, `Cargo.lock`.

## 2.1 – Supportability Matrix (aggregated)

| Stream | Version | Build | backend tag |
|--------|---------|-------|-------------|
| 2.1.x | 2.1.0 | 0.3.8 | v0.3.8 |
| 2.1.x | 2.1.1 | 0.3.12 | v0.3.12 |
| 2.2.x | 2.2.0 | 0.4.5 | v0.4.5 |
| 2.2.x | 2.2.1 | 0.4.8 | v0.4.8 |
| 2.2.x | 2.2.2 | 0.4.9 | v0.4.8 (backend retag of 2.2.1) |
| 2.2.x | 2.2.3 | 0.4.11 | v0.4.11 |
| 2.2.x | 2.2.4 | 0.4.12 | v0.4.12 |

## 2.2 – Development Stream

Finding the development stream requires `getJiraIssueTypeMetaWithFields` to list unreleased RHTPA versions. That is a Jira call, which this eval does not make, and the fixtures contain no unreleased-version or branch-HEAD data. **The development stream could not be determined.** It is reported as a gap and no version was guessed for it.

## 2.4 – Version Impact Table

```
Version Impact for CVE-2026-99002 (rustls < 0.23.5):
```

| Version | Stream | rustls (Cargo.lock) | Affected? | Notes |
|---------|--------|---------------------|-----------|-------|
| 2.1.0 | 2.1.x | not present | NO | Not in lock file (only native-tls was available). Outside issue scope |
| 2.1.1 | 2.1.x | not present | NO | Not in lock file. Outside issue scope |
| 2.2.0 | 2.2.x | 0.23.4 | YES (feature-gated) | Optional dep behind non-default `tls-rustls`. rustls first appears here |
| 2.2.1 | 2.2.x | 0.23.4 | YES (feature-gated) | Optional dep behind non-default `tls-rustls` |
| 2.2.2 | 2.2.x | — | YES (feature-gated) | Same as 2.2.1 (backend retag of v0.4.8), result carried forward |
| 2.2.3 | 2.2.x | 0.23.4 | YES (feature-gated) | Optional dep behind non-default `tls-rustls` |
| 2.2.4 | 2.2.x | 0.23.4 | YES (feature-gated) | Optional dep behind non-default `tls-rustls` |
| dev | — | unknown | not determined | No Jira or branch-HEAD data available (see 2.2) |

**Lock-file result:** every 2.2.x release locks rustls 0.23.4, which is below the 0.23.5 fix, so all five are in the affected range. Cargo.lock records optional dependencies of workspace members even when their feature is off, so being in the lock file does **not** mean the crate is compiled into the shipped binary. The manifest context below decides that.

**Cross-stream:** 2.1.x does not ship rustls, so no other stream is affected. **Case A (cross-stream comment / preemptive tasks) does not apply.**

## 2.3.5 – Dependency Chain Context

Source: the "Mock Dependency Chain Data" in the issue fixture, standing in for `git show <tag>:backend/Cargo.toml`.

```
Dependency chain for rustls:
  backend (workspace) → rustls (direct optional dependency)
  Type: direct dependency
  Profile: feature-gated (optional = true, behind non-default feature "tls-rustls")
  Default features do NOT include "tls-rustls" — the product ships with
  the "tls-native" feature enabled by default

Feature declaration:
  [features]
  default = ["tls-native"]
  tls-native = ["dep:native-tls"]
  tls-rustls = ["dep:rustls"]

First appeared: 2.2.0 (added as alternative TLS backend)
Not present in: 2.1.x (only native-tls was available)
```

Manifest evidence (`backend/Cargo.toml`, v0.4.5 and later):

```toml
[dependencies]
rustls = { version = "0.23.4", optional = true }

[features]
default = ["tls-native"]
tls-native = ["dep:native-tls"]
tls-rustls = ["dep:rustls"]
```

**Classification (dependency scope decision tree):** this is a **feature-gated optional dependency**, not a dev-only or build-only one. rustls is only compiled when `tls-rustls` is enabled, and the default build uses `tls-native` (native-tls/OpenSSL). The shipped product therefore does not run the vulnerable rustls certificate-verification code.

**Required action:** before any remediation tasks are created, the engineer must be shown the VEX justification prompt (see `feature-gate-prompt.md`).

**Remediation path if the engineer chooses to proceed anyway:** rustls is a direct dependency, so the fix is a simple bump: `rustls = { version = ">=0.23.5", optional = true }` in `backend/Cargo.toml` and `cargo update -p rustls`. That means 2 tasks for the 2.2.x stream: an upstream bump or backport on `release/0.4.z`, plus downstream propagation in `rhtpa-release.0.4.z`. Per the decision tree, option 2 tasks get no extra labels and no priority changes.

**Caveat to verify:** the gate only holds if the Konflux build of `rhtpa-server` uses default features. If the container build passes `--features tls-rustls` or `--all-features`, rustls ships and the VEX claim is invalid. The fixture only provides the manifest, not the Konflux build arguments.

## 2.5 – Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | not available (no `git show release/0.4.z:Cargo.lock` data in fixtures) | unknown |

The 2.1.x stream is not affected, so no upstream check is needed there. If remediation goes ahead, check `release/0.4.z` first to decide between the "dependency bump" and "upstream backport" templates.

## Preliminary Outcome (pending engineer decision)

- **Affects Versions (Step 3 preview):** PSIRT set RHTPA 2.2.0. The lock-file evidence shows 2.2.0 through 2.2.4 all lock rustls 0.23.4. If the engineer chooses remediation, the proposed correction is RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4. If the engineer accepts the VEX justification, this is moot because the issue is closed as not affected.
- **Option 1 (recommended):** every in-scope version is not affected through the feature gate. No other stream is affected and the dev stream is unknown, so the overall issue can be closed as **Not a Bug** with VEX Justification (customfield_12345) = **Vulnerable Code not in Execute Path**, after confirmation.
- **Option 2:** Case B, 2 Cargo remediation tasks for 2.2.x with standard labels and priority.

Waiting for the engineer to review this table and answer the feature-gate prompt before moving to Step 3.
