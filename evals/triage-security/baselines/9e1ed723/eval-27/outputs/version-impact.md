# Step 2 – Version Impact Analysis: TC-8051

Data sources: fixture `security-matrix-mock.md` (simulated `git show <tag>:Cargo.lock` output) and fixture dependency-chain data in `vuln-issue-feature-gated.md` (simulated manifest inspection). No real `git show` executed.

## 2.1 – Supportability matrix (in-scope stream 2.2.x)

| Version | Build | backend tag | Notes |
|---|---|---|---|
| 2.2.0 | 0.4.5 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | `v0.4.12` | |

Ecosystem: Cargo, repository backend, lock file `Cargo.lock`, upstream branch `release/0.4.z`.

## 2.2 – Development stream

Jira unreleased-version lookup not performed (no Jira access in eval) and no development-head lock data in fixtures. Development stream: **not determined** — would require `getJiraIssueTypeMetaWithFields` and `git show HEAD:Cargo.lock` in a live run.

## 2.4 – Version impact table

Version Impact for CVE-2026-99002 (rustls < 0.23.5) — stream 2.2.x:

| Version | rustls | In lock file? | Within affected range? | Affected? | Notes |
|---------|--------|---------------|------------------------|-----------|-------|
| 2.2.0 | 0.23.4 | Yes | Yes | YES (feature-gated) | optional dep, behind non-default `tls-rustls` |
| 2.2.1 | 0.23.4 | Yes | Yes | YES (feature-gated) | optional dep, behind non-default `tls-rustls` |
| 2.2.2 | — | — | — | YES (feature-gated) | same as 2.2.1 (backend retag of `v0.4.8`) |
| 2.2.3 | 0.23.4 | Yes | Yes | YES (feature-gated) | optional dep, behind non-default `tls-rustls` |
| 2.2.4 | 0.23.4 | Yes | Yes | YES (feature-gated) | optional dep, behind non-default `tls-rustls` |

By version number alone, every 2.2.x release ships rustls 0.23.4 (< 0.23.5) in `Cargo.lock`. However, the dependency is **optional** and only compiled when the non-default `tls-rustls` feature is enabled; the shipped product uses the default `tls-native` feature. The vulnerable code is therefore not in the default execution path — see the feature-gate prompt (`feature-gate-prompt.md`).

### Cross-stream check (out of scope, informational)

| Version | rustls | Affected? | Notes |
|---------|--------|-----------|-------|
| 2.1.0 | not present | NO | `v0.3.8` — rustls absent from Cargo.lock |
| 2.1.1 | not present | NO | `v0.3.12` — rustls absent from Cargo.lock |

No other stream is affected, so Case A (cross-stream impact comment / preemptive tasks) does not apply.

## 2.3.5 – Dependency chain context

```
Dependency chain for rustls:
  backend (workspace) → rustls
  Type: direct optional dependency
  Profile: feature-gated (optional = true, behind non-default feature "tls-rustls")
  Default features do NOT include "tls-rustls" — product ships with the
  "tls-native" feature (native-tls) enabled by default

Feature declaration (backend/Cargo.toml, v0.4.5+):
  [dependencies]
  rustls = { version = "0.23.4", optional = true }

  [features]
  default = ["tls-native"]
  tls-native = ["dep:native-tls"]
  tls-rustls = ["dep:rustls"]

First appeared: 2.2.0 (added as alternative TLS backend)
Not present in: 2.1.x (only native-tls was available)

Remediation (if pursued): bump rustls to >= 0.23.5 in backend/Cargo.toml
(direct dependency — simple version bump, no transitive pinning needed)
```

Dependency scope decision tree result: **feature-gated optional dependency** (not dev/build-only). Per `version-impact-analysis.md`, before creating remediation tasks the engineer is presented with the VEX justification option **Vulnerable Code not in Execute Path** (see `feature-gate-prompt.md`). No `dev-dependency` label or priority override applies.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | unknown (no fixture data; `git -C <backend> show release/0.4.z:Cargo.lock` not run) | Unknown |

If remediation is chosen and the upstream branch is not fixed, the path is: upstream backport (bump rustls to 0.23.5 on `release/0.4.z`) + downstream propagation in rhtpa-release.0.4.z (2 tasks, Cargo source dependency).

## Awaiting engineer confirmation

Please review the version impact table before proceeding to Step 3 (Affects Versions correction). Note: if remediation proceeds, PSIRT's Affects Versions (RHTPA 2.2.0 only) is incomplete — lock file evidence shows 2.2.0 through 2.2.4 all ship rustls 0.23.4. If the VEX/close option is chosen, all 2.2.x versions are not affected in the default build.
