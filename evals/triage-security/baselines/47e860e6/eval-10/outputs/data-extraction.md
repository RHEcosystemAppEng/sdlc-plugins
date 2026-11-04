# Step 1 – Data Extraction: TC-8020

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Eval run, so no Jira, git, or WebFetch calls were made. All data comes from the supplied mock files.

## Step 0 – Configuration validation (claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component / PS Component / Stream fields | Not configured in Security Configuration. The issue carries customfield_10632 / 10669 / 10832, but the config does not declare them, so Steps 4.3 and 7 are skipped. |
| ProdSec contact / account ID | Not configured, so no ProdSec @mentions |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend). There is no Deployment Context column, so the context defaults to `upstream` and the Coordination Guidance subsection is omitted (backward compatibility). |

All required sections are present, so the run continues.

## Step 0.3 – Matrix staleness

The matrix mock has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-04, so the matrix is about 129 days old, which is past the 14-day threshold. **Staleness warning:** the matrix may be missing recent releases. The engineer would choose Refresh, Proceed, or Stop. For this eval, the choice is **Proceed anyway**.

## Step 0.8 – Assign and transition

The status is New. Proposed actions: assign TC-8020 to the current user, then move it to the "Assigned" transition found dynamically through `get_transitions`. Both need confirmation and were not executed.

## Extracted fields

| Field | Value |
|---|---|
| Issue key | TC-8020 |
| CVE ID | CVE-2026-55123 (from the label and summary) |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.2] |
| Status | New |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed, suffix) | `[rhtpa-2.2]` |
| Affects Versions (Jira) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Ecosystem | Cargo (Rust crate). This is a source dependency, so 2 tasks per stream. |
| Affected version range | < 1.42.0 (versions before 1.42.0) |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp (also RUSTSEC-2026-0088) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 (already past) |
| Assignee | Unassigned |
| Existing links | none |
| Existing comments | none |
| Upstream Affected Component (customfield_10632) | tokio |
| Stream (customfield_10832) | rhtpa-2.2 |

## Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to the configured Version Stream **2.2.x** (rhtpa-release.0.4.z).
- The issue is **scoped** to 2.2.x. Step 3 changes only 2.2.x versions, and Case A cross-stream handling applies to the other streams.

## Deployment context

rhtpa-backend has no Deployment Context column, so it defaults to `upstream`. Because the column is absent, the coordination guidance subsection is omitted from the task descriptions.

## Step 1.5 – External enrichment

MITRE and OSV were not queried because external calls are disabled in this eval. The fix threshold comes from the Jira description only (< 1.42.0, fixed in 1.42.0). It matches the task statement (threshold 1.42.0) and RUSTSEC-2026-0088. Note: confidence is reduced because the external databases were not consulted.

## Step 1.7 – Embargo check

Skipped because no Embargo policy URL is configured. CVSS 8.1 would otherwise have triggered the gate.
