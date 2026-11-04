# Step 1 – Data Extraction: TC-8030

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Source: mock Jira issue fixture
(`vuln-issue-enrichment.md`). No live Jira calls were made.

## Step 0 – Configuration validation (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | not configured (Steps 4.3 and 7 skipped) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| ProdSec Jira account ID | not configured (no @mentions of ProdSec) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (Deployment Context column absent → default `upstream`; coordination guidance omitted per backward-compat rule) |

All required sections present. Proceeding.

## Step 0.3 – Matrix staleness check

`<!-- Last-Updated: 2026-06-28T10:00:00Z -->` → 129 days old as of 2026-11-04
(threshold 14 days).

> Security matrix was last updated on 2026-06-28 (129 days ago). The matrix may
> not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

Eval context: proceeding with the current (mock) matrix. Any 2.2.x/2.1.x releases
after 2026-05-04 would not be covered by this analysis.

## Step 0.8 – Assign and transition (proposed, not executed)

Status is **New**, Assignee is Unassigned → propose assigning to current user and
transitioning to the workflow's "Assigned" target (discovered dynamically via
`get_transitions`). Not executed in eval.

## Extracted fields

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8030 | Issue |
| CVE ID | CVE-2026-48901 | Label `CVE-2026-48901` + summary |
| Summary | CVE-2026-48901 h2 - HTTP/2 CONTINUATION flood [rhtpa-2.2] | Issue |
| Status | New | Issue |
| Affected component | `pscomponent:org/rhtpa-server` | Label |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | h2 (Rust crate, hyperium/h2) | Description |
| Affected version range | **"versions prior to the fix"** — imprecise, no numeric threshold | Description |
| Fixed version | **"see advisory"** — not stated | Description |
| CVSS | 7.5 (High) | Description |
| Vulnerability | HTTP/2 CONTINUATION flood — unbounded CONTINUATION frames after HEADERS → excessive memory/CPU (DoS) | Description |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p ; https://rustsec.org/advisories/RUSTSEC-2026-0089.html | Remote links / description |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 | Remote links |
| Due date | 2026-08-01 (already past as of 2026-11-04) | `duedate` |
| Existing comments | none | Issue |
| Reporter | not present in fixture (needed for post-triage @mention) | — |

### Critical-field check

- CVE ID: parsed.
- Library: parsed (h2).
- Affected range: **not parseable from the Jira description** ("versions prior to
  the fix"). Rather than stopping to ask the engineer, Step 1.5 external enrichment
  (always run) supplies the structured threshold; see `enrichment.md`. Had both
  external sources been unavailable, triage would stop here and ask the engineer.

## Stream scope resolution

- Suffix `[rhtpa-2.2]` → stream **2.2.x**
- Matches Version Streams row: 2.2.x → `git.example.com/rhtpa/rhtpa-release.0.4.z`
- **Issue stream scope: 2.2.x (scoped)**. Steps 3–4 and Case B are limited to 2.2.x;
  other streams are evaluated for cross-stream impact (Case A).

## Ecosystem detection

- h2 is a Rust crate → **Cargo**
- Cargo is listed in both streams' Ecosystem Mappings (repo `backend`, lock file
  `Cargo.lock`, check `git show <tag>:Cargo.lock`)
- Classification: **source dependency** → 2 remediation tasks per affected stream

## Deployment context

Affected repository: rhtpa-backend (`backend` in Ecosystem Mappings). Source
Repositories table has no Deployment Context column → default `upstream`; per
remediation-templates.md the Coordination Guidance subsection is omitted when the
column is absent.
