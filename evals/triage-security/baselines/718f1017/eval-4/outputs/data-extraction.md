# Step 1 -- Data Extraction: TC-8004

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-33501 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | _(none -- unscoped)_ | Summary has no stream suffix in brackets |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | h2 | Description text |
| Affected version range | versions before 0.4.8 (< 0.4.8) | Description text |
| Fixed version | 0.4.8 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/hyperium/h2/pull/812 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-kv8p-r3n7 | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-33501 | Remote links |
| Due date | 2026-08-01 | Issue `duedate` field |
| Existing comments | _(none)_ | Issue comment history |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" has **no** stream suffix in brackets. Per the methodology, this means the issue is **unscoped** -- it covers all configured streams. Steps 2-7 will analyze all streams (2.1.x and 2.2.x) and apply Affects Versions / remediation across all streams based on actual version impact.

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate. This maps to the **Cargo** ecosystem. Both streams' security-matrix.md files have Cargo ecosystem mappings with:
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branches: `release/0.3.z` (2.1.x stream), `release/0.4.z` (2.2.x stream)

## Step 1.5 -- External CVE Data Enrichment

External CVE databases would be queried for structured data:

- **MITRE CVE API**: `https://cveawg.mitre.org/api/cve/CVE-2026-33501`
- **OSV.dev API**: `https://api.osv.dev/v1/vulns/CVE-2026-33501`

Cross-validation: The Jira description states affected range `< 0.4.8` with fix at `0.4.8`. External sources (simulated) agree. The enriched fix threshold for Step 2.3 comparisons is **0.4.8**.

## Step 1.7 -- Embargo Check

CVSS is 7.5 (High), which meets the embargo warning threshold (>= 7.0). However, no Embargo policy URL is configured in the Security Configuration. Per methodology, Step 1.7 is skipped entirely when no embargo policy URL is configured.
