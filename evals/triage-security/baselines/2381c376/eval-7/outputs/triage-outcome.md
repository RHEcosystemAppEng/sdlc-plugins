# Triage Outcome -- Step 4.2 Pre-Existing Link Handling for TC-8006

## Context

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) arrived with a pre-existing Related link to sibling TC-8001 (CVE-2026-31812, stream [rhtpa-2.2]). This link (ID 1990401, direction outward from TC-8006 to TC-8001) was already present in the issue's `issuelinks` array before triage began.

## How Step 4.2 Handled the Pre-Existing Link

Step 4.2 (Cross-stream coordination) requires creating a Related link between the current issue and each different-stream sibling. However, the procedure mandates an **idempotency check** before any link creation:

1. **Read existing links**: The skill reads TC-8006's `issuelinks` array from the `jira.get_issue` response already fetched in Step 1.

2. **Check for matching link**: For sibling TC-8001, the skill checks whether any existing link satisfies ALL of:
   - `type.name` is `"Related"`
   - `inwardIssue.key` or `outwardIssue.key` matches `TC-8001`

3. **Match found**: Link ID 1990401 matches both criteria:
   - Type: Related
   - outwardIssue.key: TC-8001

4. **Skip link creation**: Because a matching link already exists, the skill does NOT propose a `jira.create_link` call. Instead, it logs:
   > "Related link to TC-8001 already exists -- skipping"

## Why This Matters

The idempotency check in Step 4.2 prevents duplicate link creation. Without it, re-triaging TC-8006 (or triaging it when a link was pre-created by another process or a prior partial triage) would create a second Related link to TC-8001, cluttering the issue's link graph.

This behavior is explicitly specified in the skill definition under Step 4.2:

> "Check for existing link before creating one. Read the current issue's issuelinks array from the jira.get_issue response (already fetched in Step 1). Check if any existing link satisfies all of: type.name is 'Related', inwardIssue.key or outwardIssue.key matches the sibling key. If a matching link exists, skip link creation and log: 'Related link to [sibling-key] already exists -- skipping'"

## Remaining Step 4.2 Actions

Even though link creation was skipped, the other Step 4.2 sub-actions still executed:

- **Affects Versions overlap check**: No overlap found. TC-8006 has `[RHTPA 2.1.0]` and TC-8001 has `[RHTPA 2.2.0, RHTPA 2.2.1]` -- each issue carries only its own stream's versions.
- **Sibling landscape presentation**: The companion issue table was presented to the engineer showing both TC-8006 (2.1.x, New) and TC-8001 (2.2.x, In Progress).

## Proposed Jira Mutations from Step 4

None. The only mutation Step 4.2 would have performed (creating a Related link) was skipped due to the pre-existing link. Steps 4.1, 4.3, and 4.4 also produced no mutations (no same-stream duplicate, cross-CVE overlap check skipped because custom fields are not configured, and no preemptive tasks found to reconcile).
