# Step 1 -- Data Extraction for TC-8021

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.1 (from summary suffix `[rhtpa-2.1]`) |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 |
| Existing comments | (none) |

## Custom Fields

| Field | Value |
|-------|-------|
| Upstream Affected Component (customfield_10632) | tokio |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-server |
| Stream (customfield_10832) | rhtpa-2.1 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (matches Version Streams table row for stream 2.1.x, Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`)
- Issue stream scope: **scoped to 2.1.x only**

## Ecosystem Detection

- Vulnerable library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z` (from stream 2.1.x Ecosystem Mappings)

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |

## Issue Links

No existing issue links on TC-8021.

## Embargo Check (Step 1.7)

- Embargo policy URL: not configured in Security Configuration
- Step 1.7 is **skipped** (no embargo policy URL configured).

## Notes

- The issue description explicitly states that a proactive remediation task (TC-8022) already exists for this stream, created from prior cross-stream triage of TC-8020 (stream rhtpa-2.2). This will be handled in Step 4.4.
