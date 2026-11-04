# Step 1 – Data Extraction: TC-8005

Mode: interactive (FULLSEND_OUTPUT_DIR not set). This is an eval run: Jira, git, cosign and WebFetch were not called. All values below come from the supplied mock inputs.

## Step 0 – Configuration check (claude-md-security-config.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| Upstream Affected Component field | not configured, so Step 4.3 is skipped |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column, defaults to `upstream`) |

Every required section is present. Validation passes.

## Parsed CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8005 | Issue |
| Issue type / Status | Vulnerability / New | Issue |
| CVE ID | CVE-2026-40215 | Label `CVE-2026-40215` and summary |
| Affected component | `pscomponent:org/rhtpa-server` (org/rhtpa-server) | Component label |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` -> stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | openssl-libs (RPM system package) | Description |
| Affected version range | < 3.0.7-28.el9_4 ("versions before 3.0.7-28.el9_4") | Description |
| Fixed version | 3.0.7-28.el9_4 | Description |
| CVSS / Severity | 7.1 (High) | Description |
| Vulnerability summary | Buffer over-read in X.509 certificate chain verification (`X509_verify_cert()`, SAN extension length not validated) | Description |
| Upstream fix PR | none (no GitHub PR remote link) | Remote links |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 (RHSA-2026:4021) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 | Remote links |
| Due date | 2026-08-15 | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | none | Comment history |

All critical fields (CVE ID, library, affected range) parsed successfully.

## Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to stream `2.2.x`, which matches the configured Version Stream `git.example.com/rhtpa/rhtpa-release.0.4.z`.
- **Issue stream scope: 2.2.x (scoped).** Steps 2–8 cover only the 2.2.x stream. 2.1.x is out of scope for this issue.
- Note for Step 3: the PSIRT-assigned Affects Versions value (`RHTPA 2.0.0`) does not match the 2.2.x stream scope. Correct it after version impact analysis (see version-impact.md).

## Ecosystem detection

| Item | Value |
|------|-------|
| Ecosystem | RPM (system package in container image) |
| Category | System package -> 1 remediation task per stream (Konflux release repo fix only) |
| Listed in 2.2.x Ecosystem Mappings? | Yes: `RPM \| — \| rpms.lock.yaml \| git show <tag>:rpms.lock.yaml \| —` |
| Investigation method | RPM lock file configured -> lock file + SBOM inspection |

## Deployment context

- Component `org/rhtpa-server` has no exact match in the Source Repositories table (only `rhtpa-backend`), so it defaults to **upstream**.

## Step 1.5 – External CVE Data Enrichment

The MITRE CVE API and OSV.dev were not queried because this eval forbids external calls. They are treated as unavailable:

> External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | < 3.0.7-28.el9_4 | 3.0.7-28.el9_4 |
| MITRE CVE API | unavailable (not queried) | — |
| OSV.dev | unavailable (not queried) | — |

**Fix threshold used in Step 2.3: 3.0.7-28.el9_4** (from the Jira description).

## Step 1.7 – Embargo Check

CVSS 7.1 meets the trigger threshold. However, no Embargo policy URL is configured, so this step is skipped silently.
