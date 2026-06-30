# Data Extraction — TC-8002

## Step 0 — Configuration Validation

Project configuration validated from CLAUDE.md:

| Setting | Value |
|---------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |

Version Streams:
- 2.1.x: rhtpa-release.0.3.z
- 2.2.x: rhtpa-release.0.4.z

Source Repositories:
- rhtpa-backend: https://github.com/rhtpa/rhtpa-backend

## Step 1 — Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 |
| Fixed version | 1.0.135 |
| Upstream fix PR | (none linked) |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| CVSS | 5.3 (Medium) |
| Due date | 2026-07-30 |
| Existing comments | None |

### Stream Scope Resolution

The issue summary contains `[rhtpa-2.2]`, which maps to configured Version Stream **2.2.x**. This issue is **stream-scoped** to the 2.2.x stream. Steps 3-4 will apply only to versions in the 2.2.x stream.

### Ecosystem Detection

The vulnerable library is **serde_json**, a Rust crate. The ecosystem is **Cargo**. Per the 2.2.x stream's Ecosystem Mappings table:
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`
- Repository: backend

## Step 1.5 — External CVE Data Enrichment

(Simulated — no external API calls in eval mode)

External API queries would be:
- MITRE CVE API: `https://cveawg.mitre.org/api/cve/CVE-2026-28940`
- OSV.dev API: `https://api.osv.dev/v1/vulns/CVE-2026-28940`

Using Jira description data as the authoritative fix threshold:
- Affected range: versions before 1.0.135
- Fixed version: 1.0.135

## Step 1.7 — Embargo Check

CVSS is 5.3 (Medium), which is below the Critical/Important threshold (CVSS >= 7.0). Embargo check is **skipped** — severity does not meet the trigger threshold.
