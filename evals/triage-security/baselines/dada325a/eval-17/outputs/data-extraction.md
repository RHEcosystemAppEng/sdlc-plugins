# Step 1 – Data Extraction: TC-8001

## Step 0 – Configuration (validated)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Embargo policy URL | https://example.com/security/embargo-policy (configured — Step 1.7 is active) |
| Upstream Affected Component field | not configured (Step 4.3 and Step 7 skipped) |
| ProdSec Jira account ID | not configured (no @mentions in correction comments) |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend); no Deployment Context column → defaults to `upstream`, coordination guidance omitted (backward compatibility rule) |

### Step 0.3 – Matrix Staleness Check

Both stream matrices carry `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is
2026-11-06, which is **131 days** old (threshold: 14 days).

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28
> (131 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** — re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** — continue triage with the current matrix
> 3. **Stop** — halt triage so I can investigate

Eval simulation: **Proceed anyway** (no external access available for a refresh).
Any 2.1.x/2.2.x releases after 2026-06-28 are NOT covered by this analysis.

### Step 0.6 – Mode

`FULLSEND_OUTPUT_DIR` absent → interactive mode (Jira mutations simulated in files only).

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Jira issue | TC-8001 | Issue key |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Ecosystem | Cargo (Rust crate) — source dependency | Library name + Ecosystem Mappings (Cargo → backend, `Cargo.lock`) |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS / Severity | 7.5 (High) | Description |
| Vulnerability type | Denial of service — panic on excessive stream count in QUIC STREAMS frame | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) | Remote links / description references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (already past as of 2026-11-06) | Issue `duedate` |
| Status | New | Issue status → full triage path |
| Assignee | Unassigned | Step 0.8 would assign to current user + transition to Assigned (simulated, not executed) |
| Existing comments | none | Comment history |

## Stream Scope Resolution

- Summary suffix `[rhtpa-2.2]` → matches configured Version Stream **2.2.x**
  (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- Issue is **scoped** to 2.2.x. Other streams (2.1.x) are analysed for
  cross-stream impact (Case A).
- Note: the Jira Affects Versions field (RHTPA 2.0.0) does not match either the
  summary suffix or any configured stream — this is a PSIRT mismatch to be corrected
  in Step 3.

## Deployment Context

Ecosystem Mappings map Cargo to repository `backend` → Source Repository
`rhtpa-backend`. The Source Repositories table has no Deployment Context column, so
the context defaults to `upstream` and the Coordination Guidance subsection is omitted
from remediation tasks.

## Step 1.5 – External CVE Data Enrichment

Not executed (eval restriction: no external calls to MITRE CVE API / OSV.dev).

> ⚠ External CVE databases unavailable — using Jira description data only.
> Fix threshold confidence is reduced.

Fix threshold used for Step 2: **quinn-proto < 0.11.14 affected; 0.11.14 fixed**.
