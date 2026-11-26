# Step 1 – Data Extraction: TC-8005

## Pre-flight notes

- **Step 0 – Configuration**: Valid. Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) all present.
  - Jira version prefix: `RHTPA`
  - Vulnerability issue type ID: `10024`
  - Component label pattern: `pscomponent:`
  - VEX Justification custom field: `customfield_12345`
  - Optional fields not configured: Upstream Affected Component (Steps 4.3 and 7 skipped), PS Component, Stream field, ProdSec contact/account ID (no @mentions), Embargo policy URL (Step 1.7 skipped)
  - Source Repositories table has no Deployment Context column, so coordination guidance is left out of remediation tasks (backward-compatibility rule)
- **Step 0.3 – Matrix staleness**: the matrix says `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-23, so it is **148 days old**, past the 14-day threshold.
  > Security matrix for stream **2.2.x** (and 2.1.x) was last updated on 2026-06-28 (148 days ago). The matrix may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.
  For this eval: **Proceed anyway** with the current matrix. Any 2.2.x release after 2.2.4 (2026-05-04) is not covered.
- **Step 0.6 – Mode**: Interactive (`FULLSEND_OUTPUT_DIR` not set). Steps 0.7 and 0.8 are simulated: assigning TC-8005 to the current user and moving it New → Assigned would happen after confirmation. Nothing was written to Jira in this eval.

## Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8005 | Issue |
| Status | New (full triage path) | Issue status |
| CVE ID | CVE-2026-40215 | Label `CVE-2026-40215` and summary |
| Affected component | `pscomponent:org/rhtpa-server` (component `org/rhtpa-server`) | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Issue stream scope | **2.2.x** (maps to `git.example.com/rhtpa/rhtpa-release.0.4.z`) | Suffix matched to Version Streams table |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | openssl-libs | Description |
| Ecosystem | **RPM** (system package; category: 1 remediation task per stream, Konflux release repo fix only) | Library name plus the Ecosystem Mappings `RPM` row (`rpms.lock.yaml`) |
| Affected version range | versions before 3.0.7-28.el9_4 (`< 3.0.7-28.el9_4`) | Description |
| Fixed version | 3.0.7-28.el9_4 | Description |
| CVSS / Severity | 7.1 (High) | Description |
| Vulnerability detail | Buffer over-read in `X509_verify_cert()`: the SAN extension length field is not validated | Description |
| Upstream fix PR | None (no GitHub PR remote link) | Remote links |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 (RHSA-2026:4021) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 | Remote links |
| Due date | 2026-08-15 (**already past** as of 2026-11-23) | Issue `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Issue comments |
| Deployment context | `upstream` (default: the affected component is not in the Source Repositories table, which also has no Deployment Context column) | Step 1 lookup |

All critical fields (CVE ID, library, affected range) parsed. Nothing is missing.

## Step 1.5 – External CVE data enrichment

Not run in this eval (no external calls allowed). Following the "both APIs unavailable" rule:

> External CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced.

**Fix threshold used for Step 2:** `openssl-libs < 3.0.7-28.el9_4` (from the Jira description, matching the RHSA-2026:4021 reference).

## Step 1.7 – Embargo check

Skipped silently: no Embargo policy URL is configured in Security Configuration. CVSS 7.1 would otherwise have triggered the gate.
