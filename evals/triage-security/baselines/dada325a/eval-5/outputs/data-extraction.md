# Step 1 – Data Extraction: TC-8005

Source: mock Jira issue `vuln-issue-rpm.md` (no live Jira call was made).

## Pre-flight (Steps 0 – 0.8)

- **Step 0 – Configuration**: Security Configuration present (Product Lifecycle, Version Streams, Source Repositories). Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`, Jira version prefix `RHTPA`, Vulnerability issue type ID `10024`, component label pattern `pscomponent:`, VEX Justification field `customfield_12345`. Optional fields not configured: Upstream Affected Component, PS Component, Stream, ProdSec contact/account ID, Embargo policy URL.
- **Step 0.3 – Matrix staleness**: both stream matrices carry `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-06, so they are **131 days old**, well past the 14-day threshold. **Warning:** the matrices may be missing releases made after 2.2.4 (2026-05-04). In an interactive run the engineer would choose Refresh / Proceed / Stop. For this eval, triage proceeds on the current matrix.
- **Step 0.6 – Mode**: interactive (`FULLSEND_OUTPUT_DIR` is not set).
- **Step 0.8 – Assign/transition**: proposed: assign TC-8005 to the current user and move it New → Assigned. Not executed (eval mode).

## Extracted CVE Data

| Field | Value |
|-------|-------|
| Issue key | TC-8005 |
| CVE ID | CVE-2026-40215 (from label and summary) |
| Summary | CVE-2026-40215 openssl-libs - Buffer over-read in X.509 certificate verification [rhtpa-2.2] |
| Status | New |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed, summary suffix) | `[rhtpa-2.2]`, which maps to stream **2.2.x** |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Ecosystem | **RPM** (system package; category: system package, so 1 remediation task per stream) |
| Affected version range | versions before 3.0.7-28.el9_4 (`< 3.0.7-28.el9_4`) |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Vulnerable code path | `X509_verify_cert()`, missing length validation on the Subject Alternative Name extension |
| Upstream fix PR | None (no GitHub PR remote link) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 (RHSA-2026:4021) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 (**already past** as of 2026-11-06) |
| Assignee | Unassigned |
| Existing comments | None |

## Stream Scope Resolution

- Suffix `[rhtpa-2.2]` maps to the configured Version Stream **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`, local path `/home/dev/repos/rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x (scoped).** Steps 3 and 4 are limited to 2.2.x versions. Other affected streams are handled through Case A (cross-stream impact).

## Ecosystem Detection

- openssl-libs is an RPM system package. Both streams list `RPM` in their Ecosystem Mappings with lock file `rpms.lock.yaml` and check command `git show <tag>:rpms.lock.yaml`. The ecosystem is supported.
- Investigation method: rpms.lock.yaml lock file inspection, plus the optional SBOM cross-check (Step 2.3.5).
- Remediation structure: **1 task per stream** (Konflux release repo fix). No upstream backport.

## Deployment Context

- The component `org/rhtpa-server` does not match any entry in the Source Repositories table. The table has no Deployment Context column anyway, so the context defaults to `upstream` (backward compatibility). Because the column is absent, the coordination guidance subsection is omitted from remediation tasks.

## Step 1.5 – External CVE Data Enrichment

- MITRE CVE API and OSV.dev were **not queried**, because this eval forbids external calls. Both are treated as unavailable.
- **Warning:** external CVE databases were unavailable, so this triage uses Jira description data only. Fix threshold confidence is reduced.
- Fix threshold used for Step 2: **3.0.7-28.el9_4** (Jira description).

## Step 1.7 – Embargo Check

- No Embargo policy URL is configured, so this step is skipped silently. CVSS 7.1 would otherwise have met the threshold of 7.0 or higher.
