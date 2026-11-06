# TC-8004 — Step 2 Version Impact Analysis

## 2.1 – Supportability matrix (aggregated)

| Stream | Konflux Release Repo | Versions |
|--------|----------------------|----------|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0 (`v0.3.8`), 2.1.1 (`v0.3.12`) |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0 (`v0.4.5`), 2.2.1 (`v0.4.8`), 2.2.2 (`v0.4.8`, retag of 2.2.1), 2.2.3 (`v0.4.11`), 2.2.4 (`v0.4.12`) |

Matrix format: both streams contain Supportability Matrix, Source Pinning Method,
Ecosystem Mappings (Ecosystem | Repository | Lock File | Check Command | Upstream Branch),
and Forward Pointer → **Pass**.

## 2.2 – Development stream

No unreleased RHTPA Jira version data is available in this eval (Jira not queried), so no
development stream could be identified. The 2.2.x stream is the latest configured stream
(no forward pointer). **Flag for engineer:** if an unreleased RHTPA version exists, its
branch HEAD must be checked before finalizing.

## 2.3 – Lock file evidence (Cargo.lock at pinned commits)

Simulated output of `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'` taken from the
mock lock file data. Fix threshold: **h2 < 0.4.8 affected**.

## 2.4 – Version Impact Table

Version Impact for CVE-2026-33501 (h2 < 0.4.8):

| Stream | Version | Backend tag (pinned) | h2 | Affected? | Notes |
|--------|---------|----------------------|----|-----------|-------|
| 2.1.x | 2.1.0 | `v0.3.8`  | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | `v0.4.5`  | 0.4.8 | NO | ships fixed version (0.4.8) |
| 2.2.x | 2.2.1 | `v0.4.8`  | 0.4.8 | NO | ships fixed version |
| 2.2.x | 2.2.2 | `v0.4.8`  | —     | NO | same as 2.2.1 (backend retag; lock check skipped, result carried forward) |
| 2.2.x | 2.2.3 | `v0.4.11` | 0.4.9 | NO | |
| 2.2.x | 2.2.4 | `v0.4.12` | 0.4.9 | NO | |

### Mixed impact summary

| Stream | Impact | Detail |
|--------|--------|--------|
| **2.1.x** | **AFFECTED** (all versions) | Every 2.1.x release ships h2 0.4.5 (vulnerable) |
| **2.2.x** | **NOT AFFECTED** (all versions) | Every 2.2.x release ships h2 0.4.8 or 0.4.9 (patched); the stream picked up the fix from its first release (2.2.0) |

PSIRT's Affects Versions (RHTPA 2.1.0, RHTPA 2.2.0) is therefore partially wrong:
2.2.0 is not affected, and 2.1.1 is affected but missing.

## 2.3.5 – Dependency chain context

- Repository: `backend` (rhtpa-backend), ecosystem Cargo, lock file `Cargo.lock`.
- Direct vs transitive: **not determinable from the available evidence** — the mock
  provides only the resolved h2 version, not `Cargo.toml` manifests or the `[[package]]`
  dependency graph. h2 is typically pulled in transitively (e.g. via hyper / reqwest /
  tonic), but this is not asserted without `git show v0.3.12:Cargo.lock` dependency data.
  The engineer should run `cargo tree -i h2` on `release/0.3.z` to confirm the chain.
- Profile: assumed production (h2 is an HTTP/2 runtime library); not verified as dev-only,
  so no `dev-dependency` label / priority override is applied.
- Introduction point: h2 is present in both streams; the 2.2.x stream moved to h2 0.4.8
  at backend `v0.4.5` (2.2.0), while 2.1.x stayed at 0.4.5.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | unknown (not available in mock data) | **Not confirmed** |
| 2.2.x | Cargo | `release/0.4.z` | n/a — stream not affected | n/a (all released versions already >= 0.4.8) |

Because the fix on `release/0.3.z` cannot be confirmed, the 2.1.x remediation uses the
**upstream backport + downstream propagation** pair (not the dependency-bump variant).

## Steps 4–7 (supporting checks)

- **Step 4 – Siblings:** JQL `project = TC AND labels = 'CVE-2026-33501' AND issuetype = 10024 AND key != TC-8004` returned no results → no duplicates, no companion trackers, no links.
- **Step 4.3 – Cross-CVE overlap:** skipped (Upstream Affected Component field not configured).
- **Step 4.4 – Preemptive reconciliation:** no `security-preemptive` tasks for CVE-2026-33501 (assumed empty, consistent with no siblings).
- **Step 5 – Lifecycle:** product pages not fetched (no external calls). 2.1.x assumed supported; engineer should confirm 2.1.x is not EOL before task creation.
- **Step 6 – Already fixed:** no resolved siblings → proceed.
- **Step 7 – Concurrent triage:** skipped (Upstream Affected Component field not configured).
