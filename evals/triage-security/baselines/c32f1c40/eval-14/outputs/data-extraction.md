# Step 0.8 -- Early Assignment

Before data extraction, the following actions are proposed:

1. **Assign TC-8005 to current user** -- ensures visibility into who is actively triaging.
2. **Transition TC-8005 to Assigned status** -- the issue is currently in New status, so the Assigned transition would be executed after discovering available transitions via `jira.get_transitions(TC-8005)`.

These are proposed actions; no Jira operations were performed.

---

# Step 1 -- Data Extraction

## Parsed CVE Data Table

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| Upstream fix PR | N/A |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| CVSS | 7.1 (High) |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable package is **openssl-libs**, which is a system-level RPM package (not a Cargo crate or npm package). Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is **RPM**.

The RPM ecosystem is classified as a **system package** ecosystem. Per the ecosystem classification table:
- System package ecosystems produce **1 remediation task** per stream (Konflux release repo fix only).
- No upstream backport task is needed -- the fix happens directly in the Konflux release repo.

## Deployment Context Lookup

The Source Repositories table in Security Configuration does not include a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`. The Coordination Guidance subsection will be omitted from remediation task descriptions.
