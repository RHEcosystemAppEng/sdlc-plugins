# Step 0.7 — Early Assignment

Before extracting CVE data, assign and transition the Vulnerability issue:

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info()
   ```

2. **Assign TC-8040 to the current user:**
   ```
   jira.edit_issue("TC-8040", assignee=<current-user-account-id>)
   ```

3. **Discover the target transition dynamically:**
   ```
   jira.get_transitions("TC-8040")
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8040", <assigned-transition-id>)
   ```

---

# Step 1 — Data Extraction

**Issue**: TC-8040

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| CVSS | 7.5 (High) |
| Existing comments | (none) |

### Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the configured **2.2.x** Version Stream. Triage is scoped to the 2.2.x stream.

### Ecosystem Detection

The vulnerable library and component context resolve to ecosystem: **Go modules**.

**Ecosystem Mappings check**: The 2.2.x stream's security-matrix.md Ecosystem Mappings table lists the following ecosystems:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**Result**: The detected ecosystem **Go modules** is NOT present in the Ecosystem Mappings table. The supported ecosystems for stream 2.2.x are: Cargo, RPM.

Automated triage cannot proceed for an unsupported ecosystem. See `outputs/unsupported-ecosystem.md` for the notification presented to the user.
