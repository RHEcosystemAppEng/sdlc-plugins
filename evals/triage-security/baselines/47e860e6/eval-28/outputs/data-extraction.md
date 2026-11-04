# Step 1 – Data Extraction: TC-8060

Eval mode: Jira, MITRE, OSV and git were **not** called. All values come from the fixture files
(`vuln-issue-transitive.md`, `security-matrix-mock.md`, `claude-md-security-config.md`).

## Step 0 – Configuration validation

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | not configured (Step 4.3 cross-CVE overlap and Step 7 concurrent triage skipped) |
| ProdSec contact / account ID | not configured (no @mention of ProdSec) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend → https://github.com/rhtpa/rhtpa-backend (no Deployment Context column, so it defaults to `upstream`) |

All required sections are present, so the configuration check passes.

## Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8060 | Issue |
| Issue type / Status | Vulnerability / New | Issue |
| CVE ID | CVE-2026-99010 | Label `CVE-2026-99010` and summary |
| Summary | CVE-2026-99010 h2 - Memory exhaustion via CONTINUATION frames [rhtpa-2.2] | Issue |
| Affected component | `pscomponent:org/rhtpa-server` → rhtpa-backend (`backend` repo in matrix) | Component label |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → 2.2.x stream | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | `versions` field |
| Vulnerable library | h2 (Rust crate) | Description |
| Ecosystem | Cargo (source dependency, so 2 tasks per stream) | Library + Ecosystem Mappings |
| Affected version range | < 0.4.5 ("versions before 0.4.5") | Description |
| Fixed version | 0.4.5 | Description |
| Severity | CVSS 7.5 (High), DoS | Description |
| Dependency type | **Transitive**: backend → reqwest → hyper → h2 (3 levels deep) | Fixture dependency-chain data (Step 2.3.5) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | none (no GHSA link present) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99010 | Remote links |
| Due date | 2026-08-15 | `duedate` |
| Assignee | Unassigned | Issue |
| Reporter | psirt-analyst (account ID `557058:psirt-analyst-mock-id`) | Issue (used for the mandatory @mention in the summary comment) |
| Existing comments | none | Issue |
| Deployment context | column absent, so it defaults to `upstream`; the Coordination Guidance subsection is left out of the tasks per remediation-templates.md | Source Repositories |

## Stream scope resolution

- Suffix `[rhtpa-2.2]` → stream **2.2.x** → Konflux repo `git.example.com/rhtpa/rhtpa-release.0.4.z`.
- The issue is **scoped** to 2.2.x. Steps 3, 4 and 8 operate on 2.2.x only. 2.1.x is analyzed only for the Case A cross-stream check.

## Step 1.5 – External CVE enrichment

MITRE and OSV were not queried because this is an eval with no external calls. Both are treated as unavailable.

> External CVE databases unavailable. Using Jira description data only. Fix threshold confidence is reduced.

The fix threshold used for Step 2 is **h2 < 0.4.5 affected, 0.4.5 fixed**.

## Step 1.7 – Embargo check

Skipped because no Embargo policy URL is configured. CVSS 7.5 would otherwise have triggered the gate.

## Step 0.8 – Assign / transition (proposed, not executed)

- Assign TC-8060 to the current triager.
- Transition New → Assigned, using a transition discovered dynamically via `get_transitions`.
