# TC-8060 — Step 1: Data Extraction

Skill: `/sdlc-workflow:triage-security` (interactive mode; `FULLSEND_OUTPUT_DIR` not set).
Eval constraints: no Jira MCP, `git show`, WebFetch or other external calls were made. All data
comes from the provided fixtures (`vuln-issue-transitive.md`, `security-matrix-mock.md`,
`claude-md-security-config.md`).

## Step 0 — Configuration validation (from claude-md-security-config.md)

| Item | Value | Status |
|------|-------|--------|
| Repository Registry | rhtpa-backend (serena_backend) | present |
| Project key | TC | present |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | present |
| Code Intelligence | `mcp__<serena-instance>__<tool>` naming | present |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | present |
| Jira version prefix | RHTPA | present |
| Vulnerability issue type ID | 10024 | present |
| Component label pattern | `pscomponent:` | present |
| VEX Justification custom field | customfield_12345 | configured (optional) |
| Upstream Affected Component field | not configured | Step 4.3 cross-CVE overlap and Step 7 concurrent triage skipped |
| Embargo policy URL | not configured | Step 1.7 skipped |
| ProdSec contact / Jira account ID | not configured | @mentions of ProdSec skipped |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z | present |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend) | present; no Deployment Context column -> default `upstream`, coordination guidance omitted (backward-compat rule) |

## Step 0.3 — Matrix staleness check

Matrix `Last-Updated: 2026-06-28T10:00:00Z`; today is 2026-11-26 -> **151 days old** (threshold 14 days).

> Security matrix for stream **2.2.x** was last updated on 2026-06-28 (151 days ago). The matrix may
> not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

Eval run: **proceeded anyway** with the provided matrix (refresh would require external git access).
Releases after 2.2.4 (if any) are not reflected in this analysis.

## Step 0.8 — Assign and transition (proposed, not executed)

- Assign TC-8060 to the current user (`jira.user_info()` account ID).
- Transition New -> Assigned (transition discovered dynamically via `jira.get_transitions`).

## Step 1 — Parsed CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8060 | Issue |
| Issue type / Status | Vulnerability / New | Issue (status-aware handling: New -> full triage) |
| CVE ID | CVE-2026-99010 | Label `CVE-2026-99010` + summary |
| Summary | CVE-2026-99010 h2 - Memory exhaustion via CONTINUATION frames [rhtpa-2.2] | Issue |
| Affected component | `pscomponent:org/rhtpa-server` -> rhtpa-backend (backend) | Component label |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | h2 (Rust crate) | Description |
| Ecosystem | Cargo (source dependency -> 2 remediation tasks per stream) | Library name + Ecosystem Mappings |
| Affected version range | < 0.4.5 ("before version 0.4.5") | Description |
| Fixed version | 0.4.5 | Description |
| CVSS / Severity | 7.5 (High) — DoS | Description |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | none (no GHSA link present) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99010 | Remote links |
| Due date | 2026-08-15 (already past as of 2026-11-26) | `duedate` |
| Reporter | psirt-analyst (557058:psirt-analyst-mock-id) | Issue (used for mandatory @mention in summary comment) |
| Assignee | Unassigned | Issue |
| Existing comments | none | Issue |
| Deployment context | upstream (default — no Deployment Context column) | Source Repositories |

All critical fields (CVE ID, library, affected range) parsed successfully.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` -> stream **2.2.x** -> Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue is **scoped** to 2.2.x. Steps 3–8 operate on 2.2.x; other streams are only checked for Case A cross-stream impact.

## Step 1.5 — External CVE data enrichment

MITRE CVE API and OSV.dev were **not queried** (eval: no external calls). Treated as unavailable:

> External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used for Step 2.3: **h2 < 0.4.5 affected; 0.4.5 fixed**.

## Step 1.7 — Embargo check

Skipped: no Embargo policy URL configured (CVSS 7.5 would otherwise have triggered the gate).
