# Triage Outcome -- Step 4.2 Pre-Existing Link Handling

## Summary

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) was triaged with a focus on Step 4 sibling detection and cross-stream coordination. The key finding is that Step 4.2 correctly handled a pre-existing "Related" link to sibling TC-8001 (stream [rhtpa-2.2]).

## Step 4 Sibling Classification

TC-8001 was correctly classified as a **different-stream companion** issue:
- TC-8006 stream: `[rhtpa-2.1]` (2.1.x)
- TC-8001 stream: `[rhtpa-2.2]` (2.2.x)
- Classification: **different-stream companion** (NOT a same-stream duplicate)

Because the streams differ, the duplicate closure path (Step 4.1) was not triggered.

## Step 4.2 -- Idempotent Link Handling

Step 4.2 requires creating a "Related" link between companion issues. Before calling `jira.create_link`, the skill checks the current issue's existing `issuelinks` array.

### What happened

1. **Checked existing issuelinks** on TC-8006 (from the `jira.get_issue` response already fetched in Step 1).
2. **Found a pre-existing link** matching all criteria:
   - `type.name` is "Related"
   - `outwardIssue.key` is "TC-8001"
   - Link ID: 1990401
3. **Skipped link creation** -- `jira.create_link` was NOT called.
4. **Logged the skip:** "Related link to TC-8001 already exists -- skipping"

### Why this matters

The idempotent link check prevents duplicate links when triage is re-run on an issue that was previously processed (or when links were created manually or by another process before triage). Without this check, re-running triage would create a second "Related" link to TC-8001, cluttering the issue's link list.

### What was NOT affected by the skip

The following actions proceeded normally despite the link already existing:

- **Sibling landscape table** -- still presented to the engineer showing TC-8001 (2.2.x, In Progress) and TC-8006 (2.1.x, New). The idempotent check only affects link creation, not the sibling summary.
- **Affects Versions overlap check** -- still verified that TC-8006 and TC-8001 carry versions from their respective streams without overlap.
- **Step 4.3 and Step 4.4** -- proceeded as normal (Step 4.3 skipped due to no Upstream Affected Component field configured; Step 4.4 found no preemptive tasks).

## Triage Continuation

The triage is not short-circuited by the sibling check. TC-8001 is a companion, not a duplicate, so triage continues through Steps 5-8 for TC-8006:

- Step 5: Version Lifecycle Check for affected 2.1.x versions
- Step 6: Already Fixed Check against resolved siblings
- Step 7: Concurrent Triage Detection (if Upstream Affected Component configured)
- Step 8: Remediation task creation for the 2.1.x stream (Case B -- Cargo ecosystem produces 2 tasks: upstream backport + downstream propagation)

The pre-existing link to TC-8001 has no bearing on remediation task creation -- it only confirms that cross-stream coordination linkage is already in place.

## Proposed Actions Summary

All proposed actions are presented as proposals requiring engineer confirmation before execution:

| Action | Status | Rationale |
|--------|--------|-----------|
| Create "Related" link TC-8006 -> TC-8001 | **Skipped** (already exists) | Pre-existing link detected via issuelinks check |
| Close as Duplicate | **Not applicable** | TC-8001 is a different-stream companion, not a same-stream duplicate |
| Present sibling landscape table | **Completed** | Shown to engineer regardless of link status |
| Affects Versions overlap check | **Completed** | No overlap -- each issue covers its own stream's versions |
| Continue to Steps 5-8 | **Proposed** | Standard triage continuation for stream 2.1.x |
