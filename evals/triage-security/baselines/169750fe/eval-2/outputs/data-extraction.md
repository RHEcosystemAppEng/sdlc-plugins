# Data Extraction -- Step 1

## Issue Metadata

| Field | Value |
|-------|-------|
| Issue Key | TC-8002 |
| Issue Type | Vulnerability |
| Status | New |
| Assignee | Unassigned |
| Due Date | 2026-07-30 |

## CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | N/A (not provided in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo `rhtpa-release.0.4.z`).

This is a **stream-scoped** issue -- Steps 3-4 apply only to the 2.2.x stream. However, Step 2 still analyzes all supported streams for complete version impact visibility.

## Ecosystem Detection

- **Ecosystem**: Cargo (Rust crate -- serde_json is a Cargo dependency)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`
- **Classification**: Source dependency ecosystem (would normally produce 2 remediation tasks per stream, but moot since no versions are affected)

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-28940 |

## Additional References

- https://rustsec.org/advisories/RUSTSEC-2026-0019.html

## Enriched Fix Threshold (Step 1.5)

Since external CVE API calls are not performed in this eval, the fix threshold from the Jira description is used:

- **Fix threshold**: serde_json >= 1.0.135 (not affected)
- **Affected range**: serde_json < 1.0.135 (affected)

## Embargo Check (Step 1.7)

No Embargo policy URL is configured in Security Configuration. Step 1.7 is skipped.
CVSS 5.3 (Medium) is below the Critical/Important threshold (CVSS >= 7.0) regardless.
