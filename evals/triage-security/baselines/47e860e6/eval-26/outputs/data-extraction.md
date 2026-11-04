# TC-8050 — Step 1 Data Extraction

Mode: interactive (simulated). `FULLSEND_OUTPUT_DIR` is not set. Jira data comes from the fixture `vuln-issue-dev-dependency.md`; no Jira MCP calls were made.

## Step 0 – Configuration (from claude-md-security-config.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | not configured, so Step 4.3 and Step 7 are skipped |
| Embargo policy URL | not configured, so Step 1.7 is skipped (CVSS 5.3 is also below the 7.0 threshold) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`. Coordination guidance is omitted for backward compatibility) |

Step 0.3 matrix staleness: the matrix has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-04, so the matrix is about 129 days old, well past the 14-day threshold. In an interactive run the engineer would be asked to Refresh, Proceed, or Stop. For this eval we **proceed anyway** with the current matrix and record the staleness here.

Step 0.8 (simulated, not executed): assign TC-8050 to the current user and move it New → Assigned, with the transition discovered dynamically.

## Step 1 – Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8050 | Issue |
| Status | New (full triage path) | Issue status |
| CVE ID | CVE-2026-99001 | Label `CVE-2026-99001` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Component label |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | criterion (Rust crate) | Description |
| Affected version range | < 0.5.2 ("versions before 0.5.2") | Description |
| Fixed version | 0.5.2 | Description |
| CVSS / Severity | 5.3 (Medium) | Description |
| Vulnerability | Path traversal in benchmark output: crafted benchmark names containing path separators can write files to arbitrary paths | Description |
| Upstream fix PR | None in remote links | Remote links |
| Advisory URL | None (no GHSA link) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 | Remote links |
| Due date | 2026-08-01 (already past as of 2026-11-04) | `duedate` |
| Existing comments | None | Comment history |
| Assignee | Unassigned | Issue |

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to stream **2.2.x**, which is configured (Konflux repo `git.example.com/rhtpa/rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x (scoped).** Steps 3–8 apply to the 2.2.x stream only. Other streams are handled through the Case A cross-stream path.

### Ecosystem detection

- Ecosystem: **Cargo**, a source dependency. It is listed in the 2.2.x Ecosystem Mappings (backend, `Cargo.lock`, upstream branch `release/0.4.z`).
- Remediation category: source dependency, so **2 tasks per stream**.

### Deployment context

- Affected repository: rhtpa-backend (backend). The table has no Deployment Context column, so it defaults to `upstream`. The Coordination Guidance subsection is omitted because the column is absent.

## Step 1.5 – External CVE enrichment

The eval forbids external tools, so the MITRE and OSV.dev queries were not run and both are treated as unavailable.

> External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

**Fix threshold used: criterion < 0.5.2 (fixed in 0.5.2).**

## Step 1.7 – Embargo check

Skipped. No embargo policy URL is configured, and CVSS 5.3 (Medium) is below the threshold.
