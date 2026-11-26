# TC-8001 — Step 1: Data Extraction

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Eval run: no Jira, git, or external
calls were made. Data came from the provided mock files.

## Step 0 — Configuration validation (claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | not configured, so Step 4.3 overlap and Step 7 concurrent triage are skipped |
| ProdSec account ID / email | not configured, so no @mentions are added |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream` and Coordination Guidance is omitted) |

All required sections are present, so the run continues.

## Step 0.3 — Matrix staleness

Neither stream's `security-matrix.md` (mock) has a `<!-- Last-Updated -->` timestamp. Warning
(non-blocking): *"Security matrix for streams 2.1.x and 2.2.x has no Last-Updated
timestamp. Consider running `/setup` to populate it with a timestamp for future staleness
checks."* The run continues.

## Step 0.8 — Assign and transition (planned, not executed)

- `jira.user_info()` → `jira.edit_issue(TC-8001, assignee=<current-user>)`. Status is New,
  so `get_transitions` is called and the issue moves to **Assigned**.

## Step 1 — Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8001 | issue |
| CVE ID | CVE-2026-31812 | label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | label |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]`, which maps to stream **2.2.x** | summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | quinn-proto | description |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | description |
| Fixed version | 0.11.14 | description |
| Severity | CVSS 7.5 (High), DoS (panic via excessive STREAMS frame) | description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | remote link |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | remote link / references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | remote link |
| Due date | 2026-07-15 | `duedate` |
| Status / Assignee | New / Unassigned | issue |
| Existing comments | none | issue |

### Stream scope resolution

- The suffix `[rhtpa-2.2]` maps to the configured Version Stream **2.2.x**
  (git.example.com/rhtpa/rhtpa-release.0.4.z). The issue is **scoped** to 2.2.x.
- The PSIRT Affects Versions value `RHTPA 2.0.0` does not belong to any configured stream and
  conflicts with the summary scope. Step 3 corrects it.

### Ecosystem detection

- quinn-proto is a Rust crate, so the ecosystem is **Cargo**. It is listed in both streams'
  Ecosystem Mappings (repo `backend`, lock file `Cargo.lock`).
- Category: **Source dependency**, so each affected stream gets 2 remediation tasks.

### Deployment context

- Affected repository: rhtpa-backend (`backend`). The Source Repositories table has no
  Deployment Context column, so the context defaults to `upstream` (backward
  compatibility) and the Coordination Guidance subsection is omitted.

## Step 1.5 — External CVE enrichment

MITRE (`cveawg.mitre.org/api/cve/CVE-2026-31812`) and OSV.dev were **not queried**
because external calls are not allowed in this eval. Both are treated as unavailable:

> "External CVE databases unavailable — using Jira description data only. Fix
> threshold confidence is reduced."

Fix threshold used for Step 2: **quinn-proto < 0.11.14 is affected, 0.11.14 is fixed**.

## Step 1.7 — Embargo check

Skipped because no Embargo policy URL is configured. CVSS 7.5 would otherwise trigger the gate.
