# Step 0.7 -- Early Assignment

**Proposed actions** (require confirmation before execution):

1. **Assign TC-8050 to the current user:**
   ```
   jira.edit_issue("TC-8050", assignee=<current-user-account-id>)
   ```

2. **Transition TC-8050 to Assigned status:**
   - Retrieve available transitions: `jira.get_transitions("TC-8050")`
   - Select the transition whose target status name is "Assigned"
   - Execute: `jira.transition_issue("TC-8050", <assigned-transition-id>)`

   The issue is currently in **New** status, so the transition proceeds.

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99001 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | criterion |
| Affected version range | < 0.5.2 |
| Fixed version | 0.5.2 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | Not provided |
| Advisory URL | Not provided |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 |
| Due date | 2026-08-01 |
| Existing comments | None |
| Reporter | (from Jira issue reporter field) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the
**2.2.x** stream in the Version Streams table. Triage is **scoped to the 2.2.x
stream only**.

## Ecosystem Detection

The vulnerable library `criterion` is a Rust crate. The 2.2.x stream's
Ecosystem Mappings table includes **Cargo** as a configured ecosystem.

- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)
- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock`
- **Upstream Branch**: `release/0.4.z`

## Deployment Context Lookup

The Source Repositories table does not include a Deployment Context column.
Per backward compatibility rules, all repositories default to `upstream`.

- **Repository**: rhtpa-backend
- **Deployment context**: upstream (default -- no Deployment Context column)
