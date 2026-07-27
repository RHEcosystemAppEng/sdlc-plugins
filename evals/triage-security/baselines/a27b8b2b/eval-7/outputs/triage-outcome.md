# Triage Outcome -- TC-8006

## Step 4.2 Pre-existing Link Handling

Step 4 detected sibling issue TC-8001 (CVE-2026-31812, stream [rhtpa-2.2]) as a **different-stream companion** -- not a same-stream duplicate. The two issues track the same CVE for different product version streams:

- **TC-8006**: stream [rhtpa-2.1] (2.1.x)
- **TC-8001**: stream [rhtpa-2.2] (2.2.x)

### Idempotent Link Check

Step 4.2 inspected TC-8006's existing `issuelinks` array (fetched during Step 1 data extraction) before attempting to create a Related link to TC-8001. The check found:

- An existing link with `type.name` = "Related" and `outwardIssue.key` = "TC-8001"

Because this link already exists, **link creation was skipped**:

> Related link to TC-8001 already exists -- skipping

`jira.create_link` was NOT called. This idempotent behavior prevents duplicate links when triage is re-run or when PSIRT pre-populates cross-stream Related links before triage begins.

### What Was Still Presented

The idempotent check only affects the link creation mutation. The following outputs were still generated and presented to the engineer:

1. **Sibling classification** -- TC-8001 classified as different-stream companion (not duplicate)
2. **Affects Versions overlap check** -- confirmed no version overlap between the two issues
3. **Sibling landscape table** -- full companion issue table showing both TC-8001 and TC-8006 with their streams, statuses, and Affects Versions

### Summary of Step 4 Actions

| Action | Result |
|--------|--------|
| Sibling search (JQL) | 1 result: TC-8001 |
| Same-stream duplicate check | No -- different streams (2.1.x vs 2.2.x) |
| Cross-stream Related link | **Skipped** -- pre-existing link detected |
| Affects Versions overlap | None detected (clean stream separation) |
| Sibling landscape table | Presented to engineer |
| Cross-CVE overlap (Step 4.3) | Skipped -- Upstream Affected Component field not configured |
| Preemptive task reconciliation (Step 4.4) | No preemptive tasks found |

### Triage Continues

With the sibling check complete and no duplicate detected, triage continues to Step 5 (Version Lifecycle Check) and subsequent steps. The issue TC-8006 remains open for standard remediation processing scoped to the 2.1.x stream.
