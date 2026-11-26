# Step 1 – Data Extraction: TC-8021

Mode: interactive (no `FULLSEND_OUTPUT_DIR`); simulated per the eval instructions. No Jira MCP, WebFetch or `git show` calls were made. All values below come from the provided input files.

> **Key discrepancy:** the task names the issue **TC-8021**, but the mock issue file (`vuln-issue-standard.md`) has `Key: TC-8001`. This analysis uses TC-8021, as the task instructs, and treats the mock file's content as that issue's data.

## Step 0 – Configuration validation (from claude-md-security-config.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | rhtpa-backend | Present |
| Project key | TC | Present |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | Present |
| Code Intelligence | serena_backend | Present |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | Present |
| Jira version prefix | RHTPA | Present |
| Vulnerability issue type ID | 10024 | Present |
| Component label pattern | `pscomponent:` | Present |
| VEX Justification field | customfield_12345 | Present |
| Upstream Affected Component field | customfield_10632 | Assumed configured, per the eval instructions (not in the mock CLAUDE.md) |
| PS Component / Stream custom fields | — | Not configured, so Step 4.3 is skipped |
| ProdSec contact / account ID | — | Not configured, so @mentions are skipped silently |
| Embargo policy URL | — | Not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) | Present |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) | Present |

Result: configuration is valid, so triage proceeds.

## Step 0.3 – Matrix staleness

- `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-26, so the matrix is **151 days old**. That is well past the 14-day threshold.
- Warning to the engineer: "Security matrix for streams **2.1.x / 2.2.x** was last updated on 2026-06-28 (151 days ago). The matrix may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop."
- Eval assumption: **Proceed anyway**, using the provided matrix. Releases after 2.2.4 may be missing.

## Step 0.8 – Assign and transition (proposed, not executed)

- Assign TC-8021 to the current user.
- The issue status is **New**, so transition it to **Assigned** using a dynamically discovered transition.

## Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8021 (mock file shows TC-8001) | Task / issue file |
| CVE ID | **CVE-2026-31812** | Label + summary |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | Summary |
| Status | New | Issue |
| Assignee | Unassigned | Issue |
| Affected component | `pscomponent:org/rhtpa-server` | Label |
| Upstream Affected Component (customfield_10632) | **quinn-proto** | Eval instructions |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Issue |
| Vulnerable library | **quinn-proto** (Rust crate) | Description |
| Affected version range | **< 0.11.14** ("versions before 0.11.14") | Description |
| Fixed version | **0.11.14** | Description |
| CVSS | 7.5 (High), denial of service (panic on an unbounded STREAMS frame) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote link |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq; https://rustsec.org/advisories/RUSTSEC-2026-0042.html | Remote link / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote link |
| Due date | 2026-07-15 (already passed as of 2026-11-26) | Issue |
| Existing comments | None | Issue |

## Stream scope resolution

- The suffix `[rhtpa-2.2]` maps to the configured stream **2.2.x** (rhtpa-release.0.4.z).
- The issue is **scoped** to 2.2.x.

## Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**.
- Cargo is listed in both streams' Ecosystem Mappings (repository `backend`, lock file `Cargo.lock`).
- Category: source dependency, so remediation needs 2 tasks per stream.

## Deployment context

- The affected repository is rhtpa-backend.
- The Source Repositories table has no Deployment Context column, so it defaults to **upstream**.

## Step 1.5 – External enrichment

- MITRE and OSV.dev were not queried because external calls are forbidden in this eval. Both are treated as unavailable.
- "External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced."
- Fix threshold used: **0.11.14**, from the Jira description.

## Step 1.7 – Embargo check

- No Embargo policy URL is configured, so this step was skipped silently. CVSS 7.5 would otherwise have met the threshold.
