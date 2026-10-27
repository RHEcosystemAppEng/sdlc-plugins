# Step 1 -- Data Extraction

## Parsed CVE Data Table

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | quinn-rs/quinn#2048 (https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | GHSA-2026-qp73-x4mq (https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Status | In Progress |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged |
| Assignee | engineer-a@example.com |
| Upstream Affected Component (customfield_10632) | quinn-proto |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-server |
| Stream (customfield_10832) | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
- Scope: single-stream (scoped to 2.2.x only)

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`
- Remediation pattern: 2 tasks per stream (upstream backport + downstream propagation)

## Version Impact Analysis (from security-matrix-mock.md)

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build Tag | quinn-proto version | Affected? |
|---------|-----------|---------------------|-----------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES (< 0.11.14) |
| 2.2.1 | v0.4.8 | 0.11.12 | YES (< 0.11.14) |
| 2.2.2 | v0.4.9 | (retag of v0.4.8 = 0.11.12) | YES (< 0.11.14) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO (= 0.11.14, fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO (= 0.11.14, fixed) |

### Stream 2.1.x (rhtpa-release.0.3.z) -- cross-stream reference

| Version | Build Tag | quinn-proto version | Affected? |
|---------|-----------|---------------------|-----------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES (< 0.11.14) |
| 2.1.1 | v0.3.12 | 0.11.9 | YES (< 0.11.14) |

## Existing Issue Links (from Jira)

- **Depend**: TC-8100 -- remediation Task (upstream backport), Status: In Progress
- **Depend**: TC-8101 -- remediation Task (downstream propagation), Status: Open, Blocks TC-8100

## Existing Comments

1. Description digest comment: `sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` (posted 2026-07-01T10:00:00Z by sdlc-workflow/triage-security)
2. Post-triage summary comment (posted 2026-07-01T10:01:00Z by sdlc-workflow/triage-security)

## Existing Labels

- `CVE-2026-31812` -- CVE identifier
- `pscomponent:org/rhtpa-server` -- component label
- `ai-cve-triaged` -- triage completion marker (already present)
