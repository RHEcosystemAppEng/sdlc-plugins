# Triage Outcome -- TC-8006 (CVE-2026-31812)

## Step 4.2 Pre-Existing Link Handling

The central question for this eval case is how Step 4.2 handles a pre-existing "Related" link to a cross-stream sibling.

### Methodology Requirement (from jira-triage-operations.md, Step 4.2)

The methodology specifies an idempotent link creation process:

> 1. **Check for existing link** before creating one. Read the current issue's
>    `issuelinks` array from the `jira.get_issue` response (already fetched in
>    Step 1). Check if any existing link satisfies all of:
>    - `type.name` is `"Related"`
>    - `inwardIssue.key` or `outwardIssue.key` matches the sibling key
>
>    If a matching link exists, skip link creation and log:
>    > "Related link to [sibling-key] already exists -- skipping"
>
>    If no matching link exists, create the link.

### What Happened

TC-8006 already has a "Related" link to TC-8001 (Link ID: 1990401, direction: outward). When Step 4.2 processed sibling TC-8001:

1. The skill checked TC-8006's `issuelinks` array (fetched in Step 1 Data Extraction).
2. Found an existing link where:
   - `type.name` = "Related" -- matches the required type
   - `outwardIssue.key` = "TC-8001" -- matches the sibling key
3. Both conditions are satisfied, so the link already exists.
4. **Result: Link creation was skipped.** The skill logged: "Related link to TC-8001 already exists -- skipping"

No duplicate link was created. The methodology's idempotency check prevented a redundant `jira.create_link` call. This is the correct behavior -- the skill must check for existing links before creating new ones to avoid duplicate links on the issue.

### Why This Matters

Without the idempotency check, the skill would attempt to create a second "Related" link to TC-8001, which could either:
- Fail with a Jira API error (duplicate link)
- Create a redundant link, cluttering the issue

The Step 4.2 methodology explicitly guards against this by requiring a pre-check of the `issuelinks` array before any link creation.

## Overall Triage Summary

| Step | Result |
|------|--------|
| Step 1 (Data Extraction) | CVE-2026-31812, quinn-proto < 0.11.14, stream 2.1.x, Cargo ecosystem |
| Step 2 (Version Impact) | 2.1.0 (0.11.9 - YES), 2.1.1 (0.11.9 - YES) -- both affected |
| Step 3 (Affects Versions) | PSIRT set RHTPA 2.1.0 only; should add RHTPA 2.1.1 (if it exists in Jira) |
| Step 4.1 (Duplicates) | No same-stream duplicates |
| Step 4.2 (Cross-stream) | Sibling TC-8001 (2.2.x, In Progress) -- pre-existing Related link found, skipped link creation |
| Step 4.3 (Cross-CVE Overlap) | Skipped -- required custom fields not configured |
| Step 4.4 (Preemptive Reconciliation) | No preemptive tasks found |
| Step 5 (Lifecycle) | Would check product pages URL for EOL status |
| Step 6 (Already Fixed) | TC-8001 is In Progress (not resolved) -- no already-fixed scenario |
| Step 7 (Remediation) | Case A: Both 2.1.x versions affected -- create remediation tasks (upstream Cargo backport + downstream propagation) |

## Remediation Recommendation (Step 7, Case A)

Since both versions in the 2.1.x stream are affected (quinn-proto 0.11.9 < fix threshold 0.11.14), remediation tasks would be created:

1. **Upstream backport task**: Bump quinn-proto to >= 0.11.14 in the backend repository on branch `release/0.3.z`
2. **Downstream propagation subtask**: Update backend source reference in rhtpa-release.0.3.z Konflux repo after upstream fix merges

Both tasks would be linked to TC-8006 with "Depend" link type. The downstream task is blocked by the upstream task.

### Cross-Stream Impact Note

The version impact analysis also shows that stream 2.2.x versions 2.2.0 and 2.2.1 are affected (quinn-proto 0.11.9 and 0.11.12 respectively). However, TC-8001 already exists for that stream and is In Progress, so no proactive remediation tasks are needed for stream 2.2.x. The existing "Related" link between TC-8006 and TC-8001 provides the cross-stream coordination.
