# Step 1 – Data Extraction: TC-8005

## Pre-flight (Steps 0–0.8)

- **Step 0.6 Mode**: interactive. `FULLSEND_OUTPUT_DIR` is not set, so this is not a Fullsend sandbox run. This eval simulates the run: no Jira, git, or cosign calls were made.
- **Step 0 Configuration**: `claude-md-security-config.md` passes validation. It has Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, and Security Configuration. Security Configuration sets prefix `RHTPA`, Vulnerability type `10024`, label pattern `pscomponent:`, VEX field `customfield_12345`, 2 Version Streams and 1 Source Repository.
  - Not configured: Embargo policy URL, Upstream Affected Component / PS Component / Stream custom fields, ProdSec contact/account ID, Deployment Context column.
- **Step 0.3 Matrix staleness**: the matrix has `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. That is **129 days old**, well past the 14-day threshold. In an interactive run, the skill would offer "Refresh now / Proceed anyway / Stop". This eval proceeds with the current matrix and records the warning.
- **Step 0.8 Assign/transition**: the skill would propose assigning TC-8005 to the current user and moving it New → Assigned. It looks up the transition at runtime and does not hardcode an ID. This eval made no Jira call.

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8005 | Issue |
| CVE ID | CVE-2026-40215 | Label `CVE-2026-40215` + summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | openssl-libs (RPM system package) | Description |
| Affected version range | versions before 3.0.7-28.el9_4 (`< 3.0.7-28.el9_4`) | Description |
| Fixed version | 3.0.7-28.el9_4 | Description |
| CVSS / Severity | 7.1 (High) | Description |
| Vulnerability | Buffer over-read in `X509_verify_cert()`: SAN extension length is not validated | Description |
| Upstream fix PR | None (no GitHub PR remote link) | Remote links |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 | Remote links |
| Due date | 2026-08-15 (**already past**: today is 2026-11-04) | `duedate` |
| Status | New | Issue |
| Assignee | Unassigned | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) were parsed successfully.

## Stream Scope Resolution

- Suffix `[rhtpa-2.2]` maps to stream **2.2.x**. That stream's Konflux release repo is `git.example.com/rhtpa/rhtpa-release.0.4.z`, local path `/home/dev/repos/rhtpa-release.0.4.z`.
- **Issue stream scope: 2.2.x (scoped).** Steps 3, 4 and 8 are limited to 2.2.x. Other streams are handled through Case A (cross-stream impact).

## Ecosystem Detection

- `openssl-libs` is a system package inside a container image, so the ecosystem is **RPM**.
- The 2.2.x Ecosystem Mappings table has an RPM row: Lock File `rpms.lock.yaml`, Check Command `git show <tag>:rpms.lock.yaml`, Repository `—`, Upstream Branch `—`.
- **Category: System package.** That means 1 remediation task per stream, a Konflux release repo fix, with no upstream backport.
- Investigation method: lock file (`rpms.lock.yaml`), with optional SBOM cross-check (Step 2.3.5).

## Deployment Context

- The component `org/rhtpa-server` is built in the Konflux release repo. The affected source repo is not uniquely identifiable from the label. The Source Repositories table has no Deployment Context column.
- Context therefore **defaults to `upstream`** for backward compatibility. Because the column is absent, the Coordination Guidance subsection is **omitted** from the remediation task, per `remediation-templates.md`.

## Step 1.5 – External CVE Data Enrichment

- MITRE CVE API (`https://cveawg.mitre.org/api/cve/CVE-2026-40215`) and OSV.dev (`https://api.osv.dev/v1/vulns/CVE-2026-40215`) were **not queried**, because this eval forbids external calls.
- Both sources are treated as unavailable: "⚠ External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced."
- **Fix threshold used in Step 2.3: `3.0.7-28.el9_4`**, taken from the Jira description and consistent with RHSA-2026:4021.

## Step 1.7 – Embargo Check

- CVSS 7.1 meets the threshold (≥ 7.0). However, **no Embargo policy URL is configured**, so this step is skipped silently.
