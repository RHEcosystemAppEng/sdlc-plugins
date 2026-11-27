# Step 1 – Data Extraction: TC-8001

Source: simulated `jira.get_issue(TC-8001)` + `jira.get_issue_remote_links(TC-8001)` (from vuln-issue-standard.md). No live Jira calls were made.

## Pre-flight notes

- **Step 0 – Configuration**: Security Configuration present and complete (Product pages URL, Jira version prefix `RHTPA`, Vulnerability issue type ID `10024`, Component label pattern `pscomponent:`, 2 Version Streams, 1 Source Repository). Optional fields: VEX Justification field `customfield_12345`; ProdSec contact email `prodsec-team@example.com`; ProdSec Jira account ID `557058:prodsec-mock-account-id`. Not configured: Upstream Affected Component field (Steps 4.3 / 7 skipped), Embargo policy URL (Step 1.7 skipped). Source repos have no Deployment Context column -> default `upstream`.
- **Step 0.3 – Matrix staleness**: matrix `Last-Updated: 2026-06-28T10:00:00Z` is 152 days old (> 14-day threshold). WARNING: matrix may not reflect releases after 2026-06-28. Proceeding with the current matrix for this eval (in interactive use the engineer would be offered Refresh / Proceed / Stop).
- **Step 0.6 – Mode**: interactive (FULLSEND_OUTPUT_DIR absent); Jira writes are recorded to files instead of executed.
- **Step 0.8 – Assign/transition** (proposed, not executed): assign TC-8001 to the current triager and transition New -> Assigned.

## Extracted CVE data

| Field | Value |
|-------|-------|
| Issue key | TC-8001 |
| Issue type / Status | Vulnerability / New |
| CVE ID | CVE-2026-31812 (label + summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed, summary suffix) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) – remote DoS (panic via excessive QUIC streams) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 (already past as of 2026-11-27) |
| Reporter | psirt-analyst (account ID `557058:psirt-analyst-mock-id`) |
| Assignee | Unassigned |
| Existing comments | none |

## Derived context

| Item | Value |
|------|-------|
| Stream scope | `[rhtpa-2.2]` -> **2.2.x** (rhtpa-release.0.4.z) – scoped issue |
| Ecosystem | Cargo (Rust crate) – source dependency category (2 remediation tasks per stream) |
| Lock file / check command | `Cargo.lock` / `git show <tag>:Cargo.lock \| grep -A2 'name = "quinn-proto"'` |
| Affected repository | rhtpa-backend (`backend` in matrix) |
| Deployment context | upstream (default – no Deployment Context column) |

## Step 1.5 – External enrichment

MITRE / OSV queries not performed (external calls prohibited in this eval). Treated as unavailable: "External CVE databases unavailable – using Jira description data only. Fix threshold confidence is reduced." Fix threshold used: **0.11.14** (affected: < 0.11.14).

## Step 1.7 – Embargo check

Skipped: no Embargo policy URL configured (CVSS 7.5 would otherwise meet the threshold).
