# Triage Outcome -- TC-8006

## Step 4.2 Pre-existing Link Handling

### Summary

Step 4 detected sibling TC-8001 as a **different-stream companion** (stream [rhtpa-2.2]) for the current issue TC-8006 (stream [rhtpa-2.1]). This is expected -- PSIRT creates one Vulnerability issue per stream to track the same CVE independently.

### Idempotent link check result

Step 4.2 inspected TC-8006's existing `issuelinks` array before attempting to create a "Related" link to TC-8001. The check found:

- A pre-existing "Related" link from TC-8006 to TC-8001 (Link ID: 1990401, direction: outward)

Because this link satisfies all conditions (`type.name` == "Related" AND `outwardIssue.key` == "TC-8001"), link creation was **skipped**.

**Related link to TC-8001 already exists -- skipping.**

No call to `jira.create_link()` was made. This idempotent behavior prevents duplicate links from being created when the same triage is run multiple times or when links were established by prior triage activity.

### What the idempotent check does and does not affect

- **Affected**: Link creation only. The `jira.create_link()` call is skipped when a matching link already exists.
- **Not affected**: The sibling landscape table is still presented to the engineer. The engineer retains full visibility into all companion issues across streams, regardless of whether links needed to be created or were already in place.

## Overall triage flow

The triage for TC-8006 proceeds through the standard steps:

1. **Step 0**: Configuration validated -- project key TC, Security Configuration present.
2. **Step 0.8**: Assign TC-8006 to current user, transition to Assigned status (proposed).
3. **Step 1**: Data extracted -- CVE-2026-31812, quinn-proto, affected range < 0.11.14, fixed version 0.11.14, ecosystem Cargo, scoped to stream 2.1.x.
4. **Step 4**: Sibling check found TC-8001 (stream 2.2.x, In Progress). Classified as different-stream companion. Pre-existing "Related" link detected -- link creation skipped. Sibling landscape presented. No same-stream duplicates found. No cross-CVE overlap check (Upstream Affected Component field not configured). No preemptive task reconciliation needed.
5. **Steps 5-8**: Would continue with version lifecycle check, already-fixed check, concurrent triage detection, release Jira orchestration, and remediation task creation for the 2.1.x stream (both versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9, which is within the affected range < 0.11.14).

### Version impact summary (for context)

Based on the security-matrix mock data, the 2.1.x stream versions are:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 0.11.9 | YES | < 0.11.14 |

Both supported versions in the 2.1.x stream ship a vulnerable version of quinn-proto. Remediation tasks would be created (Case B -- 2 tasks for Cargo ecosystem: upstream backport on release/0.3.z + downstream propagation to rhtpa-release.0.3.z).

### Cross-stream impact

This is a scoped issue ([rhtpa-2.1]). The version impact analysis of the 2.2.x stream (via TC-8001, the companion issue) shows that 2.2.x versions 2.2.0 and 2.2.1 are also affected, but versions 2.2.3 and 2.2.4 ship the fix. Since TC-8001 already exists and is In Progress for the 2.2.x stream, no preemptive remediation tasks are needed for that stream. A cross-stream impact comment would note that TC-8001 is already tracking the 2.2.x remediation.
