# Step 1 – Data Extraction: TC-8005

Source: mock Jira issue `vuln-issue-rpm.md` (no live Jira call made).

## Parsed CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8005 | Issue |
| Issue type / status | Vulnerability / New | Issue |
| CVE ID | CVE-2026-40215 | Label `CVE-2026-40215` + summary text (consistent) |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching Component label pattern `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | openssl-libs | Description |
| Affected version range | < 3.0.7-28.el9_4 ("versions before 3.0.7-28.el9_4") | Description |
| Fixed version | 3.0.7-28.el9_4 | Description |
| CVSS | 7.1 (High) | Description |
| Vulnerability summary | Buffer over-read in `X509_verify_cert()` – SAN extension length field not validated | Description |
| Upstream fix PR | None (no GitHub PR remote links) | Remote links |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 (RHSA-2026:4021) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 | Remote links |
| Due date | 2026-08-15 (already past as of 2026-11-20) | Issue `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Comment history |

All critical fields (CVE ID, library, affected range) were parsed successfully.

## Stream scope resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Parsed stream | 2.2.x |
| Matched Version Stream | 2.2.x → `git.example.com/rhtpa/rhtpa-release.0.4.z` (local: `/home/dev/repos/rhtpa-release.0.4.z`) |
| Issue stream scope | **Scoped – 2.2.x only** (2.1.x stream excluded from this issue) |

## Ecosystem detection

| Item | Value |
|------|-------|
| Ecosystem | **RPM** (system package in container image) |
| Category | System package |
| Remediation tasks per stream | 1 – Konflux release repo fix only |
| Lock file (2.2.x Ecosystem Mappings) | `rpms.lock.yaml` (configured) |
| Check command | `git show <tag>:rpms.lock.yaml` (grep `openssl-libs`) |
| Investigation method | Lock file + SBOM inspection (cosign available) |
| Upstream branch | — (none for RPM; Step 2.5 upstream fix check not applicable) |

## Deployment context

The affected component `org/rhtpa-server` is not listed in the Source Repositories
table (only `rhtpa-backend`), and the table has no deployment-context column →
defaulting to **upstream**. Not material for an RPM fix, which is applied in the
Konflux release repo.

## Observations

- **Affects Versions mismatch**: PSIRT set `RHTPA 2.0.0`, but the issue is scoped to
  `[rhtpa-2.2]` and no 2.0.x stream is configured. Step 2 shows that 2.2.0, 2.2.1 and
  2.2.2 are the affected versions; the field needs correcting in Step 3.
- **Step 1.5 (external enrichment)**: no MITRE/OSV calls were made because external
  calls are not allowed in this eval. The Jira description threshold
  (`< 3.0.7-28.el9_4`) is used.
  ⚠ External CVE databases not queried – using Jira description data only. Fix
  threshold confidence is reduced.
- **Step 1.7 (embargo check)**: CVSS 7.1 meets the threshold, but no Embargo policy URL
  is configured in Security Configuration → step skipped silently.
