# Step 1 – Data Extraction: TC-8051

Source: mock Jira issue (`vuln-issue-feature-gated.md`). No Jira MCP calls were made.

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8051 | Issue key |
| Issue status | New | Issue status (full triage path) |
| CVE ID | CVE-2026-99002 | Label `CVE-2026-99002` + summary text |
| Affected component | `org/rhtpa-server` | Label `pscomponent:org/rhtpa-server` (pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | rustls | Description |
| Ecosystem | Cargo (Rust crate) — source dependency | Library name + component context; listed in 2.2.x Ecosystem Mappings |
| Affected version range | < 0.23.5 ("versions before 0.23.5") | Description |
| Fixed version | 0.23.5 | Description |
| Severity | CVSS 8.1 (High) | Description |
| Vulnerability summary | Improper server certificate validation when using custom certificate verifiers (MITM with invalid chain) | Description |
| Upstream fix PR | https://github.com/rustls/rustls/pull/2100 | Remote links |
| Advisory URL | — (no GHSA/advisory link present) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 | Remote links |
| Due date | 2026-08-01 | `duedate` field |
| Assignee | Unassigned | Issue field |
| Existing comments | None | Comment history |
| Deployment context | upstream (default — Source Repositories table has no Deployment Context column) | Step 0 Source Repositories mapping |

All critical fields (CVE ID, library, affected range) were parsed successfully.

## Stream Scope Resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** (Konflux repo `git.example.com/rhtpa/rhtpa-release.0.4.z`) |
| Scope | **Scoped** — Steps 3–8 apply to the 2.2.x stream only; other streams are analyzed for cross-stream impact (Case A) |

## Configuration Notes (Steps 0 – 1.7)

- **Step 0**: Security Configuration present (Jira prefix `RHTPA`, Vulnerability type ID `10024`, component label pattern `pscomponent:`, VEX Justification field `customfield_12345`, 2 version streams, 1 source repo). Upstream Affected Component field not configured (Steps 4.3 / 7 would be skipped). Embargo policy URL not configured.
- **Step 0.3 (matrix staleness)**: matrix `Last-Updated: 2026-06-28T10:00:00Z` is ~151 days old (threshold 14 days). In interactive mode the engineer would be offered Refresh / Proceed / Stop; for this eval, proceeding with the current matrix.
- **Step 0.6**: `FULLSEND_OUTPUT_DIR` not set — interactive mode (simulated; outputs written to files instead of Jira).
- **Step 1.5 (external enrichment)**: MITRE / OSV not queried (external calls prohibited in this eval). Treated as unavailable:
  > "External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced."
  Fix threshold used for Step 2: **rustls < 0.23.5 affected; fixed in 0.23.5**.
- **Step 1.7 (embargo)**: CVSS 8.1 meets the threshold, but no Embargo policy URL is configured, so the step is skipped.
