# Step 1 – Data Extraction: TC-8005

Source: mock Jira issue `vuln-issue-rpm.md` (simulated `jira.get_issue` + `jira.get_issue_remote_links`; no Jira MCP calls were made).

## Preliminary steps (simulated)

| Step | Result |
|------|--------|
| 0 – Validate Configuration | PASS. `claude-md-security-config.md` has Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories). Jira version prefix `RHTPA`; Vulnerability issue type ID `10024`; Component label pattern `pscomponent:`; VEX Justification field `customfield_12345`. Not configured (optional): Upstream Affected Component, PS Component, Stream field, ProdSec contact/account, Embargo policy URL. |
| 0.3 – Matrix Staleness | WARNING. The security matrix data for stream 2.2.x (and 2.1.x) has no `<!-- Last-Updated -->` timestamp. Proceeding without blocking; consider re-running `/setup` to populate the timestamp. |
| 0.5 – Jira Access | Simulated (eval: no external calls). |
| 0.6 – Fullsend Mode | `FULLSEND_OUTPUT_DIR` absent -> interactive mode (outputs written to files per eval instructions instead of Jira). |
| 0.8 – Assign / Transition | Would assign TC-8005 (currently Unassigned) to the current user and transition New -> Assigned. Not executed (eval). |
| Status-aware handling | Status `New` -> full triage path. |

## Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8005 | Issue |
| CVE ID | CVE-2026-40215 | Label `CVE-2026-40215` + summary |
| Summary | CVE-2026-40215 openssl-libs - Buffer over-read in X.509 certificate verification [rhtpa-2.2] | Issue summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` -> RHTPA 2.2 | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | openssl-libs | Description |
| Affected version range | versions before 3.0.7-28.el9_4 (`< 3.0.7-28.el9_4`) | Description |
| Fixed version | 3.0.7-28.el9_4 | Description |
| CVSS / Severity | 7.1 (High) | Description |
| Vulnerable code path | `X509_verify_cert()` – SAN extension length field not validated (out-of-bounds read) | Description |
| Upstream fix PR | None (no GitHub PR remote link) | Remote links |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 (RHSA-2026:4021) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 | Remote links |
| Due date | 2026-08-15 | `duedate` |
| Assignee | Unassigned | Issue |
| Status | New | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) parsed successfully.

## Stream scope resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x** (Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z`, local path `/home/dev/repos/rhtpa-release.0.4.z`) |
| Issue stream scope | **Scoped – 2.2.x only** (Steps 3–8 scoped to this stream; other streams handled via Case A cross-stream logic) |

## Ecosystem detection

| Item | Value |
|------|-------|
| Ecosystem | **RPM** (system package in container image) |
| In stream Ecosystem Mappings? | Yes – RPM row, lock file `rpms.lock.yaml`, check command `git show <tag>:rpms.lock.yaml`, Repository `—` (Konflux release repo), Upstream Branch `—` |
| Category | System package |
| Investigation method | Lock file (`rpms.lock.yaml`) + optional SBOM verification (cosign available: `which cosign` -> `/usr/bin/cosign`) |
| Remediation tasks per stream | 1 – Konflux release repo fix |

## Deployment context

Component `org/rhtpa-server` does not match an entry in the Source Repositories table (only `rhtpa-backend` is listed) -> default deployment context: **upstream**.

## Step 1.5 – External CVE Data Enrichment (simulated)

| Source | Affected range | Fixed version | Status |
|--------|----------------|---------------|--------|
| Jira description | < 3.0.7-28.el9_4 | 3.0.7-28.el9_4 | Parsed |
| MITRE CVE API | — | — | Not queried (eval forbids external calls) |
| OSV.dev | — | — | Not queried (eval forbids external calls) |

> "External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced."

**Fix threshold used for Step 2.3:** `openssl-libs < 3.0.7-28.el9_4` (fixed in `3.0.7-28.el9_4`).

## Step 1.7 – Embargo Check

CVSS 7.1 meets the Important/Critical threshold, but no Embargo policy URL is configured in Security Configuration -> step skipped.
