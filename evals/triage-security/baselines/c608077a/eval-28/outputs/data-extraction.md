# TC-8060 — Step 1 Data Extraction

Skill: `/sdlc-workflow:triage-security` (run in interactive mode, `FULLSEND_OUTPUT_DIR` not set). This is an eval run, so Jira, git, and external lookups were simulated from the fixture files and no live calls were made.

## Step 0 – Configuration validation (from claude-md-security-config.md)

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | not configured, so Step 4.3 (cross-CVE overlap) and Step 7 (concurrent triage) are skipped |
| Embargo policy URL | not configured, so Step 1.7 is skipped |
| ProdSec contact / account ID | not configured, so @mentions are skipped |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend). The Deployment Context column is missing, so the context defaults to `upstream` and coordination guidance is left out (backward compatibility). |

All required sections are present (Repository Registry, Jira Configuration, Code Intelligence, Security Configuration). The skill continues.

## Step 0.3 – Matrix staleness check

The matrix has `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. Today is 2026-11-20, so it is **145 days old**, which is past the 14-day limit.

> Security matrix for streams **2.1.x / 2.2.x** was last updated on 2026-06-28 (145 days ago). The matrix may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

Eval assumption: the run uses **Proceed anyway**. Any release after 2.2.4 (2026-05-04) is missing from this analysis.

## Step 0.8 – Assign / transition (proposed only)

- Proposed: assign TC-8060 to the current triager and move it from New to Assigned. The Assigned transition must be found dynamically. Not executed, because Jira is not called in this eval.

## Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8060 | Issue |
| Issue status | New (full triage path) | Issue |
| CVE ID | CVE-2026-99010 | Label `CVE-2026-99010` and summary |
| Summary | CVE-2026-99010 h2 - Memory exhaustion via CONTINUATION frames [rhtpa-2.2] | Issue |
| Affected component | `pscomponent:org/rhtpa-server` → rhtpa-backend (`backend` in the Ecosystem Mappings) | Labels |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` |
| Vulnerable library | h2 (Rust crate) | Description |
| Ecosystem | Cargo (source dependency, so 2 remediation tasks per stream) | Library + Ecosystem Mappings |
| Affected version range | < 0.4.5 ("versions before 0.4.5") | Description |
| Fixed version | 0.4.5 | Description |
| Severity | CVSS 7.5 (High), denial of service | Description |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | none (no GHSA or advisory remote link) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99010 | Remote links |
| Due date | 2026-08-15 (**already past** as of 2026-11-20) | `duedate` |
| Reporter | psirt-analyst (account ID `557058:psirt-analyst-mock-id`) | Issue |
| Assignee | Unassigned | Issue |
| Existing comments | none | Issue |
| Deployment context | upstream (default, column missing) | Source Repositories |

### Stream scope resolution

- The suffix `[rhtpa-2.2]` maps to the configured Version Stream **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x.** Steps 2–8 are scoped to this stream. Other streams are only checked for cross-stream impact (Case A).

## Step 1.5 – External CVE data enrichment

MITRE (`cveawg.mitre.org/api/cve/CVE-2026-99010`) and OSV.dev (`api.osv.dev/v1/vulns/CVE-2026-99010`) were **not queried**, because external tools are disallowed in this eval.

> ⚠ External CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced.

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | < 0.4.5 | 0.4.5 |
| MITRE CVE API | unavailable | unavailable |
| OSV.dev | unavailable | unavailable |

**Fix threshold used in Step 2: h2 < 0.4.5 is affected; 0.4.5 and later are fixed.**

## Step 1.7 – Embargo check

Skipped. No Embargo policy URL is configured. The CVSS of 7.5 would otherwise meet the warning threshold.
