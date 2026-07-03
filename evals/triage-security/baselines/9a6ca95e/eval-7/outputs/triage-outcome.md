# Triage Outcome -- Step 4.2 Pre-Existing Link Handling

## Summary

Step 4.2 (Cross-stream coordination) handled the pre-existing Related link to sibling TC-8001 through its **idempotent link creation** protocol. The link was not duplicated; creation was skipped because the existing link satisfied all matching criteria.

## How Step 4.2 Handled the Pre-Existing Link

### The Idempotent Check

Step 4.2 requires checking the current issue's `issuelinks` array (already fetched in Step 1's `jira.get_issue` call) before creating any new link. The check verifies whether an existing link satisfies **all** of these conditions:

1. `type.name` is `"Related"`
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key

### Application to TC-8006

TC-8006's `issuelinks` array contains a link with:
- `type`: Related
- `outwardIssue.key`: TC-8001
- Link ID: 1990401

Both conditions are met:
- Condition 1: type.name "Related" -- **matched**
- Condition 2: outwardIssue.key "TC-8001" matches sibling key TC-8001 -- **matched**

### Result

Because a matching link already exists, Step 4.2 **skipped link creation** and logged:

> "Related link to TC-8001 already exists -- skipping"

No `jira.create_link` call was made. This is the correct idempotent behavior -- re-running triage on an issue that already has its sibling links in place does not create duplicate links.

### Why This Matters

PSIRT or a prior triage run may have already linked companion issues. Without the idempotent check, each triage run would create an additional Related link between the same two issues, cluttering the issue's link section. The pre-existing link check ensures that Step 4.2 is safe to run multiple times on the same issue without side effects.

## Remaining Triage Flow

After Step 4.2 completed (with the link skip), the triage continues with:

- **Step 4.3** (Cross-CVE Overlap Detection): Skipped because Upstream Affected Component, PS Component, and Stream custom fields are not configured in Security Configuration.
- **Step 4.4** (Preemptive Task Reconciliation): No preemptive tasks found for CVE-2026-31812 in stream rhtpa-2.1.
- **Step 5** (Version Lifecycle Check): Verify that RHTPA 2.1.0 is still within its support lifecycle.
- **Step 6** (Already Fixed Check): TC-8001 is In Progress (not Closed/Done), so no already-fixed scenario applies.
- **Step 7** (Concurrent Triage Detection): Skipped because Upstream Affected Component custom field is not configured.
- **Step 8** (Remediation): Based on version impact analysis, determine whether to create remediation tasks (Case A), post cross-stream notice (Case B), or close as Not a Bug (Case C). Since quinn-proto 0.11.9 (shipped in RHTPA 2.1.0 and 2.1.1) is below the fix threshold of 0.11.14, all 2.1.x versions are affected, and remediation tasks would be needed (Case A). Because the ecosystem is Cargo (source dependency), two tasks would be created: an upstream backport task and a downstream propagation subtask.
