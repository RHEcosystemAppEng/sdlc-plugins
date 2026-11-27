# Step 1 – Data Extraction: TC-8006

Source: mock issue `vuln-issue-sibling-prelinked.md` (simulated `jira.get_issue` +
`jira.get_issue_remote_links`; no live Jira calls were made).

## Step 0 – Configuration (from claude-md-security-config.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | not configured, so Step 4.3 is skipped |
| ProdSec Jira account ID | not configured, so no @mentions |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| Version streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source repositories | rhtpa-backend (no Deployment Context column, so defaults to `upstream`) |

All required sections are present, so validation passes.

## Extracted CVE data

| Field | Value |
|-------|-------|
| Issue key | TC-8006 |
| Status | New, so the full triage path applies |
| CVE ID | CVE-2026-31812 (from the label and the summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed, summary suffix) | `[rhtpa-2.1]` |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | none in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (plus RUSTSEC-2026-0042 in the description) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Existing comments | none |
| Existing issue links | Related → TC-8001 (link ID 1990401, outward: TC-8006 → TC-8001) |

All critical fields (CVE ID, library, affected range) were parsed.

## Stream scope resolution

- The suffix `[rhtpa-2.1]` maps to stream **2.1.x** (Konflux repo `rhtpa-release.0.3.z`).
- **Issue stream scope: 2.1.x (scoped).** Steps 3, 4 and 8 are limited to this stream.

## Ecosystem and deployment context

- Ecosystem: **Cargo** (Rust crate). It is listed in the 2.1.x Ecosystem Mappings: repo `backend`,
  lock file `Cargo.lock`, upstream branch `release/0.3.z`.
- Category: source dependency. Remediation would be 2 tasks per stream.
- Deployment context: `upstream` (the default).

## Step 1.5 note

No external calls were allowed in this eval, so MITRE and OSV were not queried. The fix
threshold comes from the Jira description only (< 0.11.14, fixed in 0.11.14), so confidence
in it is reduced.

## Step 0.3 note

The matrix `Last-Updated` timestamp is 2026-06-28. Today is 2026-11-27, so the matrix is
about 152 days old, well past the 14-day threshold. In an interactive run the engineer would be
offered Refresh / Proceed / Stop. This eval proceeds with the current matrix.

## Step 2 – Version impact (simulated lock-file data, for context)

| Stream | Version | backend tag | quinn-proto | Affected? |
|--------|---------|-------------|-------------|-----------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.x | 2.2.2 | v0.4.8 (retag) | 0.11.12 | YES |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO |

Step 3 (scoped to 2.1.x): the current Affects Versions value is correct but incomplete.
Current: [RHTPA 2.1.0]. Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]. This change needs engineer
confirmation and was not executed.
