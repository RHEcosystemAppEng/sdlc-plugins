# Step 0.7 -- Early Assignment

**Proposed actions** (not executed -- eval mode):

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-8005 to the current user:
   ```
   jira.edit_issue("TC-8005", assignee=<current-user-account-id>)
   ```
3. Discover the "Assigned" transition dynamically:
   ```
   jira.get_transitions("TC-8005")
   ```
   Select the transition whose target status name is "Assigned".
4. Transition TC-8005 from New to Assigned:
   ```
   jira.transition_issue("TC-8005", <assigned-transition-id>)
   ```

# Step 1 -- Data Extraction

## Parsed CVE Data Table

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Upstream fix PR | N/A (RPM advisory) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library is **openssl-libs**, which is a system-level RPM package (not a Cargo crate or npm package). Checking the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

The **RPM** ecosystem is listed in the Ecosystem Mappings table. The ecosystem is identified as **RPM** based on the library name (openssl-libs is a system-level RPM package, not a source-level crate) and the component context (container image dependency).

## Deployment Context Lookup

The affected repository identified from the component label `pscomponent:org/rhtpa-server` is `rhtpa-backend`. Checking the Source Repositories table: rhtpa-backend is listed but no Deployment Context column exists, so it defaults to `upstream`.
