# Step 1 – Data Extraction: TC-8001 (re-run)

## Execution context

- **Mode**: Interactive (Step 0.6: `FULLSEND_OUTPUT_DIR` is not set). The eval runs as a simulation: no Jira MCP, `git show`, or WebFetch calls are made. The mock files stand in for the tool output.
- **Step 0 – Configuration**: valid. Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) are all present in `claude-md-security-config.md`.
  - Jira version prefix: `RHTPA`
  - Vulnerability issue type ID: `10024`
  - Component label pattern: `pscomponent:`
  - VEX Justification field: `customfield_12345`
  - Upstream Affected Component / PS Component / Stream custom fields: not declared in Security Configuration. The issue carries `customfield_10632`, `customfield_10669`, and `customfield_10832`, but the config does not declare them, so Steps 4.3, 7, and 7.5.3 (config-gated) are skipped.
  - ProdSec account ID and embargo policy URL are not configured, so there are no @mentions and Step 1.7 is skipped.
- **Step 0.3 – Matrix staleness**: `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Measured against the session date (2026-11-23), the matrix is 148 days old, which is past the 14-day threshold. In a live run this would show the Refresh now / Proceed anyway / Stop prompt. In this eval the matrix is the fixed fixture, so the run proceeds with it.
- **Status-aware handling**: the issue is **In Progress**. The skill warns: "This issue is already in `In Progress`. It may be actively worked on." It then asks whether to proceed or skip. This eval assumes the engineer chose **Proceed** so that version impact can be re-verified.

## Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8001 | Issue |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]`, which maps to stream **2.2.x** (`rhtpa-release.0.4.z`) | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 | `versions` field (already corrected by the prior run) |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Ecosystem | Cargo (source dependency, so 2 remediation tasks per stream) | Library name + Ecosystem Mappings |
| Lock file / repo | `Cargo.lock` in `backend` (upstream branch `release/0.4.z`) | security-matrix Ecosystem Mappings |
| Deployment context | `upstream` (default, because the Source Repositories table has no Deployment Context column) | Step 0 mapping |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | `duedate` |
| Status | In Progress | Issue |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, **ai-cve-triaged** | Issue |
| Assignee | engineer-a@example.com | Issue |
| Upstream Affected Component (cf 10632) | quinn-proto | Custom field |
| PS Component (cf 10669) | pscomponent:org/rhtpa-server | Custom field |
| Stream (cf 10832) | rhtpa-2.2 | Custom field |
| Existing issue links | Depend to TC-8100 (In Progress), Depend to TC-8101 (Open, Blocks TC-8100) | `issuelinks` |
| Existing comments | (1) `[sdlc-workflow] Description digest: sha256-md:a1b2…b2` (2026-07-01T10:00Z); (2) Post-triage summary with footnote, v0.11.1 (2026-07-01T10:01Z) | Comment history |

All critical fields (CVE ID, library, affected range) parsed successfully.

**Stream scope**: scoped to **2.2.x**.

## Step 1.5 / 1.7

- Step 1.5: MITRE and OSV lookups are simulated as unavailable in this eval. The Jira description threshold (< 0.11.14, fixed in 0.11.14) is used, with reduced confidence noted.
- Step 1.7: skipped because no Embargo policy URL is configured, even though CVSS 7.5 meets the threshold.

## Step 2 – Version impact (re-verification, simulated lock-file data)

| Stream | Version | Build | backend tag | quinn-proto | Affected (< 0.11.14)? |
|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | 0.3.8 | v0.3.8 | 0.11.9 | YES (out of scope) |
| 2.1.x | 2.1.1 | 0.3.12 | v0.3.12 | 0.11.9 | YES (out of scope) |
| **2.2.x** | **2.2.0** | 0.4.5 | v0.4.5 | 0.11.9 | **YES** |
| **2.2.x** | **2.2.1** | 0.4.8 | v0.4.8 | 0.11.12 | **YES** |
| **2.2.x** | **2.2.2** | 0.4.9 | v0.4.8 (backend retag of 2.2.1) | 0.11.12 (same as 2.2.1) | **YES** |
| 2.2.x | 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | NO |
| 2.2.x | 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | NO |

Note: by the retag rule, 2.2.2 ships the same backend as 2.2.1 (`v0.4.8`, quinn-proto 0.11.12), so it is **affected**. The prior run's summary comment says "RHTPA 2.2.2 and later ship quinn-proto 0.11.14 (not affected)". The matrix contradicts that statement. See `idempotency-check.md` and `triage-outcome.md`.
