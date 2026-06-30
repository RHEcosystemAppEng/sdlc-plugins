# Step 1 -- Data Extraction: TC-8020

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Due date | 2026-08-15 |
| Existing comments | None |

## Stream Scope Resolution

Issue summary suffix: `[rhtpa-2.2]`
Mapped to configured Version Stream: **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)

The issue is **stream-scoped** to 2.2.x. Steps 3-7 will scope Affects Versions
and remediation to the 2.2.x stream only, while cross-stream impact on other
streams will be handled via Case B (preemptive remediation).

## Ecosystem Detection

Library: tokio (Rust crate)
Ecosystem: **Cargo**
Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock`
Source repository: backend (rhtpa-backend)

## Embargo Check (Step 1.7)

CVE-2026-55123 severity is High (CVSS 8.1, >= 7.0 threshold).
No Embargo policy URL is configured in Security Configuration.
Step 1.7 is skipped per configuration.

## External CVE Data Enrichment (Step 1.5)

Sources consulted (simulated -- no external calls in eval mode):

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | < 1.42.0 | 1.42.0 |

Enriched fix threshold: **1.42.0** (from Jira description; external APIs not queried in eval mode).
