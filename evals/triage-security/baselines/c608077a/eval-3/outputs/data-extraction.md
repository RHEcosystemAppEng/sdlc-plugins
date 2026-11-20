# Step 1 – Data Extraction: TC-8003

> Simulated run: Jira data taken from `vuln-issue-duplicate.md`; no Jira MCP, git, or web calls were made.

## Step 0 – Configuration validation (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component / PS Component / Stream fields | Not configured, so Steps 4.3, 7 and 7.5.3 are skipped |
| ProdSec contact / account ID | Not configured, so no @mentions are added |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| Version streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source repos | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

All required sections are present, so triage can go ahead.

## Step 0.3 – Matrix staleness

Both matrix streams have `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-20, so the matrix is **145 days old**, well past the 14-day threshold. In an interactive run the skill would stop here and offer three choices: Refresh, Proceed anyway, or Stop. For this eval I chose "Proceed anyway". The matrix may not list releases after 2.2.4.

## Step 0.8 – Assign / transition (proposed, not executed)

TC-8003 is in status **New** and unassigned. The skill would assign it to the current user and move it to Assigned.

## Extracted CVE data

| Field | Value |
|---|---|
| Issue key | TC-8003 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Status | New |
| CVE ID | CVE-2026-31812 (from the label and the summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| PSIRT-claimed product version (suffix) | `[rhtpa-2.2]` |
| Affects Versions (Jira) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Ecosystem | Cargo (source dependency, needs 2 remediation tasks per stream if a fix is needed) |
| Affected range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | None in the remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 (already passed) |
| Existing comments | None |
| Deployment context | upstream (default) |

## Stream scope resolution

The suffix `[rhtpa-2.2]` maps to configured stream **2.2.x** (rhtpa-release.0.4.z), so the issue is **scoped**.

## Step 1.5 – External enrichment

Not performed, because the eval forbids external calls. The fix threshold comes from the Jira description only (< 0.11.14, fixed in 0.11.14), so confidence is reduced.

## Step 1.7 – Embargo check

Skipped: no Embargo policy URL is configured. CVSS 7.5 would otherwise have triggered the gate.

## Step 2 – Version impact analysis (simulated lock-file data)

| Stream | Version | Backend tag | quinn-proto | Affected? |
|---|---|---|---|---|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.x | 2.2.2 | v0.4.8 (retag) | same as 2.2.1 | YES (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO |

The development stream cannot be determined because there was no Jira unreleased-version query. The latest 2.2.x release (2.2.4) already ships the fix.

## Step 3 – Affects Versions correction (scoped to 2.2.x)

- Current: [RHTPA 2.2.0]
- Lock-file evidence: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Because Step 4 finds a same-stream duplicate, I recommend **not** editing TC-8003's Affects Versions. Instead the gap is handed to the surviving issue, TC-7999 (see duplicate-check.md).
