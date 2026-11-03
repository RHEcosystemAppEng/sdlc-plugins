# TC-8002 — Version Impact Analysis (Step 2)

## 2.1 – Supportability matrix loaded

Source: `security-matrix-mock.md`, covering both configured Version Streams. The matrix is in the expected format: Supportability Matrix, Source Pinning Method, and Ecosystem Mappings sections are all present.

| Stream | Konflux repo | Versions | Backend pinning |
|---|---|---|---|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0, 2.1.1 | `artifacts.lock.yaml` tag |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4 | `artifacts.lock.yaml` tag |

Staleness caveat: the matrix is 128 days old (see data-extraction.md, Step 0.3).

## 2.2 – Development stream

- Detecting the development stream needs `getJiraIssueTypeMetaWithFields` to list unreleased `RHTPA` versions. The eval forbids Jira calls, so **no Jira version data is available**, and the input files contain no development-stream lock data at branch HEAD.
- Result: **development stream not assessed.** It is marked "not determined" below rather than guessed. Every released version, including the oldest ones, ships serde_json 1.0.137 or later, and Cargo.lock versions of serde_json only move forward in these tags. A development HEAD is therefore very unlikely to regress below 1.0.135. A real run must still confirm this with `git show HEAD:Cargo.lock` in rhtpa-backend.

## 2.3 – Dependency versions at pinned commits

Simulated output of `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`, taken from the "serde_json versions by tag" mock data.

Fix threshold: vulnerable if `< 1.0.135`. Source: Jira description. External enrichment was unavailable.

## 2.4 – Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | Backend tag | serde_json | Affected? | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 2.1.x | `v0.3.8` | 1.0.137 | **NO** | 1.0.137 ≥ 1.0.135 |
| 2.1.1 | 2.1.x | `v0.3.12` | 1.0.137 | **NO** | 1.0.137 ≥ 1.0.135 |
| 2.2.0 | 2.2.x | `v0.4.5` | 1.0.138 | **NO** | 1.0.138 ≥ 1.0.135. PSIRT listed this version as affected, which is incorrect |
| 2.2.1 | 2.2.x | `v0.4.8` | 1.0.138 | **NO** | 1.0.138 ≥ 1.0.135 |
| 2.2.2 | 2.2.x | `v0.4.8` | — | **NO** | Retag of 2.2.1 (backend `v0.4.8`). Lock check skipped, result carried forward from 2.2.1 |
| 2.2.3 | 2.2.x | `v0.4.11` | 1.0.139 | **NO** | 1.0.139 ≥ 1.0.135 |
| 2.2.4 | 2.2.x | `v0.4.12` | 1.0.139 | **NO** | 1.0.139 ≥ 1.0.135 |
| dev (unreleased) | — | branch HEAD | not determined | not determined | No Jira version metadata or HEAD lock data in eval inputs (see 2.2) |

**Summary:** None of the 7 released supported versions in either stream ships a vulnerable serde_json. The oldest shipped version is 1.0.137, which is already 2 patch releases past the fix (1.0.135).

- Issue scope (2.2.x): 0 of 5 versions affected.
- Cross-stream (2.1.x): 0 of 2 versions affected.

## 2.3.5 – Dependency chain context

No version is affected, so remediation-oriented chain tracing is not needed. For the record:

```
Dependency chain for serde_json:
  backend (workspace) → serde_json   (Cargo.lock evidence only; Cargo.toml not provided in eval inputs)
  Type: not determined (direct vs transitive needs Cargo.toml / `cargo tree`; not needed since not affected)
  Profile: not determined (not needed since not affected)
  Present in all supported versions at 1.0.137–1.0.139 (patched)
```

## 2.5 – Upstream fix check

No stream is affected, so no remediation path is needed. The upstream branches (`release/0.3.z`, `release/0.4.z`) were not inspected because the eval forbids git calls and no HEAD data was supplied. The newest pinned tags on those branches (`v0.3.12`: 1.0.137, `v0.4.12`: 1.0.139) already ship the fix.

| Stream | Ecosystem | Upstream Branch | Latest pinned tag version | Fixed? |
|---|---|---|---|---|
| 2.1.x | Cargo | release/0.3.z | 1.0.137 (`v0.3.12`) | YES (already patched) |
| 2.2.x | Cargo | release/0.4.z | 1.0.139 (`v0.4.12`) | YES (already patched) |
