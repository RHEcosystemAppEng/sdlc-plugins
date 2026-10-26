# Triage Outcome -- Step 4.2 Pre-existing Link Handling for TC-8006

## Summary

Step 4.2 (Cross-stream coordination) detected that a Related link from TC-8006 to sibling TC-8001 **already exists** and correctly skipped link creation, demonstrating the idempotent linking behavior required by the skill specification.

## How Step 4.2 Handled the Pre-existing Link

### Procedure Followed

The Step 4.2 procedure requires checking for an existing link before creating one. The check is defined as:

> Read the current issue's `issuelinks` array from the `jira.get_issue` response (already fetched in Step 1). Check if any existing link satisfies all of:
> - `type.name` is `"Related"`
> - `inwardIssue.key` or `outwardIssue.key` matches the sibling key

### Evidence Evaluated

TC-8006's issue links (from the issue data fetched in Step 1):

| Link ID | Type | Direction | Target |
|---------|------|-----------|--------|
| 1990401 | Related | outward | TC-8001 |

### Match Criteria

1. `type.name` is `"Related"` -- **MATCH** (the existing link type is Related)
2. `outwardIssue.key` matches sibling key `TC-8001` -- **MATCH**

Both conditions satisfied. The existing link fully satisfies the cross-stream coordination requirement.

### Action Taken

**Link creation was skipped.** The skill logged:

> "Related link to TC-8001 already exists -- skipping"

No `jira.create_link` call was made. This prevents a duplicate Related link between TC-8006 and TC-8001.

### Why This Matters

The idempotent check in Step 4.2 prevents duplicate Jira links when:

1. **PSIRT pre-links sibling issues** -- As in this case, PSIRT may create Related links between companion CVE trackers across streams when creating them. Without the idempotency check, the triage skill would create a second Related link between the same two issues.

2. **Re-triage scenarios** -- If the triage skill is run a second time on the same issue (e.g., to update Affects Versions after a new release), the idempotency check ensures existing links are preserved without duplication.

3. **Consistency with other idempotent checks** -- The same pattern is used in Step 4.3 (cross-CVE overlap links) and Step 4.4 (preemptive task reconciliation), ensuring consistent behavior across all linking operations.

## Additional Step 4.2 Findings

- **No Affects Versions overlap**: TC-8006 carries RHTPA 2.1.0 (stream 2.1.x) and TC-8001 carries RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x). Each issue correctly owns only versions from its own stream.
- **Sibling landscape presented**: Both companion issues are documented with their stream, status, and Affects Versions for the engineer's awareness.
- **TC-8001 status**: In Progress -- the sibling is already being actively triaged/worked on for the 2.2.x stream, which is expected since each stream has its own CVE tracker.

## Overall Triage Disposition

TC-8006 is a valid, non-duplicate vulnerability issue scoped to the 2.1.x stream. Both versions in the stream (2.1.0 and 2.1.1) ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14. The issue requires remediation (Case B: create remediation tasks for the 2.1.x stream). The cross-stream sibling TC-8001 is already linked and being handled separately for the 2.2.x stream. No new links, duplicate closures, or overlap actions are needed for Step 4.
