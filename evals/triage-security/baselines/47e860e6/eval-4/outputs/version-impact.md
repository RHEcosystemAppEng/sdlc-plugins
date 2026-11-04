# TC-8004 — Step 2: Version Impact Analysis

CVE-2026-33501, h2 < 0.4.8 (fixed 0.4.8). The issue is unscoped, so **all streams** are analyzed.

Source: lock-file data in security-matrix-mock.md, standing in for `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'` at each pinned backend tag.

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

| Stream | Version | Build | backend tag (pinned) | h2 | Affected? | Notes |
|--------|---------|-------|----------------------|----|-----------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | `v0.3.8` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | 0.3.12 | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | 0.4.5 | `v0.4.5` | 0.4.8 | NO | ships the fixed version (0.4.8) |
| 2.2.x | 2.2.1 | 0.4.8 | `v0.4.8` | 0.4.8 | NO | ships the fixed version |
| 2.2.x | 2.2.2 | 0.4.9 | `v0.4.8` | — | NO | retag of 2.2.1 (same as 2.2.1, lock check skipped) |
| 2.2.x | 2.2.3 | 0.4.11 | `v0.4.11` | 0.4.9 | NO | |
| 2.2.x | 2.2.4 | 0.4.12 | `v0.4.12` | 0.4.9 | NO | |

### Mixed impact summary

| Stream | Konflux release repo | Impact |
|--------|----------------------|--------|
| **2.1.x** | rhtpa-release.0.3.z | **AFFECTED**. All released versions (2.1.0, 2.1.1) ship h2 0.4.5 |
| **2.2.x** | rhtpa-release.0.4.z | **NOT AFFECTED**. Every version from 2.2.0 on ships h2 >= 0.4.8 (0.4.8 / 0.4.9) |

### Development stream (Step 2.2)

The Jira version metadata was not queried in this eval, so the unreleased-version list isn't available. No stream beyond 2.2.x is configured, and the 2.2.x matrix says it is the latest stream. Its HEAD can't be worse than released 2.2.4 for this purpose (2.2.4 already ships h2 0.4.9), but a HEAD lock-file read was not performed. **Not assessed. Verify at branch HEAD if an unreleased RHTPA version exists.**

## Step 2.3.5 — Dependency chain

- Ecosystem: Cargo, repository `backend` (rhtpa-backend), lock file `Cargo.lock`.
- The mock data only supplies the resolved h2 version per tag. Cargo.toml and the `cargo tree` dependency path were not provided, so I'm not asserting whether h2 is direct or transitive. In Rust HTTP services h2 usually arrives transitively through hyper (for example `backend -> reqwest/axum -> hyper -> h2`). **This must be confirmed** by reading the Cargo.lock dependents at `v0.3.12` before the task is implemented.
- Profile: assumed production/runtime. h2 is an HTTP/2 runtime library, and the mock gives no dev-only indication, so normal priority handling applies and there is no `dev-dependency` label.
- Introduction point: h2 is present in every version. The 2.2.x stream moved to h2 0.4.8 by 2.2.0 (`v0.4.5`). The 2.1.x stream (`release/0.3.z`) never picked up the bump.

## Step 2.5 — Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | not available in eval data (no branch HEAD read) | **Unknown, treated as NOT fixed** |
| 2.2.x | Cargo | release/0.4.z | n/a: stream not affected | (released pins already >= 0.4.8) |

Because a fix on `release/0.3.z` can't be confirmed, the 2.1.x remediation uses the **upstream backport + downstream propagation** pair. If a HEAD check shows `release/0.3.z` already ships h2 >= 0.4.8, switch to the dependency-bump variant.

Engineer review/confirmation of this table is required before Step 3.
