# Triage Outcome -- Step 4.2 Pre-Existing Link Handling

## Summary

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) has a sibling issue TC-8001 (same CVE, stream [rhtpa-2.2]).

### Step 4.2 handled the pre-existing link as follows:

1. **Sibling classification**: TC-8001 is classified as a **different-stream companion** (stream [rhtpa-2.2] vs current issue's [rhtpa-2.1]). It is NOT a duplicate.

2. **Pre-existing link detection**: Before attempting to create a "Related" link to TC-8001, Step 4.2 checked TC-8006's existing `issuelinks` array (fetched in Step 1). The array contains a pre-existing "Related" link to TC-8001 (Link ID: 1990401, direction: outward).

3. **Link creation skipped**: Because a matching link already exists (type.name = "Related", outwardIssue.key = TC-8001), `jira.create_link` was NOT called. This is the idempotent check described in the skill documentation (Step 4.2): "If a matching link exists, skip link creation and log: Related link to [sibling-key] already exists -- skipping."

4. **Sibling landscape still presented**: The sibling landscape table was presented to the engineer showing both TC-8001 (2.2.x, In Progress) and TC-8006 (2.1.x, New). The idempotent check only affects link creation, not the sibling summary -- the engineer still gets full visibility into the companion issues for this CVE.

### Triage continues

Since TC-8006 is not a duplicate, triage proceeds to the remaining steps:
- Step 4.3 (Cross-CVE overlap detection)
- Step 4.4 (Preemptive task reconciliation)
- Steps 5-6 (Lifecycle and already-fixed checks)
- Step 7 (Concurrent triage detection)
- Step 8 (Remediation -- Case A for the 2.1.x stream)
