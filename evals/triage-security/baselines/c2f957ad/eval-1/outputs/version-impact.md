# TC-8001 — Version Impact Analysis (Step 2)

> **Simulation notice:** Dependency versions come from the mock `git show <tag>:Cargo.lock`
> output supplied in `security-matrix-mock.md`. No real `git show` was executed and no
> Jira operation was performed.

## 2.1 — Supportability matrix loaded

Both streams in the Version Streams table were enumerated: `2.1.x`
(rhtpa-release.0.3.z) and `2.2.x` (rhtpa-release.0.4.z). The matrix format is valid:
Supportability Matrix, Ecosystem Mappings, Source Pinning Method, and Forward Pointer
are present, and the Ecosystem Mappings columns match the template. The staleness
warning from Step 0.3 still applies (151 days since the last update).

## 2.2 — Development stream

This requires `getJiraIssueTypeMetaWithFields` to find unreleased `RHTPA` versions.
That call was **not executed** and no unreleased-version data was supplied, so **the
development stream could not be determined**. In a live run, the matching source repo
would be checked at branch HEAD. No dev-stream row is fabricated below.

## 2.3 / 2.4 — Version Impact Table

```
Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):
```

| Version | Stream | Backend tag (pinned) | quinn-proto | Affected? | Notes |
|---------|--------|----------------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | **YES** | Outside this issue's scope (cross-stream) |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | **YES** | Outside this issue's scope (cross-stream) |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | **YES** | In scope |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | **YES** | In scope |
| 2.2.2 | 2.2.x | `v0.4.8` | — | **YES** | Same as 2.2.1 (backend retag of 2.2.1; lock-file check skipped, result carried forward) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | Ships the fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | Ships the fixed version |
| dev | — | branch HEAD | not determined | not determined | Unreleased Jira versions not available (see 2.2) |

Commands that would have produced this data (Cargo check command from Ecosystem Mappings):
`git -C /home/dev/repos/rhtpa-backend show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

**Summary:**
- **Scoped stream 2.2.x:** 2.2.0, 2.2.1, and 2.2.2 are affected. 2.2.3 and later already ship quinn-proto 0.11.14.
- **Cross-stream 2.1.x:** 2.1.0 and 2.1.1 are affected, and the latest 2.1.x release still ships 0.11.9.
- PSIRT's claimed `RHTPA 2.0.0` does not correspond to any configured stream.

## 2.3.5 — Dependency chain context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) → ... → quinn → quinn-proto   [chain not verifiable in this eval]
  Type: not determined. The mock data supplies only resolved versions, not
        Cargo.toml manifests or the [[package]] dependency graph, so direct vs
        transitive cannot be established without git show of Cargo.toml / Cargo.lock.
  Profile: assumed production pending verification. quinn-proto is the QUIC
        protocol engine, typically a runtime dependency (e.g., via quinn/reqwest
        http3); no evidence of [dev-dependencies] scope was supplied.
  Introduction point: present in all supported versions (2.1.0 onward).
  Version change: 0.11.9 (≤ 2.2.0) → 0.11.12 (2.2.1/2.2.2) → 0.11.14 (2.2.3+).

Remediation: if direct, bump quinn-proto to >= 0.11.14; if transitive, bump the
direct dependency (e.g., quinn / reqwest) first, and fall back to `cargo add quinn-proto@0.11.14`.
```

The engineer must confirm the dependency type before tasks are finalized. Remediation
templates include both the direct and transitive approaches.

## 2.5 — Upstream fix status

| Stream | Ecosystem | Repository | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|------------|-----------------|-----------------|--------|
| 2.1.x | Cargo | rhtpa-backend | `release/0.3.z` | not read (simulation) | **Unknown.** No tag on this branch ships ≥ 0.11.14; latest tag `v0.3.12` = 0.11.9 |
| 2.2.x | Cargo | rhtpa-backend | `release/0.4.z` | not read (simulation) | **Yes, per tag evidence.** Tags `v0.4.11` and `v0.4.12` cut from this branch already ship 0.11.14 |

Implications:
- **2.2.x:** the fix is already on the upstream branch **and already shipped**. The Konflux repo pins backend `v0.4.12` for 2.2.4. This stream uses the dependency-bump variant, and the work is mostly verification.
- **2.1.x:** the fix is not known to be on `release/0.3.z`. An upstream backport is needed, followed by downstream propagation in `rhtpa-release.0.3.z`.

**Gate:** the engineer reviews and confirms this table before Step 3.
