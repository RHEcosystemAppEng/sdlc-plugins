# Step 1 – Data Extraction: TC-8030

Source: mock Jira issue (`vuln-issue-enrichment.md`). No Jira MCP calls were made; the
fixture stands in for `jira.get_issue` and `jira.get_issue_remote_links`.

## Step 0 – Configuration (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| VEX Justification field | customfield_12345 |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| Upstream Affected Component field | not configured, so Steps 4.3 and 7 are skipped |
| ProdSec Jira account ID | not configured, so no @mentions |
| Version streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream` and coordination guidance is omitted) |

## Extracted fields

| Field | Value | Source |
|---|---|---|
| CVE ID | CVE-2026-48901 | Label + summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | h2 (Rust crate, hyperium) | Description |
| Affected version range | **"versions prior to the fix"**. This is imprecise and gives no numeric threshold | Description |
| Fixed version | **"see advisory"**. No numeric value is given | Description |
| CVSS | 7.5 (High) | Description |
| Vulnerability | HTTP/2 CONTINUATION flood (no limit on CONTINUATION frames after HEADERS), which leads to DoS | Description |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p (also RUSTSEC-2026-0089) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 | Remote links |
| Due date | 2026-08-01 | `duedate` |
| Status | New | Issue status |
| Assignee | Unassigned | Issue |
| Existing comments | none | Comments |

## Critical-field assessment

- CVE ID: parsed.
- Library: parsed (h2).
- Affected range: **not parseable from the Jira description** ("versions prior to the fix").
  In interactive mode this would block execution until the engineer supplied a value. Here
  Step 1.5 (external CVE enrichment, which always runs) supplies a precise, machine-readable
  threshold: `< 0.4.8`, fixed in `0.4.8`. See `enrichment.md`.

## Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux repo `rhtpa-release.0.4.z`), which is a configured stream.
- **Issue stream scope: 2.2.x (scoped).** Steps 3 and 4 are scoped to 2.2.x. Other streams are handled through the cross-stream path (Case A).

## Ecosystem detection

- h2 is a Rust crate, so the ecosystem is **Cargo**. Cargo is listed in both streams' Ecosystem Mappings (repo `backend`, lock file `Cargo.lock`).
- Category: **source dependency**. Each affected stream gets two remediation tasks.

## Deployment context

- Affected repository: rhtpa-backend (backend). The Source Repositories table has no Deployment Context column, so the context defaults to `upstream` for backward compatibility, and the Coordination Guidance subsection is omitted from task descriptions.

## Step 0.8 (simulated, not executed)

Proposed: assign TC-8030 to the current user and transition New → Assigned. No Jira call was made.
