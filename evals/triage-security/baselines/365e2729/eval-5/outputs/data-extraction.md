# Step 1 – Data Extraction: TC-8005

## Pre-flight (Steps 0 – 0.8)

| Step | Result |
|------|--------|
| 0 – Validate Configuration | PASS. Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, and Security Configuration are all present. Product Lifecycle: version prefix `RHTPA`, Vulnerability issue type `10024`, component label pattern `pscomponent:`, VEX Justification field `customfield_12345`. Version Streams: 2.1.x (`rhtpa-release.0.3.z`), 2.2.x (`rhtpa-release.0.4.z`). Source Repositories: `rhtpa-backend`. |
| 0 – Optional config | Not configured: Upstream Affected Component field (Steps 4.3 and 7 skipped), PS Component field, Stream field, ProdSec email, ProdSec Jira account ID (no @mention), Embargo policy URL (Step 1.7 skipped). The Source Repositories table has no Deployment Context column, so it defaults to `upstream` and coordination guidance is left out (backward compatibility). |
| 0.3 – Matrix Staleness | WARNING. Matrix `Last-Updated: 2026-06-28T10:00:00Z` is 151 days old (today is 2026-11-26), well past the 14-day threshold. The matrix may be missing releases after 2.2.4. In interactive mode the engineer would choose Refresh, Proceed, or Stop. For this eval we proceed with the current matrix. |
| 0.6 – Fullsend Mode | Interactive mode (`FULLSEND_OUTPUT_DIR` not set). |
| 0.8 – Assign / Transition | Proposed (not executed): assign TC-8005 to the current user and move it from `New` to `Assigned`. |

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Jira key | TC-8005 | Issue |
| Issue type / Status | Vulnerability / New | Issue |
| CVE ID | CVE-2026-40215 | Label `CVE-2026-40215` + summary |
| Affected component | `pscomponent:org/rhtpa-server` (component `org/rhtpa-server`) | Labels (pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | openssl-libs (RPM system package) | Description |
| Affected version range | versions before 3.0.7-28.el9_4 (`< 3.0.7-28.el9_4`) | Description |
| Fixed version | 3.0.7-28.el9_4 | Description |
| CVSS / Severity | 7.1 (High) | Description |
| Vulnerability | Buffer over-read in `X509_verify_cert()`: the SAN extension length is not validated | Description |
| Upstream fix PR | None (no GitHub PR in remote links) | Remote links |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 (RHSA-2026:4021) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 | Remote links |
| Due date | 2026-08-15 (already **past due**, 103 days overdue) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) were parsed, so there is no need to stop.

## Stream Scope Resolution

- Suffix `[rhtpa-2.2]` → stream `2.2.x`. It matches the Version Streams row `2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z`.
- **Issue stream scope: 2.2.x.** Steps 3–8 are scoped to this stream. The 2.1.x stream is still analyzed in Step 2 so that cross-stream impact (Case A) can be detected.

## Ecosystem Detection

- Library `openssl-libs` is a system package in the container image, so the ecosystem is **RPM**.
- RPM appears in the 2.2.x Ecosystem Mappings: Repository `—` (Konflux release repo), Lock File `rpms.lock.yaml`, Check Command `git show <tag>:rpms.lock.yaml`, no Upstream Branch.
- Category: **System package**, which means **1 remediation task per stream** (Konflux release repo fix only).
- Investigation method: lock file (`rpms.lock.yaml`), plus optional SBOM verification.

## Deployment Context

- Component `org/rhtpa-server` is not listed in Source Repositories, and that table has no Deployment Context column. The context defaults to `upstream`, and coordination guidance is left out because the column is absent.

## Step 1.5 – External CVE Data Enrichment

- MITRE CVE API (`https://cveawg.mitre.org/api/cve/CVE-2026-40215`) was **not queried**, because the eval forbids external calls.
- OSV.dev (`https://api.osv.dev/v1/vulns/CVE-2026-40215`) was **not queried**, for the same reason.
- Result: "External CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced."
- **Fix threshold used in Step 2:** `openssl-libs < 3.0.7-28.el9_4` (fixed in `3.0.7-28.el9_4`), taken from the Jira description.

## Step 1.7 – Embargo Check

- No Embargo policy URL is configured, so this step is skipped silently. (CVSS 7.1 would otherwise meet the >= 7.0 threshold.)
