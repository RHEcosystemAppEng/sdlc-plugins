# Step 1 -- Data Extraction: TC-8060

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99010 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.5 (< 0.4.5) |
| Fixed version | 0.4.5 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99010 |
| Due date | 2026-08-15 |
| Reporter | psirt-analyst (557058:psirt-analyst-mock-id) |
| Existing comments | None |

## Stream Scope Resolution

Issue summary suffix `[rhtpa-2.2]` maps to stream **2.2.x** in the Version Streams table.
Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

- **Ecosystem**: Cargo (Rust crate -- h2 is a Rust crate)
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)
