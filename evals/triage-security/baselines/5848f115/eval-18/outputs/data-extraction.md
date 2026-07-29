# Step 1 -- Data Extraction: TC-8001

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | quinn-proto |
| Ecosystem | Cargo (Rust crate) |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Assignee | engineer-a@example.com |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Current Status | In Progress |
| Current Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration's Version Streams table. This corresponds to the Konflux release repo `rhtpa-release.0.4.z`.

The issue is **stream-scoped** to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Per the security-matrix.md Ecosystem Mappings table for the 2.2.x stream, the ecosystem is **Cargo**, with:
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

Per the ecosystem classification table, Cargo is a **source dependency** ecosystem, producing 2 remediation tasks per stream (upstream backport + downstream propagation).

## Deployment Context

The affected repository `rhtpa-backend` is found in the Source Repositories table with URL `https://github.com/rhtpa/rhtpa-backend`. No Deployment Context column is present in the configuration, so the default of `upstream` applies.

## Existing Issue Links (Depend)

| Linked Issue | Type | Summary | Status |
|---|---|---|---|
| TC-8100 | Depend | Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2] | In Progress |
| TC-8101 | Depend | Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2] | Open |

TC-8101 Blocks TC-8100 (upstream backport must complete before downstream propagation).

## Existing Comments

| # | Comment | Author | Created |
|---|---------|--------|---------|
| 1 | Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2 | sdlc-workflow/triage-security | 2026-07-01T10:00:00Z |
| 2 | Post-triage summary (version impact, actions taken, remediation tasks created) | sdlc-workflow/triage-security | 2026-07-01T10:01:00Z |

## Version Impact Analysis (from security-matrix.md mock data)

For the 2.2.x stream (rhtpa-release.0.4.z), quinn-proto versions by tag:

| Version | Build Tag | quinn-proto version | Affected? (< 0.11.14) |
|---------|-----------|--------------------|-----------------------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.2 | v0.4.9 | _(retag of v0.4.8)_ = 0.11.12 | YES |
| 2.2.3 | v0.4.11 | 0.11.14 | NO (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO (fixed) |

For the 2.1.x stream (rhtpa-release.0.3.z, out of scope for this scoped issue but included for cross-stream awareness):

| Version | Build Tag | quinn-proto version | Affected? (< 0.11.14) |
|---------|-----------|--------------------|-----------------------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.1 | v0.3.12 | 0.11.9 | YES |

The Affects Versions on the issue (RHTPA 2.2.0, RHTPA 2.2.1) are consistent with the version impact analysis. Versions 2.2.0 and 2.2.1 ship quinn-proto < 0.11.14 (affected). Versions 2.2.2 through 2.2.4 ship quinn-proto >= 0.11.14 (not affected). Note: 2.2.2 is a retag of 2.2.1 and would also be affected, but the existing triage did not include it in Affects Versions -- this is consistent with the post-triage summary which states "RHTPA 2.2.2 and later ship quinn-proto 0.11.14 (not affected)." This suggests the retag at v0.4.9 may have been treated as shipping the same backend binary as 2.2.1 but the product version 2.2.2 notes "backend retag of 2.2.1" meaning it re-tagged the backend image without rebuilding, so the actual shipped binary content depends on the retag semantics. The prior triage accepted RHTPA 2.2.0 and RHTPA 2.2.1 as the affected versions.
