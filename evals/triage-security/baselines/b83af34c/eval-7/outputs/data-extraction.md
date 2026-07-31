# Step 1 -- Data Extraction for TC-8006

## Extracted CVE Metadata

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| Upstream fix PR | (none in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (none) |
| CVSS | 7.5 (High) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Parsed stream: 2.1.x
- Matched Version Stream: 2.1.x (Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.3.z)
- Issue stream scope: **2.1.x only**

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Remediation task count per stream: 2 (upstream backport + downstream propagation)

## Existing Issue Links (from Jira get_issue response)

The following links already exist on TC-8006:

| Link ID | Type | Direction | Linked Issue |
|---------|------|-----------|--------------|
| 1990401 | Related | outward (TC-8006 -> TC-8001) | TC-8001 |

This existing link data is critical for Step 4.2 idempotent link checking.
