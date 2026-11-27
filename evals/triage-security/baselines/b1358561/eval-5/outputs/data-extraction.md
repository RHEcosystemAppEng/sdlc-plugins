# Step 1 – Data Extraction: TC-8005

Mode: interactive (`FULLSEND_OUTPUT_DIR` absent). Source: mock issue data (`vuln-issue-rpm.md`); no Jira calls were made.

## Step 0 – Configuration validation

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | not configured (Steps 4.3 and 7 skipped) |
| ProdSec Jira account ID | not configured (no @mention) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream` and coordination guidance is left out) |

All required sections are present, so validation passed.

## Step 0.3 – Matrix staleness check

`<!-- Last-Updated: 2026-06-28T10:00:00Z -->` is 152 days old as of 2026-11-27, which is more than the 14-day threshold.

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28 (152 days ago). The matrix may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

For this eval: **Proceed anyway** (no refresh possible offline). Releases after 2.2.4 (2026-05-04) may be missing from the matrix.

## Extracted CVE data

| Field | Value |
|-------|-------|
| Issue key | TC-8005 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-40215 (label + summary) |
| Summary | CVE-2026-40215 openssl-libs - Buffer over-read in X.509 certificate verification [rhtpa-2.2] |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed, summary suffix) | `[rhtpa-2.2]` |
| Issue stream scope | **2.2.x** (rhtpa-release.0.4.z). The suffix matches a configured stream |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs (RPM: openssl) |
| Ecosystem | **RPM** (system package, so 1 remediation task per stream) |
| Affected version range | versions before 3.0.7-28.el9_4 (`< 3.0.7-28.el9_4`) |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS / severity | 7.1 (High) |
| Vulnerable code path | `X509_verify_cert()`: missing SAN extension length bounds check |
| Upstream fix PR | none (no GitHub PR remote link) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 (**overdue** as of 2026-11-27) |
| Assignee | Unassigned |
| Existing comments | none |
| Deployment context | `upstream` (default; no Deployment Context column) |

## Step 0.8 – Assign and transition (proposed, not executed)

- Assign TC-8005 to the current user.
- Transition New → Assigned (transition ID discovered dynamically via `get_transitions`).

## Step 1.5 – External CVE data enrichment

MITRE CVE API and OSV.dev were not queried (no external calls in this eval).

> ⚠ External CVE databases unavailable: using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used for Step 2: **openssl-libs < 3.0.7-28.el9_4** (from the Jira description).

## Step 1.7 – Embargo check

No Embargo policy URL is configured, so the step was skipped silently (CVSS 7.1 would otherwise trigger the gate).
