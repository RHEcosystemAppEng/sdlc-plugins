# Step 1 – Data Extraction: TC-8001

Source: mock Jira issue `vuln-issue-standard.md` (no Jira MCP call made).

## Step 0 – Configuration check (from claude-md-security-config-embargo.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Embargo policy URL | https://example.com/security/embargo-policy (configured, so Step 1.7 runs) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend). There is no Deployment Context column. |

All required sections are present, so triage can continue.

## Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| Status | New (full triage path) | Issue status |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Component label |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field. This is wrong: no 2.0.x stream exists (see Step 3) |
| Vulnerable library | quinn-proto | Description |
| Ecosystem | Cargo (Rust crate). This is a source dependency, so 2 tasks per stream | Library name and Ecosystem Mappings |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS / Severity | 7.5 (High) | Description |
| Vulnerability type | Denial of service (panic from unbounded stream count in a STREAMS frame) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links and references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | `duedate` |
| Assignee | Unassigned. Step 0.8 would assign it to the triager and transition it to Assigned, with confirmation; not executed in this eval | Issue |
| Existing comments | None | Comments |

## Stream scope resolution

- The summary suffix `[rhtpa-2.2]` maps to the configured stream **2.2.x** (rhtpa-release.0.4.z).
- **Issue stream scope: 2.2.x.** The issue is scoped. Stream 2.1.x is outside its scope and is handled through Case A, cross-stream impact.

## Deployment context

- Affected repo: rhtpa-backend (the `backend` repository in Ecosystem Mappings). The Source Repositories table has no Deployment Context column, so the context defaults to `upstream` per Step 0. The coordination-guidance subsection is omitted in the remediation tasks for backward compatibility, per remediation-templates.md.

## Step 1.5 – External CVE data enrichment

MITRE and OSV were not queried, because the eval forbids external calls. The skill therefore falls back to the Jira description data, with reduced confidence:

> External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

Effective fix threshold: **quinn-proto < 0.11.14 is affected, and 0.11.14 is the fix.**
