# Step 1 – Data Extraction: TC-8005

Source: simulated Jira issue (vuln-issue-rpm.md). No Jira MCP calls were made.

## Configuration (Step 0)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Upstream Affected Component field | not configured (Steps 4.3 and 7 skipped) |
| Version streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |

## Parsed CVE Data

| Field | Value |
|-------|-------|
| Issue key | TC-8005 |
| Status | New |
| CVE ID | CVE-2026-40215 (from label and summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed, summary suffix) | `[rhtpa-2.2]` |
| Issue stream scope | **2.2.x** (matches Version Streams row `git.example.com/rhtpa/rhtpa-release.0.4.z`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Ecosystem | RPM (system package; lock file `rpms.lock.yaml` configured in Ecosystem Mappings) |
| Affected version range | versions before 3.0.7-28.el9_4 (`< 3.0.7-28.el9_4`) |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Vulnerability | Buffer over-read in `X509_verify_cert()` SAN extension parsing |
| Upstream fix PR | none in remote links |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Assignee | Unassigned |
| Existing comments | none |
| Deployment context | not configured (Source Repositories table has no Deployment Context column; coordination guidance omitted) |

## Remediation category

RPM is a **system package** ecosystem: **1 remediation task per affected stream** (Konflux release repo fix).

## Notes on skipped / simulated steps

- **Step 0.3 (staleness)**: the mock security-matrix.md has no `<!-- Last-Updated -->` timestamp; warning only, not blocking. Consider re-running `/setup` to add one.
- **Step 0.8 (assign + transition to Assigned)**: would assign TC-8005 to the current user and transition New -> Assigned. Not executed (no Jira calls in eval).
- **Step 1.5 (MITRE / OSV enrichment)**: not queried (no external calls). Falling back to Jira description: fix threshold `3.0.7-28.el9_4`. Confidence reduced.
- **Step 1.7 (embargo)**: CVSS 7.1 meets the threshold, but no Embargo policy URL is configured, so the step is skipped.
