# Step 1 – Data Extraction: TC-8005

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Step 0 configuration validation passed
(Repository Registry, Jira Configuration, Code Intelligence, and Security Configuration
with Product Lifecycle, Version Streams, and Source Repositories are all present).

Data source: mock issue file `vuln-issue-rpm.md`. In this eval it stands in for
`jira.get_issue(TC-8005)` and `jira.get_issue_remote_links(TC-8005)`. No Jira calls were made.

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8005 | Issue |
| Issue type / Status | Vulnerability / New | Issue |
| CVE ID | CVE-2026-40215 | Label `CVE-2026-40215` + summary (match) |
| Affected component | `pscomponent:org/rhtpa-server` → `org/rhtpa-server` | Label matching the Component label pattern `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → RHTPA 2.2 | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | openssl-libs | Description |
| Ecosystem | RPM (system package, container-level) | Library name / description |
| Affected version range | versions before 3.0.7-28.el9_4 (`< 3.0.7-28.el9_4`) | Description |
| Fixed version | 3.0.7-28.el9_4 | Description |
| CVSS / Severity | 7.1 (High) | Description |
| Vulnerable code path | `X509_verify_cert()`: SAN extension length field not validated, which causes an out-of-bounds read | Description |
| Upstream fix PR | None (no GitHub PR remote link) | Remote links |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 (RHSA-2026:4021) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 | Remote links |
| Due date | 2026-08-15 (already past as of 2026-11-03) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) were parsed. No engineer input is needed.

## Stream Scope Resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** (configured Version Stream) |
| Konflux release repo | git.example.com/rhtpa/rhtpa-release.0.4.z |
| Local path | /home/dev/repos/rhtpa-release.0.4.z |
| Issue stream scope | **Scoped to 2.2.x only.** Steps 2–8 analyse only this stream. 2.1.x is out of scope. |

## Ecosystem Detection

| Item | Value |
|------|-------|
| Ecosystem | RPM. It is listed in the 2.2.x Ecosystem Mappings, so it is supported. |
| Category | System package. Remediation is 1 task per stream (Konflux release repo fix only). |
| RPM lock file configured? | Yes: `rpms.lock.yaml` (check: `git show <tag>:rpms.lock.yaml`) |
| Investigation method | Lock file + SBOM inspection |

## Deployment Context

Component `org/rhtpa-server` does not match any entry in the Source Repositories table
(only `rhtpa-backend` is listed, and there is no Deployment Context column). The context
defaults to **upstream**.

## Notes on Pre-Analysis Steps

- **Step 0.3 (Matrix staleness):** the mock security matrix has no `<!-- Last-Updated -->`
  timestamp. This is a warning only and does not block triage. Consider re-running `/setup`
  so the matrix gets a timestamp.
- **Step 0.8 (Assign + transition to Assigned):** issue is New and Unassigned. Proposed
  action: assign to the current user and transition to Assigned. Not executed, because
  this eval makes no Jira calls.
- **Step 1.5 (External enrichment):** MITRE and OSV.dev were not queried (no external
  calls in this eval). The Jira description threshold `< 3.0.7-28.el9_4` is used, so
  confidence in the fix threshold is reduced.
- **Step 1.7 (Embargo check):** CVSS 7.1 meets the threshold, but no Embargo policy URL
  is configured, so this step is skipped silently.
- **Affects Versions mismatch (Step 3 preview):** the Jira field says RHTPA 2.0.0, but
  the issue is scoped to 2.2.x. Step 2 evidence will drive the correction.
