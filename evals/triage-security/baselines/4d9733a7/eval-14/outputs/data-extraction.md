# Step 1 -- Data Extraction for TC-8005

## Step 0.7 -- Early Assignment

1. **Retrieve current user's Jira account ID**: `jira.user_info()`
2. **Assign TC-8005 to current user**: `jira.edit_issue("TC-8005", assignee=<current-user-account-id>)`
3. **Discover transitions**: `jira.get_transitions("TC-8005")` -- select transition with target status "Assigned"
4. **Transition to Assigned**: `jira.transition_issue("TC-8005", <assigned-transition-id>)` -- issue is currently in New status

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | < 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Upstream fix PR | N/A (RPM system package) |
| Advisory URL | RHSA-2026:4021 (https://access.redhat.com/errata/RHSA-2026:4021) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | None |

### Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` which maps to the **2.2.x** stream in Version Streams configuration. Triage is scoped to the 2.2.x stream.

### Ecosystem Detection

The vulnerable library `openssl-libs` is a system RPM package. The 2.2.x stream's Ecosystem Mappings table lists **RPM** as a supported ecosystem with Lock File `rpms.lock.yaml` and Check Command `git show <tag>:rpms.lock.yaml`. Ecosystem: **RPM**.
