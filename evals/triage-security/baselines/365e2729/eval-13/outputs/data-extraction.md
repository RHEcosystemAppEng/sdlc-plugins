# Step 1 – Data Extraction: TC-8001

Mode: interactive (FULLSEND_OUTPUT_DIR absent). Eval simulation, so no Jira, Git or WebFetch calls were made. All values come from the provided input files.

## Step 0 – Configuration validation (claude-md-security-config.md)

| Item | Value | Status |
|---|---|---|
| Repository Registry | rhtpa-backend (serena_backend) | OK |
| Project key | TC | OK |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 | OK |
| Code Intelligence | `mcp__<serena-instance>__<tool>` naming convention | OK |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa | OK |
| Jira version prefix | RHTPA | OK |
| Vulnerability issue type ID | 10024 | OK |
| Component label pattern | `pscomponent:` | OK |
| VEX Justification field | customfield_12345 | Optional, configured |
| Upstream Affected Component field | not configured | Steps 4.3 and 7 are skipped |
| ProdSec Jira account ID | not configured | @mentions are skipped |
| Embargo policy URL | not configured | Step 1.7 is skipped |
| Version Streams | 2.1.x → rhtpa-release.0.3.z, 2.2.x → rhtpa-release.0.4.z | OK |
| Source Repositories | rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) | OK |

## Step 0.3 – Matrix staleness

The matrix has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-26, so the matrix is about 151 days old, well past the 14-day threshold.
> Security matrix for streams 2.1.x and 2.2.x was last updated on 2026-06-28 (151 days ago). It may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

For this eval: **Proceed anyway** with the current matrix.

## Step 0.8 – Assign and transition (planned, not executed)

- `jira.user_info()` → `jira.edit_issue(TC-8001, assignee=<current-user>)`
- `jira.get_transitions(TC-8001)` → select the transition whose target status is "Assigned". The status is currently New, so transition it.

## Extracted CVE data

| Field | Value | Source |
|---|---|---|
| Issue key | TC-8001 | Issue |
| Issue type / Status | Vulnerability / New | Issue |
| CVE ID | CVE-2026-31812 | Label `CVE-2026-31812` and summary |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field. **Suspect, because no 2.0.x stream exists** |
| Vulnerable library | quinn-proto | Description |
| Ecosystem | Cargo (Rust crate) → source dependency | Library + Ecosystem Mappings |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description |
| Fixed version | 0.11.14 | Description |
| CVSS / Severity | 7.5 (High) | Description |
| Vulnerability class | Denial of service (panic from unbounded stream allocation in a STREAMS frame) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Other references | https://rustsec.org/advisories/RUSTSEC-2026-0042.html | Description |
| Due date | 2026-07-15 | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | none | Comment history |
| Affected repository | rhtpa-backend (Ecosystem Mappings repository `backend`) | Component + matrix |
| Deployment context | upstream (default, because the column is absent) | Source Repositories |

## Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to the configured Version Stream **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x** (scoped issue). The 2.1.x stream is outside this issue's scope and is handled through Case A cross-stream logic.

## Step 1.5 – External CVE enrichment

- MITRE (`https://cveawg.mitre.org/api/cve/CVE-2026-31812`) and OSV (`https://api.osv.dev/v1/vulns/CVE-2026-31812`) were not queried, because the eval forbids external calls.
> External CVE databases unavailable — using Jira description data only. Fix threshold confidence is reduced.
- Fix threshold used: **quinn-proto < 0.11.14 is affected, and 0.11.14 is fixed**.

## Step 1.7 – Embargo check

Skipped. No Embargo policy URL is configured. CVSS is 7.5 and would otherwise meet the threshold.
