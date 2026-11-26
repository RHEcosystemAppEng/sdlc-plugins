# TC-8005 — Step 1: Data Extraction

Mode: interactive (FULLSEND_OUTPUT_DIR not set). Jira was not called for this eval; the
issue data comes from the mock issue file (`vuln-issue-rpm.md`).

## Step 0: Configuration check

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| Upstream Affected Component field | not configured, so Step 4.3 is skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (no Deployment Context column, defaults to `upstream`) |

Result: all required Security Configuration sections are present. Continue.

## Parsed CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8005 | Issue |
| Issue status | New (full triage path) | Issue status |
| CVE ID | CVE-2026-40215 | Label `CVE-2026-40215` and summary |
| Affected component | `pscomponent:org/rhtpa-server` (org/rhtpa-server) | Component label |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | openssl-libs (RPM) | Description |
| Affected version range | versions before 3.0.7-28.el9_4 (`< 3.0.7-28.el9_4`) | Description |
| Fixed version | 3.0.7-28.el9_4 | Description |
| CVSS / severity | 7.1 (High) | Description |
| Vulnerability summary | Buffer over-read in `X509_verify_cert()` while parsing the SAN extension length (X.509 chain verification) | Description |
| Upstream fix PR | none (no GitHub PR remote link) | Remote links |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 (RHSA-2026:4021) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 | Remote links |
| Due date | 2026-08-15 | `duedate` |
| Assignee | Unassigned (Step 0.8 would assign the current user and move New to Assigned; not run for this eval) | Issue |
| Existing comments | none | Comment history |

All critical fields (CVE ID, library, affected range) were parsed.

## Stream scope resolution

| Item | Value |
|------|-------|
| Summary suffix | `[rhtpa-2.2]` |
| Parsed stream | 2.2.x |
| Matching configured stream | 2.2.x, git.example.com/rhtpa/rhtpa-release.0.4.z |
| Issue stream scope | **Scoped to 2.2.x.** Steps 2 to 8 cover only the 2.2.x stream. 2.1.x is outside this issue's scope. |

Note: the PSIRT Affects Versions value (RHTPA 2.0.0) does not belong to the scoped
2.2.x stream. No 2.0.x stream is configured. Step 3 should correct this field.

## Ecosystem detection

| Item | Value |
|------|-------|
| Ecosystem | RPM (system package in the container image) |
| Category | System package, so 1 remediation task per affected stream (Konflux release repo fix only) |
| Lock file configured (2.2.x Ecosystem Mappings) | `rpms.lock.yaml`, checked with `git show <tag>:rpms.lock.yaml` |
| Investigation path | Lock file plus SBOM inspection (cosign is available) |
| Deployment context | org/rhtpa-server is not listed in Source Repositories, so it defaults to `upstream` |

## Step 1.5: External enrichment

The MITRE CVE API and OSV.dev were not queried, because this eval allows no external
calls. The fix threshold falls back to the Jira description: **3.0.7-28.el9_4**.

## Step 1.7: Embargo check

Skipped. No Embargo policy URL is configured.
