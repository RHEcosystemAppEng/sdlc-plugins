# Step 1 – Data Extraction: TC-8005

Source: mock Jira issue (`vuln-issue-rpm.md`). No live Jira calls were made in this eval.

## Pre-checks (Steps 0 – 0.8)

| Check | Result |
|-------|--------|
| Step 0 – Configuration | PASS. Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) are all present |
| Jira version prefix | `RHTPA` |
| Vulnerability issue type ID | `10024` |
| Component label pattern | `pscomponent:` |
| VEX Justification field | `customfield_12345` (configured) |
| Optional fields not configured | Upstream Affected Component, PS Component, Stream field, ProdSec contact/account ID, Embargo policy URL |
| Step 0.3 – Matrix staleness | WARNING. Matrix `Last-Updated: 2026-06-28T10:00:00Z` is 131 days old (today is 2026-11-06), past the 14-day threshold. In an interactive run the engineer would choose Refresh / Proceed / Stop. This eval continues with the current matrix |
| Step 0.6 – Mode | Interactive (`FULLSEND_OUTPUT_DIR` not set) |
| Step 0.8 – Assign/transition | Status is `New`, so the skill would assign the issue to the current user and move it to Assigned. Not executed (no Jira calls) |

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8005 | Issue |
| CVE ID | CVE-2026-40215 | Label `CVE-2026-40215` and summary |
| Summary | CVE-2026-40215 openssl-libs - Buffer over-read in X.509 certificate verification [rhtpa-2.2] | Issue summary |
| Status | New | Issue |
| Affected component | `org/rhtpa-server` | Label `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `rhtpa-2.2` | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | openssl-libs | Description |
| Ecosystem | RPM (system package) | Library name plus container component. Listed in the stream's Ecosystem Mappings with lock file `rpms.lock.yaml` |
| Affected version range | versions before 3.0.7-28.el9_4 (`< 3.0.7-28.el9_4`) | Description |
| Fixed version | 3.0.7-28.el9_4 | Description |
| CVSS | 7.1 (High) | Description |
| Vulnerable code path | `X509_verify_cert()`: the SAN extension length field is not validated | Description |
| Upstream fix PR | None (no GitHub PR remote link) | Remote links |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 (RHSA-2026:4021) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 | Remote links |
| Due date | 2026-08-15 (already past as of 2026-11-06) | Issue `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Issue |

All critical fields (CVE ID, library, affected range) were parsed.

## Stream Scope Resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Mapped stream | **2.2.x**, which matches the configured Version Stream `git.example.com/rhtpa/rhtpa-release.0.4.z` (local path `/home/dev/repos/rhtpa-release.0.4.z`) |
| Issue stream scope | **Scoped to 2.2.x**. Steps 3–8 apply to this stream only. Other streams get cross-stream handling (Case A) |

## Ecosystem Classification

| Category | Ecosystem | Remediation tasks per stream |
|----------|-----------|------------------------------|
| System package | RPM | 1: Konflux release repo fix |

Investigation method: lock file (`rpms.lock.yaml`, configured in the 2.2.x Ecosystem Mappings) plus optional SBOM verification (cosign is available at `/usr/bin/cosign`).

## Deployment Context

The `org/rhtpa-server` component is a container image built in the Konflux release repo. The RPM ecosystem row has no source repository (`—`). Source Repositories has no Deployment Context column, so the context defaults to `upstream`.

## Step 1.5 – External CVE Data Enrichment

MITRE CVE API and OSV.dev were not queried, because this eval does not allow external calls. Both sources are treated as unavailable:

> "External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced."

**Fix threshold used for Step 2:** `< 3.0.7-28.el9_4` (from the Jira description).

## Step 1.7 – Embargo Check

Skipped. No Embargo policy URL is configured in Security Configuration. CVSS 7.1 would otherwise meet the threshold.
