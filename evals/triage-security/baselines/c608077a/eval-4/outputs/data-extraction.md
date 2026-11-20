# Step 1 – Data Extraction: TC-8004

Source: `vuln-issue-split.md` (simulated `jira.get_issue` + `jira.get_issue_remote_links`).
No Jira MCP, Git, or external API calls were made.

## Step 0 – Configuration (from claude-md-security-config.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Vulnerability issue type ID | 10024 |
| Jira version prefix | RHTPA |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Version streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source repository | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend) |
| Embargo policy URL | not configured → Step 1.7 skipped silently (CVSS 7.5 would otherwise trigger) |
| ProdSec Jira account ID | not configured → @mention omitted |
| Upstream Affected Component field | not configured → Step 7 (concurrent triage) skipped |

## Extracted CVE data

| Field | Value |
|-------|-------|
| Issue key | TC-8004 |
| Status | New (Unassigned) |
| CVE ID | CVE-2026-33501 (label + summary) |
| Summary | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed, summary suffix) | **none** — no bracketed stream suffix |
| Affects Versions (Jira field, current) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 (Rust crate) |
| Affected version range | < 0.4.8 |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/812 |
| Advisory URL | https://github.com/advisories/GHSA-2026-kv8p-r3n7 (also RUSTSEC-2026-0055) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-33501 |
| Due date | 2026-08-01 |
| Existing comments | none |

Note: distinct from CVE-2024-2758 (httpd CONTINUATION flood); this CVE concerns h2's
header-block accumulation. Fix adds a max header list size (default 16 KiB).

## Stream scope resolution

The summary contains **no** stream suffix in brackets → the issue is **unscoped** and
covers **all** configured streams (2.1.x and 2.2.x). Consequences:

- Step 2 analyzes every version in both streams.
- Step 3 Affects Versions correction includes affected versions from all streams
  (and only affected versions).
- Step 8 Case A (cross-stream preemptive remediation) does **not** apply; Case B
  creates remediation for every affected stream.

## Ecosystem detection

- h2 is a Rust crate → **Cargo** ecosystem (listed in both streams' Ecosystem Mappings,
  repository `backend`, lock file `Cargo.lock`).
- Classification: **source dependency** → 2 remediation tasks per affected stream.

## Deployment context

rhtpa-backend is in the Source Repositories table but no Deployment Context column is
present → coordination guidance subsection omitted from task descriptions (backward
compatibility rule).

## Step 1.5 – External enrichment (simulated)

MITRE / OSV queries were not executed (external calls prohibited in this eval).
> ⚠ External CVE databases unavailable — using Jira description data only.
> Fix threshold confidence is reduced.

Fix threshold used for Step 2: **h2 < 0.4.8 is vulnerable; 0.4.8+ is fixed**
(Jira description; consistent with the RUSTSEC reference).
