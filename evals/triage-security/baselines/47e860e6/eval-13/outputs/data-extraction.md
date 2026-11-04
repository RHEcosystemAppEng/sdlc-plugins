# TC-8001 — Step 1: Data Extraction

Source: `vuln-issue-standard.md` (simulated `jira.get_issue` + `jira.get_issue_remote_links`).
No Jira MCP calls were made; all values below come from the mock issue file.

## Pre-steps (summary)

| Step | Result |
|------|--------|
| 0 – Validate configuration | PASS. Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) are all present. |
| 0 – Extracted config | Jira version prefix `RHTPA`; Vulnerability issue type ID `10024`; Component label pattern `pscomponent:`; VEX Justification field `customfield_12345`; Product pages URL `https://access.example.com/product-life-cycle/rhtpa`. Not configured: Upstream Affected Component field, PS Component field, Stream field, ProdSec contact/account ID, Embargo policy URL. |
| 0.3 – Matrix staleness | WARNING: neither stream's security-matrix.md has a `Last-Updated` timestamp. The issue file has `Last-Updated: 2026-06-28T10:00:00Z`, which is 129 days before today (2026-11-04), well past the 14-day threshold. In a live run I would offer Refresh / Proceed / Stop. For this eval I proceed with the matrix as provided. |
| 0.6 – Fullsend mode | `FULLSEND_OUTPUT_DIR` not set, so this is interactive mode. |
| 0.8 – Assign / transition | Would assign TC-8001 to the current user and move it New -> Assigned (transition discovered with `get_transitions`). Not executed. |
| Status-aware handling | Status is `New`, so full triage runs. |

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| CVE ID | **CVE-2026-31812** | Label `CVE-2026-31812` + summary |
| Affected component | `pscomponent:org/rhtpa-server` -> `org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` -> stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | **RHTPA 2.0.0** (wrong: no 2.0.x stream is configured; see Step 3) | `versions` field |
| Vulnerable library | **quinn-proto** (Rust crate) | Description |
| Affected version range | **< 0.11.14** ("versions before 0.11.14") | Description |
| Fixed version | **0.11.14** | Description |
| CVSS / severity | 7.5 (High), DoS (panic on excessive stream count in STREAMS frame) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / References |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (**already past** as of 2026-11-04) | `duedate` |
| Assignee | Unassigned | Issue |
| Status | New | Issue |
| Existing comments | None | Comment history |

## Stream Scope Resolution

- Suffix `[rhtpa-2.2]` maps to configured Version Stream **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x (scoped).** The 2.1.x stream is out of scope for this issue, so Case A (cross-stream) applies if 2.1.x is affected.

## Ecosystem Detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. Both streams list it in Ecosystem Mappings (repo `backend`, lock file `Cargo.lock`).
- Category: **Source dependency**, so each stream gets 2 remediation tasks: (upstream backport or dependency bump) + downstream propagation.

## Deployment Context

- Affected repository: rhtpa-backend (`backend` in Ecosystem Mappings).
- The Source Repositories table has **no Deployment Context column**. For backward compatibility the context defaults to `upstream`, and **the Coordination Guidance subsection is omitted** from task descriptions.

## Step 1.5 – External CVE Data Enrichment

- MITRE (`https://cveawg.mitre.org/api/cve/CVE-2026-31812`) and OSV.dev (`https://api.osv.dev/v1/vulns/CVE-2026-31812`) were **not queried** because external calls are not allowed in this eval.
- Warning: External CVE databases unavailable, so only the Jira description data is used. Fix threshold confidence is reduced.
- Fix threshold used for Step 2: **quinn-proto < 0.11.14 is affected; 0.11.14 or later is fixed.**

## Step 1.7 – Embargo Check

- No Embargo policy URL is configured, so this step is skipped silently. (CVSS 7.5 would otherwise meet the >= 7.0 threshold.)
