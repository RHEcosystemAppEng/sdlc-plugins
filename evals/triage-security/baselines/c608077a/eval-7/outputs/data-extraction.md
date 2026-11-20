# Step 1 – Data Extraction: TC-8006

> Simulated eval run. Jira MCP, `git show`, and external CVE APIs were **not** called. All data below comes from the provided input files (`vuln-issue-sibling-prelinked.md`, `security-matrix-mock.md`, `claude-md-security-config.md`).

## Step 0 – Configuration validation

| Item | Value | Status |
|---|---|---|
| Project key | TC | OK |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | OK |
| Jira version prefix | RHTPA | OK |
| Vulnerability issue type ID | 10024 | OK |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | OK |
| Component label pattern | `pscomponent:` | OK |
| VEX Justification field | customfield_12345 | configured |
| Upstream Affected Component field | not configured | Steps 4.3, 7, 7.5.3 skipped |
| ProdSec Jira account ID | not configured | @mentions omitted |
| Embargo policy URL | not configured | Step 1.7 skipped |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) | OK |
| Source Repositories | rhtpa-backend (no Deployment Context column, defaults to `upstream`) | OK |

### Step 0.3 – Matrix staleness

`<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-20, so the matrix is **145 days old**, past the 14-day threshold. In an interactive run the engineer would choose Refresh / Proceed / Stop. For this eval we **proceed with the current matrix** and flag the staleness here.

### Step 0.6 – Mode

`FULLSEND_OUTPUT_DIR` is not set, so this is interactive mode. Jira writes are written to these files as proposals and are not executed.

## Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8006 | Issue |
| Status | New | Issue (full triage path) |
| CVE ID | CVE-2026-31812 | Label + summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label |
| Stream suffix (PSIRT-claimed) | `[rhtpa-2.1]` | Summary |
| Issue stream scope | **2.1.x** (rhtpa-release.0.3.z) | Matched to Version Streams table |
| Affects Versions (current Jira) | RHTPA 2.1.0 | `versions` field |
| Vulnerable library | quinn-proto | Description |
| Ecosystem | Cargo (source dependency, so 2 remediation tasks per stream) | Library name + Ecosystem Mappings |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Vulnerability type | DoS (panic from unbounded STREAMS frame allocation) | Description |
| Upstream fix PR | none in remote links | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Other references | https://rustsec.org/advisories/RUSTSEC-2026-0042.html | Description |
| Due date | 2026-07-15 | `duedate` |
| Assignee | Unassigned. Step 0.8 would assign to the current user and transition to Assigned | Issue |
| Existing comments | none | Issue |
| Existing issue links | Related → TC-8001 (link ID 1990401, outward) | `issuelinks` |
| Deployment context (rhtpa-backend) | upstream (default) | Source Repositories |

## Step 1.5 – External enrichment

MITRE and OSV were not queried because the eval forbids external calls. Following the "Unavailable" rule, the skill falls back to the Jira description: fix threshold **0.11.14**, with reduced confidence.

## Step 1.7 – Embargo check

Skipped. No Embargo policy URL is configured, even though CVSS 7.5 would otherwise trigger the gate.

## Step 2 – Version impact (simulated lock-file data)

| Stream | Version | Build | backend tag | quinn-proto | Affected (< 0.11.14)? |
|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | 0.3.8 | v0.3.8 | 0.11.9 | **YES** |
| 2.1.x | 2.1.1 | 0.3.12 | v0.3.12 | 0.11.9 | **YES** |
| 2.2.x | 2.2.0 | 0.4.5 | v0.4.5 | 0.11.9 | YES |
| 2.2.x | 2.2.1 | 0.4.8 | v0.4.8 | 0.11.12 | YES |
| 2.2.x | 2.2.2 | 0.4.9 | v0.4.8 | same as 2.2.1 (retag) | YES |
| 2.2.x | 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | NO |
| 2.2.x | 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | NO |

Not determinable without live tools: the development stream (Step 2.2 needs unreleased Jira versions) and upstream fix status on `release/0.3.z` (Step 2.5 needs `git show`).

## Step 3 – Affects Versions correction (scoped to 2.1.x)

- Current: `[RHTPA 2.1.0]` → Proposed: `[RHTPA 2.1.0, RHTPA 2.1.1]` (correct but incomplete, since 2.1.1 also ships quinn-proto 0.11.9).
- 2.2.x versions are excluded because they belong to sibling TC-8001.
- This needs engineer confirmation and a correction comment with the Comment Footnote. No ProdSec @mention, because none is configured.
