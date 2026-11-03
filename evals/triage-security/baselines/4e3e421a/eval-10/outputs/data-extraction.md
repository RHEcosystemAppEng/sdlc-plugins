# TC-8020 — Data Extraction (Steps 0–1.7)

## Step 0 — Configuration validation

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | not configured (Step 4.3 and Step 7 skipped) |
| ProdSec contact / account ID | not configured (no ProdSec @mentions) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column; defaults to `upstream`, coordination guidance omitted per backward-compat rule) |

All required sections exist (Repository Registry, Jira Configuration, Code Intelligence, Security Configuration). Proceeding.

## Step 0.3 — Matrix staleness check

`<!-- Last-Updated: 2026-06-28T10:00:00Z -->` — today is 2026-11-03, so the matrix is **128 days old** (threshold 14 days).

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28 (128 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now  2. Proceed anyway  3. Stop

Eval mode: proceeding with the current matrix ("Proceed anyway"). The staleness is recorded in the triage summary.

## Step 0.6 / 0.7 — Mode

`FULLSEND_OUTPUT_DIR` absent → interactive mode (simulated; Jira mutations are written to files instead of executed).

## Step 0.8 — Assign and transition (proposed)

- Assign TC-8020 to the current user (currently Unassigned).
- Status is **New** → transition to **Assigned** (transition ID discovered dynamically via `get_transitions`).

## Step 1 — Extracted CVE data

| Field | Value |
|---|---|
| Issue key | TC-8020 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.2] |
| Status | New |
| CVE ID | CVE-2026-55123 (label + summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Affects Versions (Jira) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Ecosystem | Cargo (Rust crate) → source dependency category |
| Affected version range | < 1.42.0 ("versions before 1.42.0") |
| Fixed version | 1.42.0 |
| Severity | CVSS 8.1 (High) |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp (also RUSTSEC-2026-0088) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 (already past as of 2026-11-03) |
| Existing comments | none |
| Existing issue links | none |
| Custom fields on issue | Upstream Affected Component = tokio; PS Component = pscomponent:org/rhtpa-server; Stream = rhtpa-2.2 |

### Stream scope resolution

- Suffix `[rhtpa-2.2]` → stream **2.2.x** (matches Version Streams table, Konflux repo `rhtpa-release.0.4.z`).
- Issue is **scoped** to 2.2.x. Stream 2.1.x is outside this issue's scope → Case A applies if 2.1.x is affected.

### Ecosystem detection

- tokio is a Rust crate → **Cargo**, listed in both streams' Ecosystem Mappings.
- Lock file: `Cargo.lock` in repository `backend` (rhtpa-backend); check command `git show <tag>:Cargo.lock`.
- Classification: source dependency → **2 tasks per affected stream** (upstream backport/dependency bump + downstream propagation).

### Deployment context

rhtpa-backend: Source Repositories table has no Deployment Context column → default `upstream`; per backward-compatibility rule, the Coordination Guidance subsection is omitted from task descriptions.

## Step 1.5 — External CVE data enrichment

MITRE / OSV were not queried (eval constraint: no external calls). Treated as unavailable:

> External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used for Step 2: **tokio < 1.42.0, fixed in 1.42.0**.

## Step 1.7 — Embargo check

CVSS 8.1 meets the Critical/Important threshold, but no Embargo policy URL is configured → step skipped silently per skill rules.
