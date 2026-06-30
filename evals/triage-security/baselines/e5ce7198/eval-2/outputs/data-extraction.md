# Data Extraction — TC-8002

## Step 0 — Configuration Validation

All required sections present in CLAUDE.md:

| Config Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Version Streams | 2.1.x, 2.2.x |
| Source Repositories | rhtpa-backend |

Configuration is valid. Proceeding with triage.

## Step 1 — Parsed CVE Data

| Field | Value |
|---|---|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 (< 1.0.135) |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | Not listed in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | None |
| Issue status | New |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped to stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
- This issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Vulnerable library: serde_json (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`

## Step 1.7 — Embargo Check

- CVSS: 5.3 (Medium) — below threshold (7.0)
- Embargo check: **skipped** (severity below Critical/Important threshold)
