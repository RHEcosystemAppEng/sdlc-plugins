# TC-8060 — Step 1: Data Extraction

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Eval run: Jira, `git show`, and
WebFetch calls were simulated from fixture files; no external services contacted.

## Step 0 — Configuration validation (from claude-md-security-config.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | not configured (Step 4.3 and Step 7 skipped) |
| ProdSec Jira account ID | not configured (no ProdSec @mentions) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend); Deployment Context column absent → defaults to `upstream` |

All required sections exist: Repository Registry, Jira Configuration, Code Intelligence, Security Configuration. Validation passed.

## Step 0.3 — Matrix staleness check

| Stream | Last-Updated | Age (as of 2026-11-23) | Status |
|--------|--------------|------------------------|--------|
| 2.1.x | 2026-06-28T10:00:00Z | 148 days | STALE (threshold 14 days) |
| 2.2.x | 2026-06-28T10:00:00Z | 148 days | STALE (threshold 14 days) |

> Security matrix for stream **2.2.x** was last updated on 2026-06-28 (148 days ago).
> The matrix may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

Eval decision: **Proceed anyway** (non-interactive eval; refresh would need Konflux repo access).

## Step 0.8 — Assign and transition (simulated, not executed)

- Issue status is **New** → would assign to current user and transition to **Assigned** after confirmation.

## Step 1 — Parsed CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8060 | Issue |
| Issue status | New (full triage path) | Issue status |
| CVE ID | CVE-2026-99010 | Label `CVE-2026-99010` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Component label |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | h2 (Rust crate) | Description |
| Affected version range | < 0.4.5 ("versions before 0.4.5") | Description |
| Fixed version | 0.4.5 | Description |
| Vulnerability | Memory exhaustion via unbounded CONTINUATION frames (DoS) | Description / summary |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote link |
| Advisory URL | none (no GHSA/advisory remote link) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99010 | Remote link |
| Due date | 2026-08-15 (already past due as of 2026-11-23) | `duedate` |
| Reporter | psirt-analyst (account ID 557058:psirt-analyst-mock-id) | Reporter |
| Assignee | Unassigned | Assignee |
| Existing comments | none | Comment history |

All critical fields (CVE ID, library, affected range) parsed. No engineer input needed.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` → stream **2.2.x** → matches Version Streams row `rhtpa-release.0.4.z`.
- **Issue stream scope: 2.2.x (scoped)**. Steps 2–8 are scoped to 2.2.x. Stream 2.1.x is examined only for Case A cross-stream impact.

### Ecosystem detection

- h2 is a Rust crate → ecosystem **Cargo** (listed in the 2.2.x Ecosystem Mappings table).
- Category: **source dependency** → 2 remediation tasks per affected stream.
- Lock file: `Cargo.lock`; check command: `git show <tag>:Cargo.lock`; upstream branch: `release/0.4.z`; repository: backend (rhtpa-backend).

### Deployment context

- Affected repository: rhtpa-backend. The Source Repositories table has no Deployment Context column, so it defaults to `upstream`. Per `remediation-templates.md`, the Coordination Guidance subsection is left out of task descriptions when the column is absent.

## Step 1.5 — External CVE enrichment

- MITRE CVE API and OSV.dev were **not queried** (eval: no external calls), so they are treated as unavailable.
- > External CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced.
- Fix threshold used in Step 2.3: **h2 < 0.4.5 affected; >= 0.4.5 fixed** (Jira description).

## Step 1.7 — Embargo check

- No Embargo policy URL is configured, so this step is skipped silently. (CVSS 7.5 would otherwise trigger the gate.)
