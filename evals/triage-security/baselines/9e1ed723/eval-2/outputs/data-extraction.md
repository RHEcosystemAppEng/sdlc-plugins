# TC-8002 — Data Extraction (Step 0 – Step 1.7)

Skill: `/sdlc-workflow:triage-security` (followed from SKILL.md; executed in simulation —
no Jira MCP, `git show`, or WebFetch calls were made. All values come from the provided
mock input files.)

## Step 0.6 – Mode Detection

`FULLSEND_OUTPUT_DIR` is absent → **interactive mode** (Step 0.7 skipped).

## Step 0 – Configuration Validation (from claude-md-security-config.md)

| Required section | Present | Notes |
|---|---|---|
| Repository Registry | Yes | rhtpa-backend (serena_backend) |
| Jira Configuration | Yes | Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Code Intelligence | Yes | `mcp__<serena-instance>__<tool>` naming convention |
| Security Configuration → Product Lifecycle | Yes | All 4 required fields present |
| Security Configuration → Version Streams | Yes | 2 streams |
| Security Configuration → Source Repositories | Yes | 1 repo |

Extracted configuration:

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 (configured) |
| Upstream Affected Component field | not configured → Steps 4.3, 7, 7.5.3 skipped |
| PS Component / Stream custom fields | not configured |
| ProdSec contact email / Jira account ID | not configured → no ProdSec @mentions |
| Embargo policy URL | not configured → Step 1.7 skipped |
| Version streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source repositories | rhtpa-backend → https://github.com/rhtpa/rhtpa-backend (Deployment Context column absent → default `upstream`) |

Result: configuration valid, proceed.

## Step 0.3 – Matrix Staleness Check

| Stream | Last-Updated | Age (today 2026-11-23) | Status |
|---|---|---|---|
| 2.1.x / 2.2.x (mock matrix file) | 2026-06-28T10:00:00Z | 148 days | **STALE (> 14-day threshold)** |

Warning that would be shown to the engineer:

> Security matrix for stream **2.1.x / 2.2.x** was last updated on 2026-06-28 (148 days ago).
> The matrix may not reflect recent releases.
> Options: 1. Refresh now  2. Proceed anyway  3. Stop

Eval assumption: **Proceed anyway** (no refresh possible without git access). Note: releases
after 2.2.4 (2026-05-04) may exist and are not covered by this analysis — but because every
listed version already ships a non-vulnerable serde_json and later builds would not
normally downgrade, the conclusion is very unlikely to change.

## Step 0.5 / 0.8 – Jira Access and Assignment

Not executed (no external calls). Proposed actions are recorded in `triage-outcome.md`
(assign TC-8002 to the current user; transition New → Assigned).

## Step 1 – Extracted CVE Data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8002 | Issue |
| Issue type / Status | Vulnerability / **New** (full triage path) | Issue |
| CVE ID | **CVE-2026-28940** | Label + summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | **serde_json** | Description |
| Affected version range | **< 1.0.135** ("versions before 1.0.135") | Description |
| Fixed version | **1.0.135** | Description |
| Severity | CVSS 5.3 (Medium) | Description |
| Vulnerability | Stack overflow from unbounded recursion on deeply nested JSON input (DoS / process crash) | Description |
| Upstream fix PR | none provided in remote links | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk ; https://rustsec.org/advisories/RUSTSEC-2026-0019.html | Remote links / References |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 | Remote links |
| Due date | 2026-07-30 (already past as of 2026-11-23) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | none | Comment history |

All critical fields (CVE ID, library, affected range) parsed successfully.

### Stream scope resolution

Suffix `[rhtpa-2.2]` → stream **2.2.x** (matches Version Streams row
`git.example.com/rhtpa/rhtpa-release.0.4.z`). Issue is **scoped** to 2.2.x.
Per Rule 4, all supported streams (2.1.x and 2.2.x) are still analyzed for cross-stream impact.

### Ecosystem detection

serde_json is a Rust crate → **Cargo** (present in both streams' Ecosystem Mappings:
repo `backend`, lock file `Cargo.lock`, check command `git show <tag>:Cargo.lock`).
Category: source dependency.

### Deployment context

Affected repository: rhtpa-backend (backend) → deployment context **upstream** (default; column absent).

## Step 1.5 – External CVE Data Enrichment

MITRE (`https://cveawg.mitre.org/api/cve/CVE-2026-28940`) and OSV.dev
(`https://api.osv.dev/v1/vulns/CVE-2026-28940`) were **not queried** (eval forbids external calls).
Treated as "unavailable":

> External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.

Fix threshold used for Step 2: **serde_json < 1.0.135 affected; >= 1.0.135 fixed**.
(The margin is comfortable: the lowest shipped version is 1.0.137, so a small threshold
disagreement from an external source would not change the outcome.)

## Step 1.7 – Embargo Check

Skipped — no Embargo policy URL configured (and CVSS 5.3 < 7.0 threshold anyway).
