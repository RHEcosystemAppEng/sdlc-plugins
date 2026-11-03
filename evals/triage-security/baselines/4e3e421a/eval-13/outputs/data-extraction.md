# TC-8001 — Step 1: Data Extraction

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Eval constraint: no Jira MCP / git / WebFetch calls were made;
all data below comes from the supplied mock files.

## Step 0 — Configuration validation (claude-md-security-config.md)

| Item | Value |
|---|---|
| Repository Registry | present (rhtpa-backend) |
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Code Intelligence | present (serena_backend) |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | not configured (Step 4.3 and Step 7 skipped) |
| ProdSec contact / account ID | not configured (no @mentions of ProdSec) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z ; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend) — no Deployment Context column -> defaults to `upstream`; coordination guidance omitted (backward compatibility rule) |

Result: configuration complete — proceed.

## Step 0.3 — Matrix staleness check

`<!-- Last-Updated: 2026-06-28T10:00:00Z -->` vs today 2026-11-03 -> **128 days old** (threshold 14 days).

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28 (128 days ago).
> The matrix may not reflect recent releases. Options: 1. Refresh now  2. Proceed anyway  3. Stop

Eval assumption: engineer chose **Proceed anyway** (no refresh possible without git access).

## Step 0.8 — Assign and transition (planned, not executed)

Status is `New`, Assignee `Unassigned` -> planned: `jira.user_info()`, `jira.edit_issue(TC-8001, assignee=<me>)`,
`jira.get_transitions(TC-8001)` -> select transition whose target is "Assigned" -> `jira.transition_issue`.

## Parsed CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| Status | New | Issue |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` -> org/rhtpa-server | Labels |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | quinn-proto (Rust crate) | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| Severity | CVSS 7.5 (High) — DoS (panic on excessive stream count) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (already past as of 2026-11-03) | `duedate` |
| Existing comments | none | Comment history |

All critical fields (CVE ID, library, affected range) parsed successfully.

## Stream scope resolution

Summary suffix `[rhtpa-2.2]` -> stream **2.2.x** (matches configured Version Streams row
`git.example.com/rhtpa/rhtpa-release.0.4.z`). Issue is **scoped** to 2.2.x.

## Ecosystem detection

quinn-proto is a Rust crate -> **Cargo** (listed in both streams' Ecosystem Mappings, lock file `Cargo.lock`,
repository `backend`). Category: **source dependency** -> 2 remediation tasks per stream
(upstream backport + downstream propagation).

## Deployment context

Affected repository: rhtpa-backend (`backend`) -> no Deployment Context column -> default `upstream`.
Because the column is absent, the Coordination Guidance subsection is omitted from task descriptions.

## Step 1.5 — External CVE data enrichment

MITRE (`https://cveawg.mitre.org/api/cve/CVE-2026-31812`) and OSV (`https://api.osv.dev/v1/vulns/CVE-2026-31812`)
were **not queried** (eval prohibits external calls) -> treated as unavailable:

> External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used for Step 2: **quinn-proto < 0.11.14 affected; 0.11.14 fixed**.

## Step 1.7 — Embargo check

CVSS 7.5 meets the >= 7.0 threshold, but no Embargo policy URL is configured -> step skipped silently.
