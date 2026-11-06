# Step 1 – Data Extraction: TC-8020

## Step 0 – Configuration validation

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| ProdSec Jira account ID | not configured (@mentions skipped) |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend), no Deployment Context column -> default `upstream`, coordination guidance omitted (backward compatibility) |

All required sections (Repository Registry, Jira Configuration, Code Intelligence, Security Configuration) are present. Proceeding.

Step 0.3 (matrix staleness): the matrix is marked `Last-Updated: 2026-06-28T10:00:00Z`, which is more than 14 days old as of 2026-11-06. In an interactive run the engineer would be offered Refresh / Proceed / Stop. For this eval the run proceeds with the current matrix.

Step 0.6: `FULLSEND_OUTPUT_DIR` is absent, so this runs in interactive mode, simulated here by writing files.
Step 0.8 (simulated): assign TC-8020 to the current user and transition it from New to Assigned.

## Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8020 | Issue |
| Status | New (full triage path) | Issue |
| CVE ID | CVE-2026-55123 | Label + summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label / customfield_10669 |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira) | RHTPA 2.2.0, RHTPA 2.2.1 | `versions` field |
| Vulnerable library | tokio | Description / customfield_10632 |
| Ecosystem | Cargo (source dependency, so 2 tasks per stream) | Library + Ecosystem Mappings |
| Affected version range | < 1.42.0 | Description |
| Fixed version | 1.42.0 | Description |
| CVSS | 8.1 (High) | Description |
| Vulnerability | Use-after-free when a spawned task is aborted while holding a borrowed reference | Description |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 | Remote link |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp | Remote link |
| Additional advisory | https://rustsec.org/advisories/RUSTSEC-2026-0088.html | Description references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 | Remote link |
| Due date | 2026-08-15 | `duedate` |
| Upstream Affected Component (customfield_10632) | tokio | Custom field |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-server | Custom field |
| Stream (customfield_10832) | rhtpa-2.2 | Custom field |
| Existing links | none | Issue links |
| Existing comments | none | Comments |

## Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to configured stream **2.2.x** (Konflux repo `rhtpa-release.0.4.z`).
- The issue is **scoped** to 2.2.x, so Case A (cross-stream impact) applies if other streams are affected.

## Deployment context

- Affected repo: rhtpa-backend (Cargo `backend` repo per Ecosystem Mappings). The Deployment Context column is absent, so context defaults to `upstream`. The Coordination Guidance subsection is omitted per the backward-compatibility rule.

## Step 1.5 – External CVE enrichment

- MITRE (`https://cveawg.mitre.org/api/cve/CVE-2026-55123`) and OSV (`https://api.osv.dev/v1/vulns/CVE-2026-55123`) were **not queried** because this eval forbids external calls.
- Result: "External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced."
- Fix threshold used: **tokio < 1.42.0 (fixed in 1.42.0)**.

## Step 1.7 – Embargo check

- CVSS 8.1 meets the threshold (>= 7.0), but no Embargo policy URL is configured, so this step is skipped silently.
