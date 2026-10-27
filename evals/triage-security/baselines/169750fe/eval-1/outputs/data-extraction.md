# Step 0.7 -- Early Assignment Actions

## Proposed Actions (not executed)

**Issue**: TC-8001
**Current Status**: New
**Current Assignee**: Unassigned

### Action 1: Assign to Current User

Assign TC-8001 to the current user (the triaging engineer). This provides
immediate visibility into who is actively triaging the issue.

```
jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
```

Proposed operation: `jira.user_info()` to retrieve the current user's Jira
account ID, then `jira.edit_issue("TC-8001", assignee=<account-id>)`.

### Action 2: Transition to Assigned

Transition TC-8001 from "New" to "Assigned" status.

```
jira.get_transitions("TC-8001")  -- discover the transition ID for "Assigned"
jira.transition_issue("TC-8001", <assigned-transition-id>)
```

The issue is currently in "New" status, so the transition to "Assigned" should
proceed. The transition ID is discovered dynamically via `get_transitions`,
not hardcoded.

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

- Parsed suffix: `rhtpa-2.2` maps to stream **2.2.x**
- Matched to Version Streams table entry: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`
- **Issue stream scope**: 2.2.x

## Ecosystem Detection

- **Library**: quinn-proto (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- **Remediation tasks per stream**: 2 (upstream backport or dependency bump + downstream propagation)

### Ecosystem Mappings (from security-matrix.md)

**Stream 2.1.x:**

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**Stream 2.2.x:**

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

## Deployment Context

- **Repository**: rhtpa-backend
- **Deployment context**: upstream (default -- no Deployment Context column in Source Repositories table)

## Configuration Extracted (Step 0)

| Setting | Value |
|---------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | Not configured |
| PS Component field | Not configured |
| Stream custom field | Not configured |
| ProdSec contact email | Not configured |
| ProdSec Jira account ID | Not configured |
| Embargo policy URL | Not configured (Step 1.7 skipped) |
