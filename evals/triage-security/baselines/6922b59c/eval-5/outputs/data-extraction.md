# Step 1 -- Data Extraction: TC-8005

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable package | openssl-libs |
| Ecosystem | RPM (system package) |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Due date | 2026-08-15 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| Upstream fix PR | (none in remote links) |
| Existing comments | (none) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local path: `/home/dev/repos/rhtpa-release.0.4.z`

## Ecosystem Detection

- Ecosystem: **RPM** (system package -- openssl-libs is an OS-level package)
- Lock file: `rpms.lock.yaml` (configured in Ecosystem Mappings)
- Check command: `git show <tag>:rpms.lock.yaml`
- Upstream Branch: -- (not applicable for RPM)
- Remediation tasks per stream: **1** (Konflux release repo fix only)

## Vulnerability Details

A buffer over-read vulnerability in openssl-libs during X.509 certificate chain
verification. The `X509_verify_cert()` code path does not properly validate the
length field of a Subject Alternative Name extension, allowing a remote attacker
to craft a malformed certificate that triggers an out-of-bounds read, potentially
leaking sensitive memory contents or causing a crash.
