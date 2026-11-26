# Step 1 – Data Extraction: TC-8020

Source: mock issue `vuln-issue-standard.md` (simulated `jira.get_issue` + `jira.get_issue_remote_links`).
Note: the mock file's header shows key `TC-8001`; the eval task designates the issue as **TC-8020**, which is used throughout.

## Step 0 – Configuration validation (from claude-md-security-config.md)

| Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification field | customfield_12345 |
| Upstream Affected Component field | customfield_10632 (assumed configured per eval instructions) |
| PS Component / Stream fields | not configured (Step 4.3 would be skipped; Step 7 only needs the Upstream Affected Component field) |
| ProdSec contact / account ID | not configured (no @mentions) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| Version Streams | 2.1.x -> rhtpa-release.0.3.z; 2.2.x -> rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column -> defaults to `upstream`) |

All required sections present -> proceed.

**Step 0.3 – Matrix staleness:** `Last-Updated: 2026-06-28T10:00:00Z`; today is 2026-11-26 -> **151 days old** (> 14-day threshold). In an interactive run the engineer would be offered Refresh / Proceed / Stop. For this eval the mock matrix is used as-is (treated as "Proceed anyway").

**Step 0.6:** `FULLSEND_OUTPUT_DIR` absent -> interactive mode. **Step 0.8** (assign to current user, transition New -> Assigned) would be proposed; not executed (no Jira calls in this eval).

## Extracted fields

| Field | Value |
|---|---|
| Issue key | TC-8020 |
| CVE ID | CVE-2026-31812 (label + summary) |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Status | New (full triage path) |
| Affected component | `pscomponent:org/rhtpa-server` |
| Upstream Affected Component (customfield_10632) | quinn-proto |
| PSIRT-claimed product version | `[rhtpa-2.2]` |
| Affects Versions (Jira) | RHTPA 2.0.0 (does not correspond to any configured stream — incorrect) |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Weakness | Denial of service — unbounded stream allocation from crafted STREAMS frame causes panic |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Existing comments | none |

## Stream scope resolution

Suffix `[rhtpa-2.2]` -> stream **2.2.x** (matches configured stream, repo `rhtpa-release.0.4.z`). Issue is **scoped** to 2.2.x.

## Ecosystem / deployment context

- Ecosystem: **Cargo** (Rust crate) — listed in both streams' Ecosystem Mappings (`Cargo.lock`, repo `backend`).
- Category: source dependency -> 2 remediation tasks per affected stream.
- Repository: rhtpa-backend, deployment context `upstream` (default).

## Step 1.5 – External enrichment

Not performed (no external calls permitted in this eval). Jira description data used alone: fix threshold **0.11.14**, reduced confidence noted.

## Step 1.7 – Embargo check

No Embargo policy URL configured -> skipped (despite CVSS 7.5).

## Step 2 – Version impact (simulated `git show <tag>:Cargo.lock` from mock data)

| Stream | Version | Backend tag | quinn-proto | Affected (< 0.11.14)? |
|---|---|---|---|---|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES |
| **2.2.x** | **2.2.0** | v0.4.5 | 0.11.9 | **YES** |
| **2.2.x** | **2.2.1** | v0.4.8 | 0.11.12 | **YES** |
| **2.2.x** | **2.2.2** | v0.4.8 (retag) | same as 2.2.1 (0.11.12) | **YES** |
| **2.2.x** | **2.2.3** | v0.4.11 | 0.11.14 | NO |
| **2.2.x** | **2.2.4** | v0.4.12 | 0.11.14 | NO |

Development stream: not determinable (requires Jira unreleased-version lookup, not available in this eval).

Upstream fix status (2.5): the 2.2.x stream already ships quinn-proto 0.11.14 from v0.4.11 onward, so the fix is on `release/0.4.z`. 2.1.x (`release/0.3.z`) has no evidence of the fix.

## Step 3 – Affects Versions correction (proposed, scoped to 2.2.x)

`Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

2.1.x versions (also affected) belong to a companion/sibling issue or preemptive remediation (Case A), not this issue.
