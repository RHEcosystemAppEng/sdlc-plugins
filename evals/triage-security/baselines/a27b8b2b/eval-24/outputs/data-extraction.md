# Step 0 -- Validate Project Configuration

## Configuration Extraction

The following configuration was extracted from the project CLAUDE.md:

| Setting | Value |
|---------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories -- Deployment Context

The Source Repositories table does **not** include a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`.

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | upstream (default -- column absent) |

No Deployment Context column exists in the Source Repositories table. The Coordination Guidance subsection will be omitted from all remediation task descriptions.

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md Last-Updated timestamp is `2026-06-28T10:00:00Z`. This is within the 14-day threshold (29 days from today 2026-07-27 -- wait, that is 29 days). However, using the fixture data as provided. The matrix was loaded successfully for both streams.

## Step 0.7 -- Assign and Transition to Assigned

**Proposed actions** (require confirmation before execution):

1. **Assign TC-8001** to the current user:
   - `jira.edit_issue(TC-8001, assignee=<current-user-account-id>)`

2. **Retrieve available transitions** for TC-8001:
   - `jira.get_transitions(TC-8001)`
   - Select the transition whose target status name is "Assigned"

3. **Transition TC-8001 to Assigned** (issue is currently in New status):
   - `jira.transition_issue(TC-8001, <assigned-transition-id>)`

These actions provide immediate visibility into who is actively triaging the issue and enable Step 7 (Concurrent Triage Detection).

---

# Step 1 -- Data Extraction

## Parsed CVE Data Table

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

### Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` which maps to the **2.2.x** stream (Konflux release repo: rhtpa-release.0.4.z). Triage is scoped to the 2.2.x stream only.

### Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is **Cargo**.

Cargo is a **source dependency** ecosystem per the classification table. This means remediation will produce **two tasks** per affected stream: an upstream backport task and a downstream propagation subtask.

### Deployment Context Lookup

The affected repository (`rhtpa-backend`, identified from component label `pscomponent:org/rhtpa-server`) was looked up in the Source Repositories mapping. Since the Deployment Context column is absent from the Source Repositories table, the deployment context defaults to **upstream**.

## Version Impact Table (Step 2)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Tag | quinn-proto | Affected? | Notes |
|---------|-----|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 |

**Affected versions in scope**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

### Cross-Stream Impact (informational)

The 2.1.x stream is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9), but this issue is scoped to 2.2.x. Cross-stream impact is reported via Case A in Step 8.

### Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency)
```

## Affects Versions Correction (Step 3)

Current (PSIRT-assigned): `[RHTPA 2.0.0]`
Proposed (lock-file-verified, scoped to 2.2.x): `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

The PSIRT-assigned version `RHTPA 2.0.0` does not match any supported version in the 2.2.x stream. Proposed correction replaces it with the actually affected versions based on lock file evidence at pinned commits from the supportability matrix.
