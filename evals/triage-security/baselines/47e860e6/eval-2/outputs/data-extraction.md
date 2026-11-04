# TC-8002 — Data Extraction (Step 0 – Step 1.7)

## Step 0 – Configuration validation

Source: `claude-md-security-config.md` (mock project CLAUDE.md).

| Required section | Present? | Values used |
|---|---|---|
| Repository Registry | Yes | rhtpa-backend (serena_backend) |
| Jira Configuration | Yes | Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Code Intelligence | Yes | `mcp__serena_backend__<tool>` |
| Security Configuration → Product Lifecycle | Yes | Product pages URL `https://access.example.com/product-life-cycle/rhtpa`, Jira version prefix `RHTPA`, Vulnerability issue type ID `10024`, Component label pattern `pscomponent:` |
| Security Configuration → Version Streams | Yes | 2.1.x → `rhtpa-release.0.3.z`; 2.2.x → `rhtpa-release.0.4.z` |
| Security Configuration → Source Repositories | Yes | rhtpa-backend (`https://github.com/rhtpa/rhtpa-backend`) |

Optional fields:

| Field | Status |
|---|---|
| VEX Justification custom field | Configured: `customfield_12345` |
| Upstream Affected Component / PS Component / Stream custom fields | Not configured, so Step 4.3 (cross-CVE overlap) and Step 7 (concurrent triage) are skipped |
| ProdSec contact email / Jira account ID | Not configured, so no ProdSec @mentions |
| Embargo policy URL | Not configured, so Step 1.7 is skipped |
| Source repo Deployment Context column | Absent, so default is `upstream` |

Configuration is valid. Triage proceeds.

## Step 0.3 – Matrix staleness check

| Stream | Last-Updated | Age (today = 2026-11-04) | Status |
|---|---|---|---|
| 2.1.x (rhtpa-release.0.3.z) | 2026-06-28T10:00:00Z | 129 days | STALE (threshold 14 days) |
| 2.2.x (rhtpa-release.0.4.z) | 2026-06-28T10:00:00Z | 129 days | STALE (threshold 14 days) |

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28
> (129 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now  2. Proceed anyway  3. Stop

In interactive mode this choice goes to the engineer. For this eval, refreshing is not possible because external calls are not allowed. Triage continues with **Proceed anyway**. Any 2.2.x release after 2.2.4 (2026-05-04) is not in the matrix and must be checked before closure (see triage-outcome.md).

## Step 0.6 – Mode detection

`FULLSEND_OUTPUT_DIR` is not set, so this is **interactive mode**. Jira mutations are proposed in writing only and are not executed (eval constraint).

## Step 0.8 – Assign and transition (proposed)

- Assign TC-8002 to the current triager (account ID from `jira.user_info()`).
- Status is **New**, so transition to **Assigned** using the transition target discovered dynamically with `jira.get_transitions(TC-8002)`. No hard-coded ID.

## Step 1 – Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8002 | Issue |
| Issue type / Status | Vulnerability / New | Issue |
| CVE ID | **CVE-2026-28940** | Label `CVE-2026-28940` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Affected repository | rhtpa-backend (backend, Cargo) | Component mapped through the matrix "backend" column |
| Deployment context | `upstream` (default, column absent) | Source Repositories |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Issue stream scope | **2.2.x** (scoped) | `[rhtpa-2.2]` matches Version Stream 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | **serde_json** | Description |
| Ecosystem | **Cargo** (Rust crate), a source dependency | Library and Ecosystem Mappings (Cargo → `Cargo.lock`) |
| Affected version range | **< 1.0.135** ("versions before 1.0.135") | Description |
| Fixed version | **1.0.135** | Description |
| Vulnerability | Stack overflow from unbounded recursion when deserializing deeply nested JSON. The fix adds a recursion limit, default 128. | Description |
| CVSS | 5.3 (Medium) | Description |
| Upstream fix PR | None in remote links | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk (also RUSTSEC-2026-0019: https://rustsec.org/advisories/RUSTSEC-2026-0019.html) | Remote links / References |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 | Remote links |
| Due date | 2026-07-30 (already past as of 2026-11-04) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | None | Issue |

All critical fields (CVE ID, library, affected range) were parsed. No engineer input is needed.

## Step 1.5 – External CVE data enrichment

MITRE (`https://cveawg.mitre.org/api/cve/CVE-2026-28940`) and OSV.dev (`https://api.osv.dev/v1/vulns/CVE-2026-28940`) were **not queried** because this eval does not allow external calls.

> External CVE databases unavailable, so only Jira description data is used. Fix threshold confidence is reduced.

Fix threshold used for Step 2: **serde_json < 1.0.135 is affected; 1.0.135 and later are fixed.**

## Step 1.7 – Embargo check

Skipped. No Embargo policy URL is configured. CVSS 5.3 (Medium) is also below the 7.0 threshold.
