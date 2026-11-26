# Step 1 – Data Extraction: TC-8001

## Step 0 – Configuration validation (pre-check)

All required sections are present in the project CLAUDE.md (`claude-md-security-config-embargo.md`):
Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`),
Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories).

| Config item | Value |
|---|---|
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Embargo policy URL | https://example.com/security/embargo-policy |
| Version Streams | 2.1.x (`rhtpa-release.0.3.z`), 2.2.x (`rhtpa-release.0.4.z`) |
| Source Repositories | rhtpa-backend (no Deployment Context column -> defaults to `upstream`) |
| Upstream Affected Component / PS Component / Stream fields | not configured (Steps 4.3 and 7 skipped) |
| ProdSec contact / account ID | not configured (skip @mentions silently) |

Mode: interactive (`FULLSEND_OUTPUT_DIR` absent); Steps 0.6/0.7 Fullsend handling not applicable.

## Step 0.3 – Matrix staleness check

`<!-- Last-Updated: 2026-06-28T10:00:00Z -->` -> 151 days old as of 2026-11-26 (threshold 14 days).

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28
> (151 days ago). The matrix may not reflect recent releases.
>
> Options: 1. Refresh now  2. Proceed anyway  3. Stop

Eval simulation: **Proceed anyway** (no external tools/git available). Findings below may miss
releases made after 2026-06-28.

## Step 0.8 – Assign and transition (not executed)

Would assign TC-8001 to the current user and transition New -> Assigned (with confirmation).
Not executed: Jira MCP calls are disallowed in this eval.

## Parsed CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| Status | New (full triage path) | Issue |
| CVE ID | CVE-2026-31812 | Labels + summary |
| Affected component | `pscomponent:org/rhtpa-server` -> repository `rhtpa-backend` (ecosystem mapping repo `backend`) | Labels |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` -> stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| Severity / CVSS | 7.5 (High) | Description |
| Vulnerability type | Denial of service (panic on excessive STREAMS frame stream count) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (already past as of 2026-11-26) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | none | Comment history |

All critical fields (CVE ID, library, affected range) parsed successfully.

## Stream scope resolution

- Suffix `[rhtpa-2.2]` -> matches configured Version Stream **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- Issue is **stream-scoped** to 2.2.x. Steps 3–4 are scoped to 2.2.x; other affected streams are handled via Case A (cross-stream).

## Ecosystem detection

- quinn-proto is a Rust crate -> **Cargo** (listed in both streams' Ecosystem Mappings).
- Category: **source dependency** -> 2 remediation tasks per stream.
- Lock file: `Cargo.lock`; check command `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`.

## Deployment context

- `rhtpa-backend` found in Source Repositories; Deployment Context column absent -> default `upstream`
  (per the backward-compatibility rule, coordination guidance is omitted from task descriptions).

## Step 1.5 – External CVE data enrichment

MITRE CVE API and OSV.dev were **not queried** (external calls disallowed in this eval).

> ⚠ External CVE databases unavailable — using Jira description data only.
> Fix threshold confidence is reduced.

Fix threshold used for Step 2: **quinn-proto < 0.11.14 affected; 0.11.14 fixed** (Jira description).
