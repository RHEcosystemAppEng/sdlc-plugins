# Step 0 -- Configuration Validation

Configuration extracted from CLAUDE.md:

| Parameter | Value |
|-----------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component custom field | _(not configured -- Step 4.3 and Step 7 skipped)_ |
| PS Component custom field | _(not configured)_ |
| Stream custom field | _(not configured)_ |
| ProdSec contact email | _(not configured)_ |
| ProdSec Jira account ID | _(not configured -- @mentions omitted)_ |
| Embargo policy URL | _(not configured -- Step 1.7 skipped)_ |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

Note: The Source Repositories table does NOT have a Deployment Context column.
Per backward compatibility rules, all repositories default to `upstream` for internal
routing, but the Coordination Guidance subsection is omitted entirely from remediation
task descriptions.

## Step 0.3 -- Matrix Staleness Check

Security matrix Last-Updated timestamp: 2026-06-28T10:00:00Z (4 days ago).
Within the 14-day freshness threshold. Proceeding without staleness warning.

## Step 0.7 -- Assign and Transition

**PROPOSAL**: Assign TC-8001 to current user and transition from New to Assigned status.

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Existing comments | _(no comments)_ |

## Stream Scope Resolution

Issue summary: "CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]"

Stream suffix `[rhtpa-2.2]` maps to configured Version Stream **2.2.x**
(Konflux release repo: rhtpa-release.0.4.z).

This issue is **scoped** to the 2.2.x stream. Steps 3 and 4 will apply only to
2.2.x versions. Cross-stream impact on 2.1.x will be handled via Case B.

## Ecosystem Detection

Vulnerable library: quinn-proto (Rust crate)
Detected ecosystem: **Cargo**

Ecosystem Mappings (from 2.2.x stream security-matrix.md):

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.4.z |

Ecosystem Mappings (from 2.1.x stream security-matrix.md):

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.3.z |

## Deployment Context

Source repository: rhtpa-backend
Deployment Context column: **absent** from Source Repositories table.
Per backward compatibility: default to `upstream` internally, but **omit Coordination
Guidance subsection** from all remediation task descriptions.

---

# Step 1.7 -- Embargo Check

Embargo policy URL is not configured in Security Configuration. Step 1.7 skipped.

---

# Step 2 -- Version Impact Analysis

## Supportability Matrix (aggregated)

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 | |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 | |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

## Dependency Version Extraction (quinn-proto)

Extracted from `git show <tag>:Cargo.lock` (simulated from mock data):

| Tag | quinn-proto version | vs. fix threshold (0.11.14) |
|-----|---------------------|-----------------------------|
| v0.3.8 | 0.11.9 | BELOW -- affected |
| v0.3.12 | 0.11.9 | BELOW -- affected |
| v0.4.5 | 0.11.9 | BELOW -- affected |
| v0.4.8 | 0.11.12 | BELOW -- affected |
| v0.4.9 | _(retag of v0.4.8)_ | same as v0.4.8 -- affected |
| v0.4.11 | 0.11.14 | AT threshold -- NOT affected |
| v0.4.12 | 0.11.14 | AT threshold -- NOT affected |

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | quinn-proto | Affected? | Notes |
|--------|---------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | 0.11.14 | NO | fix version shipped |
| 2.2.x | 2.2.4 | 0.11.14 | NO | fix version shipped |

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

Summary:
- **2.2.x**: Fix already present on release/0.4.z since v0.4.11. Versions 2.2.3+ ship
  the fixed quinn-proto 0.11.14. No new remediation action needed for this stream.
- **2.1.x**: Fix NOT present on release/0.3.z. All versions (2.1.0, 2.1.1) ship
  vulnerable quinn-proto 0.11.9. Upstream backport required.

---

# Step 3 -- Affects Versions Correction

## PROPOSAL: Correct Affects Versions on TC-8001

Issue is scoped to stream 2.2.x. Only 2.2.x versions are included in the correction.

Affected 2.2.x versions (from version impact table): RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

| | Current (PSIRT-assigned) | Proposed (lock-file evidence) |
|---|---|---|
| Affects Versions | RHTPA 2.0.0 | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

Rationale: PSIRT assigned "RHTPA 2.0.0" which does not exist in the supportability matrix.
Lock file analysis at pinned source commits confirms quinn-proto < 0.11.14 is present
in versions 2.2.0 (v0.4.5: 0.11.9), 2.2.1 (v0.4.8: 0.11.12), and 2.2.2 (retag of 2.2.1).
Versions 2.2.3+ ship quinn-proto 0.11.14 (the fix threshold) and are NOT affected.

PROPOSAL (Jira mutation -- requires engineer confirmation):
```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"name": "RHTPA 2.2.0"},
    {"name": "RHTPA 2.2.1"},
    {"name": "RHTPA 2.2.2"}
  ]
})
```

PROPOSAL (comment -- requires engineer confirmation):
```
jira.add_comment("TC-8001", "Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
RHTPA 2.0.0 does not exist in the supportability matrix.
Versions 2.2.3+ ship quinn-proto 0.11.14 (fixed) and are excluded.")
```

---

# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

## Step 4.1/4.2 -- Sibling Search

PROPOSAL (JQL query):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001
```

_(In this eval, no sibling issues are known. In a real triage, this query would
be executed to find companion CVE Jiras for the 2.1.x stream.)_

## Step 4.3 -- Cross-CVE Overlap Detection

Upstream Affected Component custom field is NOT configured in Security Configuration.
**Step 4.3 skipped entirely.**

## Step 4.4 -- Preemptive Task Reconciliation

PROPOSAL (JQL query):
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

_(In this eval, no preemptive tasks are known. Proceeding to Step 5.)_

---

# Step 7 -- Concurrent Triage Detection

Upstream Affected Component custom field is NOT configured in Security Configuration.
**Step 7 skipped entirely.**

---

# Triage Outcome Summary

## Stream 2.2.x (scoped stream)

- **Affected versions**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Fix status**: Already fixed starting from RHTPA 2.2.3 (build 0.4.11, quinn-proto 0.11.14)
- **Upstream fix**: Present on release/0.4.z
- **Remediation**: No new remediation tasks needed -- fix already shipped in current versions.

## Stream 2.1.x (cross-stream impact -- Case B)

- **Affected versions**: RHTPA 2.1.0, RHTPA 2.1.1 (all versions in stream)
- **Fix status**: NOT fixed
- **Upstream fix**: NOT present on release/0.3.z (latest tag v0.3.12 has quinn-proto 0.11.9)
- **Remediation**: Preemptive remediation tasks required (no CVE Jira exists for 2.1.x stream)
- See outputs/remediation.md for task descriptions

## Post-Triage Actions

PROPOSAL: Add `ai-cve-triaged` label to TC-8001.

PROPOSAL: Post summary comment to TC-8001 documenting version impact, Affects Versions
correction, cross-stream impact on 2.1.x, and preemptive remediation tasks created.
