# TC-8001 Triage — Step 0 / Step 1 Data Extraction

_Simulated run: no Jira MCP, git, or WebFetch calls were made. All values come from the provided mock inputs (vuln-issue-standard.md, security-matrix-mock.md, claude-md-security-config.md)._

## Step 0 – Configuration Validation

| Item | Value |
|------|-------|
| Repository Registry | present (rhtpa-backend) |
| Jira Configuration | Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Code Intelligence | present (`mcp__<instance>__<tool>`, serena_backend) |
| Security Configuration | present |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component / PS Component / Stream fields | not configured (Steps 4.3, 7, and 7.5.3 dedup are skipped) |
| ProdSec contact / Jira account ID | not configured (no @mentions of ProdSec) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend → https://github.com/rhtpa/rhtpa-backend |

**Deployment Context:** the Source Repositories table has **no Deployment Context column**. Per Step 0 (backward compatibility), every repo defaults to `upstream` internally (rhtpa-backend → `upstream`). Because the column is absent, `remediation-templates.md` requires the **Coordination Guidance subsection be omitted entirely** from the remediation task descriptions.

**Step 0.3 Matrix staleness:** matrix `Last-Updated: 2026-06-28T10:00:00Z`. That is well over 14 days before today (2026-11-27), so the skill would warn and offer Refresh / Proceed / Stop. For this eval, the run assumes **Proceed anyway**.

**Step 0.6:** `FULLSEND_OUTPUT_DIR` is absent, so this is interactive mode.
**Step 0.8 (proposed, not executed):** assign TC-8001 to the current user and transition New → Assigned.

## Step 1 – Parsed CVE Data

| Field | Value |
|-------|-------|
| Issue key | TC-8001 |
| Issue type / Status | Vulnerability / New |
| CVE ID | CVE-2026-31812 (from label and summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed, summary suffix) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 (**incorrect**: there is no 2.0.x stream) |
| Vulnerable library | quinn-proto |
| Ecosystem | Cargo (Rust crate). This is a source dependency, so 2 remediation tasks per stream |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| Severity | CVSS 7.5 (High), DoS (panic on excessive STREAMS frames) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Existing comments | none |
| Affected repository | rhtpa-backend ("backend" in Ecosystem Mappings) |
| Deployment context | `upstream` (default; column absent, so coordination guidance is omitted) |

### Stream scope resolution

Suffix `[rhtpa-2.2]` maps to the configured stream **2.2.x** (rhtpa-release.0.4.z). The issue is **scoped** to 2.2.x.

### Step 1.5 – External enrichment

MITRE/OSV were not queried (no external calls are allowed in this eval). The run falls back to the Jira description: fix threshold is **0.11.14** (affected < 0.11.14). Fix-threshold confidence is reduced.

### Step 1.7 – Embargo check

Skipped. No Embargo policy URL is configured, even though CVSS 7.5 is above the threshold.

## Step 2 – Version Impact (from mock lock-file data)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | backend tag | quinn-proto | Affected? | Notes |
|--------|---------|-------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | out of issue scope |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | out of issue scope |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.8 | — | YES | same as 2.2.1 (backend retag) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | |

Development stream (Step 2.2): there is no Jira version data to identify an unreleased version, so a development-head check was not possible. Flag for the engineer.

Dependency chain (Step 2.3.5): no Cargo.toml or manifest evidence is available in the inputs, so direct vs transitive cannot be determined. quinn-proto is typically pulled in transitively via `quinn` (for example reqwest http3 / QUIC). This needs engineer confirmation. Profile is assumed production; no evidence of dev-only use.

Upstream fix status (Step 2.5, inferred from the latest pinned tags because branch HEAD was not readable):

| Stream | Ecosystem | Upstream Branch | Latest evidence | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | v0.4.12 → 0.11.14 | YES (dependency-bump variant) |
| 2.1.x | Cargo | release/0.3.z | v0.3.12 → 0.11.9 | NO (backport needed) |

## Step 3 – Affects Versions Correction (proposed)

`Current: [RHTPA 2.0.0] → Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`. The correction is scoped to stream 2.2.x. The 2.1.x versions belong to a sibling issue or preemptive tasks. Jira version IDs must be discovered dynamically via `getJiraIssueTypeMetaWithFields`.

## Steps 4–7 (simulated)

- Step 4 sibling search (JQL `labels = 'CVE-2026-31812'`) was not executed. The run assumes no siblings, so 2.1.x has no CVE Jira and gets preemptive tasks.
- Step 4.3 was skipped (field not configured). Step 4.4 assumes no existing preemptive task.
- Step 5: the lifecycle page was not fetched. The run assumes 2.1.x and 2.2.x are supported.
- Step 6: no resolved siblings.
- Step 7: skipped (Upstream Affected Component field not configured).
- Step 7.5: proposed release Epic/Task for 2.2.x: "RHTPA 2.2.5 Release Tasks" / "RHTPA 2.2.5 CVE triage" (next patch after 2.2.4). This requires engineer confirmation. No release Jira link is made for 2.1.x, because its tasks are preemptive and only non-preemptive remediation is linked to release Jira. Dedup (7.5.3) is skipped.
