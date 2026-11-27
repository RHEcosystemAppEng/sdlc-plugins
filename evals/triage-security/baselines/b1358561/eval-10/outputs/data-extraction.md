# TC-8020 — Step 0 / Step 1 Data Extraction

Skill: `sdlc-workflow/triage-security` (interactive mode — `FULLSEND_OUTPUT_DIR` not set; eval run: no Jira/Git/WebFetch calls, simulated data from input files)

## Step 0 – Configuration validation

| Required section | Status | Value(s) |
|---|---|---|
| Repository Registry | Present | rhtpa-backend (serena_backend) |
| Jira Configuration | Present | Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Code Intelligence | Present | `mcp__<instance>__<tool>`, serena_backend |
| Security Configuration → Product Lifecycle | Present | Product pages URL `https://access.example.com/product-life-cycle/rhtpa`, Jira version prefix `RHTPA`, Vulnerability issue type ID `10024`, Component label pattern `pscomponent:`, VEX Justification field `customfield_12345` |
| Security Configuration → Version Streams | Present | 2.1.x → `rhtpa-release.0.3.z`; 2.2.x → `rhtpa-release.0.4.z` |
| Security Configuration → Source Repositories | Present | rhtpa-backend → `https://github.com/rhtpa/rhtpa-backend` (no Deployment Context column) |

Optional configuration not present in Security Configuration:

- Upstream Affected Component / PS Component / Stream custom fields — **not configured** → Step 4.3 (cross-CVE overlap), Step 7 (concurrent triage) and Step 7.5.3 (cross-CVE dedup) are skipped. (The issue itself carries `customfield_10632`, `customfield_10669`, `customfield_10832` values, but the skill only uses these when configured.)
- ProdSec contact email / ProdSec Jira account ID — not configured → no ProdSec @mentions.
- Embargo policy URL — not configured → Step 1.7 skipped.
- Deployment Context column — absent → deployment context defaults to `upstream` for metadata; Coordination Guidance subsection is omitted from task descriptions (backward-compatibility rule in `remediation-templates.md`).

## Step 0.3 – Matrix staleness check

| Stream | Last-Updated | Age (as of 2026-11-27) | Result |
|---|---|---|---|
| 2.1.x (rhtpa-release.0.3.z) | 2026-06-28T10:00:00Z | 152 days | **STALE** (> 14 days) |
| 2.2.x (rhtpa-release.0.4.z) | 2026-06-28T10:00:00Z | 152 days | **STALE** (> 14 days) |

> Security matrix for streams 2.1.x and 2.2.x was last updated on 2026-06-28 (152 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now  2. Proceed anyway  3. Stop

Eval run: proceeding with the current matrix ("Proceed anyway"). Any 2.2.x/2.1.x releases after 2026-06-28 are not covered by this triage and should be checked after a matrix refresh.

## Step 0.8 – Assign and transition (proposed, not executed)

- Assign TC-8020 to the current user (`jira.user_info()` → account ID).
- Issue status is **New** → transition to **Assigned** (transition ID discovered via `jira.get_transitions`).

## Step 1 – Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8020 | — |
| Issue type / Status | Vulnerability / New | Issue |
| CVE ID | **CVE-2026-55123** | Label + summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label (pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira) | RHTPA 2.2.0, RHTPA 2.2.1 | `versions` field |
| Vulnerable library | **tokio** (Rust crate) | Description |
| Affected version range | **< 1.42.0** ("versions before 1.42.0") | Description |
| Fixed version | **1.42.0** | Description |
| Vulnerability | Use-after-free when a spawned task is aborted while holding a borrowed reference (memory corruption, potential code execution) | Description |
| CVSS | 8.1 (High) | Description |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 | Remote link |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp (also RUSTSEC-2026-0088: https://rustsec.org/advisories/RUSTSEC-2026-0088.html) | Remote link / References |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 | Remote link |
| Due date | 2026-08-15 (already past as of 2026-11-27) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing links | None | `issuelinks` |
| Existing comments | None | Comments |
| Upstream Affected Component (customfield_10632) | tokio | Custom field (informational — field not configured) |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-server | Custom field (informational) |
| Stream (customfield_10832) | rhtpa-2.2 | Custom field (informational) |
| Reporter | Not present in mock data — reporter account ID required for the post-triage summary @mention | — |
| Security level | Not present in mock data — copy the parent's level into every `create_issue` call if set | — |

### Stream scope resolution

- Suffix `[rhtpa-2.2]` → stream **2.2.x** → Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z` (local `/home/dev/repos/rhtpa-release.0.4.z`).
- Issue is **SCOPED** to 2.2.x. Steps 3–4 and Case B are scoped to 2.2.x; other affected streams are handled by Case A.

### Ecosystem detection

- tokio is a Rust crate → **Cargo** ecosystem (present in both streams' Ecosystem Mappings: repository `backend`, lock file `Cargo.lock`).
- Category: **source dependency** → 2 remediation tasks per stream (upstream backport + downstream propagation, or dependency bump + downstream propagation if the upstream branch already has the fix).

### Deployment context

- Affected repository: rhtpa-backend (`backend` in Ecosystem Mappings) → not specified (no Deployment Context column) → defaults to `upstream`. Coordination Guidance is omitted from task descriptions because the column is absent.

## Step 1.5 – External CVE data enrichment

- MITRE CVE API (`https://cveawg.mitre.org/api/cve/CVE-2026-55123`) and OSV.dev (`https://api.osv.dev/v1/vulns/CVE-2026-55123`) — **not queried** (eval: no external calls).
- Treated as unavailable: "External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced."
- Fix threshold used for Step 2: **tokio < 1.42.0 is affected; 1.42.0 is fixed** (Jira description, consistent with the threshold given in the task).

## Step 1.7 – Embargo check

- CVSS 8.1 (High) meets the threshold, but **no Embargo policy URL is configured** → step skipped silently. (Recommend the engineer confirm the CVE is public: it has a public GHSA, RUSTSEC entry and upstream PR, so it is very likely not under embargo.)
