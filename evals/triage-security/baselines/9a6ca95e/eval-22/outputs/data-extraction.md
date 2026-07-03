# Step 1 -- Data Extraction for TC-8021

## Step 0 -- Configuration Validation

Project Configuration validated from CLAUDE.md:

| Config Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component custom field | customfield_10632 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend) |

Security Configuration is complete. Proceeding with triage.

## Extracted CVE Data

| Field | Value |
|---|---|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the configured **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3 and 4 will apply only to 2.2.x versions. However, all streams are analyzed in Step 2 for cross-stream impact detection (Case B).

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. From the Ecosystem Mappings table in security-matrix.md for the 2.2.x stream:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

Detected ecosystem: **Cargo** (source dependency). This means remediation will require two tasks: an upstream backport task and a downstream propagation subtask.

## Step 2 -- Version Impact Analysis

Using quinn-proto version data from lock files at pinned commits:

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

### Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) -- both ship quinn-proto 0.11.9
- **2.2.x stream**: versions 2.2.0 through 2.2.2 are affected; versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14)

### Affects Versions Correction Needed

The PSIRT-assigned Affects Versions is `RHTPA 2.0.0`, which does not correspond to any version in the supportability matrix. This issue is scoped to stream 2.2.x, so the corrected Affects Versions should be:

- Current: `[RHTPA 2.0.0]` (incorrect -- no 2.0.x stream exists)
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` (affected 2.2.x versions based on lock file evidence)

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14, which is the fixed version.
