# Triage Outcome -- Step 4.2 Pre-Existing Link Handling: TC-8006

## Summary

Step 4.2 (Cross-stream coordination) handled the pre-existing "Related" link between TC-8006 and TC-8001 through **idempotent link detection**. The link was recognized as already satisfying the cross-stream coordination requirement, so no duplicate link was created.

## How Step 4.2 Handled the Pre-Existing Link

### The Idempotent Check

SKILL.md Step 4.2 specifies that before creating a "Related" link to a different-stream sibling, the skill must first check the current issue's `issuelinks` array for an existing link that satisfies ALL of:

1. `type.name` is `"Related"`
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key

### Application to TC-8006

TC-8006 already has a "Related" link to TC-8001 (link ID 1990401, direction: outward). When Step 4.2 evaluated whether to create a link to sibling TC-8001:

1. **Read existing links**: The issuelinks array from the Step 1 `jira.get_issue` response was inspected.
2. **Found match**: Link ID 1990401 has `type.name = "Related"` and `outwardIssue.key = "TC-8001"`, satisfying both conditions.
3. **Skipped creation**: Because the matching link already exists, link creation was skipped with the log message: "Related link to TC-8001 already exists -- skipping"

### Why This Matters

The idempotent check prevents:
- **Duplicate Jira links**: Creating a second "Related" link between the same two issues would clutter the issue link section and confuse engineers reviewing the sibling landscape.
- **API errors**: Some Jira configurations reject duplicate links of the same type between the same pair of issues.
- **Re-triage safety**: When an issue is re-triaged (e.g., after Affects Versions correction), Step 4.2 runs again. Without the idempotent check, each re-triage would create another link.

### Remaining Step 4.2 Actions

After the link check, Step 4.2 continued with:
- **Affects Versions overlap verification**: Confirmed no overlap exists between TC-8006 (RHTPA 2.1.0) and TC-8001 (RHTPA 2.2.0, RHTPA 2.2.1). Each issue correctly carries only versions from its own stream.
- **Sibling landscape presentation**: The companion issue table was assembled showing both issues, their streams, statuses, and Affects Versions for engineer review.

## Overall Triage State After Step 4

| Check | Result |
|-------|--------|
| Same-stream duplicate (4.1) | None found -- TC-8001 is a different stream |
| Cross-stream link (4.2) | Pre-existing "Related" link detected -- skipped creation |
| Affects Versions overlap (4.2) | No overlap -- each issue owns its own stream's versions |
| Cross-CVE overlap (4.3) | Skipped -- required custom fields not configured |
| Preemptive task reconciliation (4.4) | No preemptive tasks found |

Triage proceeds to Step 5 (Version Lifecycle Check) with the sibling landscape documented and no Jira mutations required from Step 4.
