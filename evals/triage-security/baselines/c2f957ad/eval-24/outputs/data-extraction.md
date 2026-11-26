# TC-8001 — Step 1 Data Extraction

## Step 0 — Configuration (extracted from CLAUDE.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | not configured (Step 4.3 and Step 7 skipped) |
| ProdSec contact / account ID | not configured (no @mentions) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |

### Source Repositories mapping

The Source Repositories table has **no Deployment Context column**. For backward
compatibility, every repository defaults to `upstream`.

| Repository | URL | Deployment Context |
|---|---|---|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | `upstream` (default — column absent) |

Because the column is absent, the remediation tasks **leave out the Coordination
Guidance subsection** (see remediation-templates.md, "Coordination Guidance").

## Step 0.3 — Matrix Staleness Check

The matrix shows `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-26, so the
matrix is **151 days old**, well past the 14-day threshold.

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28
> (151 days ago). The matrix may not reflect recent releases.
> Options: 1. Refresh now  2. Proceed anyway  3. Stop

Eval mode: proceeding with the current matrix. Releases after 2.2.4 (2026-05-04) may
be missing from the analysis.

## Step 1 — Parsed CVE Data

| Field | Value |
|---|---|
| Issue key | TC-8001 |
| Status | New (full triage path) |
| CVE ID | CVE-2026-31812 (from label and summary) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Affected repository | rhtpa-backend (Ecosystem Mappings repository `backend`) |
| Deployment context | `upstream` (default — Deployment Context column absent) |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → stream **2.2.x** |
| Issue stream scope | **Scoped** to 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 (does not match the 2.2.x scope or the lock file evidence) |
| Vulnerable library | quinn-proto |
| Ecosystem | Cargo (source dependency → 2 tasks per stream) |
| Affected version range | < 0.11.14 ("versions before 0.11.14") |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Existing comments | none |

## Step 1.5 — External CVE Data Enrichment

MITRE and OSV were not queried, because the eval does not allow external calls.
Both are treated as unavailable:

> External CVE databases unavailable — using Jira description data only.
> Fix threshold confidence is reduced.

Fix threshold used: **quinn-proto < 0.11.14 is affected; 0.11.14 is fixed.**

## Step 1.7 — Embargo Check

CVSS is 7.5, which meets the threshold. **No Embargo policy URL is configured**, so the
step is skipped.

## Step 2 — Version Impact Table

Version impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Backend tag | quinn-proto | Affected? | Notes |
|---|---|---|---|---|---|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | outside issue scope |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | outside issue scope |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.8 | — | YES | same as 2.2.1 (backend retag) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | |
| dev stream | — | branch HEAD | not determined | — | No Jira version metadata, so the unreleased dev version cannot be found (no Jira calls allowed) |

**Dependency chain (Step 2.3.5):** The lock file data confirms that quinn-proto is
present. No Cargo.toml or manifest data was provided, so direct vs. transitive cannot
be determined. Profile: assumed to be production, since there is no evidence it is
dev-only, and no `dev-dependency` label is applied. The remediation tasks include both
the direct and transitive approaches. The engineer must confirm which applies.

**Upstream fix status (Step 2.5):** Branch HEAD could not be inspected, because the
eval allows no `git show`.

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|---|---|---|---|---|
| 2.2.x | Cargo | release/0.4.z | not inspected (released tag v0.4.12 already ships 0.11.14) | Likely YES (inferred from released tags, not verified) |
| 2.1.x | Cargo | release/0.3.z | not inspected (latest tag v0.3.12 ships 0.11.9) | Unknown / assumed NO |

## Step 3 — Affects Versions Correction (proposed)

- Current: RHTPA 2.0.0
- Proposed (scoped to 2.2.x): **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**
- Remove RHTPA 2.0.0. No 2.0.x stream is configured, and the issue is scoped to 2.2.x.
- 2.1.0 and 2.1.1 are also affected but are outside this issue's scope. They are
  handled by Case A (cross-stream comment and preemptive tasks).

## Steps 4–7

- Step 4: sibling JQL was not run. This eval assumes no sibling CVE-2026-31812 issue
  exists for 2.1.x. Step 4.3 is skipped because Upstream Affected Component is not
  configured.
- Step 5: the lifecycle page was not queried. 2.1.x and 2.2.x are assumed to be
  supported.
- Step 6: no resolved siblings, so the CVE is not already fixed.
- Step 7: skipped, because Upstream Affected Component is not configured.
- Step 7.5: release Jira lookup was not performed (no Jira access). Release Epic and
  Task linking is pending in an interactive run.
