# Triage Outcome -- Step 4.2 Pre-existing Link Handling

## Summary

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) has a sibling issue TC-8001 (same CVE, stream [rhtpa-2.2]). Step 4 correctly classified TC-8001 as a **different-stream companion** -- not a same-stream duplicate -- because TC-8001's stream suffix `[rhtpa-2.2]` differs from TC-8006's `[rhtpa-2.1]`.

## Step 4.2 Idempotent Link Handling

Per the Step 4.2 protocol, before creating a "Related" link to sibling TC-8001, the skill checks the current issue's existing `issuelinks` array (already available from the Step 1 `jira.get_issue` response).

### Link Inspection Result

The existing issuelinks on TC-8006 include:

- **Link ID**: 1990401
- **Type**: Related
- **Direction**: outward (TC-8006 -> TC-8001)
- **Linked Issue**: TC-8001

This link satisfies all required criteria:
1. `type.name` is `"Related"` -- confirmed
2. `outwardIssue.key` matches the sibling key `TC-8001` -- confirmed

### Decision

**Related link to TC-8001 already exists -- skipping link creation.**

The `jira.create_link` call was NOT executed because a matching "Related" link already exists between TC-8006 and TC-8001. This idempotent check prevents creating duplicate links when an issue has been previously linked (e.g., by a prior triage run or manual linking by an engineer).

### What Was NOT Skipped

The idempotent check only affects link creation. The following outputs were still produced despite the link already existing:

1. **Sibling classification** -- TC-8001 was still classified as a different-stream companion (not a duplicate)
2. **Affects Versions overlap check** -- the versions were still compared to verify no cross-stream overlap exists
3. **Sibling landscape table** -- the companion issue summary was still presented to the engineer for context

## Triage Continues

Since TC-8001 is a different-stream companion (not a same-stream duplicate), the triage of TC-8006 continues normally through Steps 5-8. The duplicate detection did not short-circuit the flow -- only same-stream duplicates (Step 4.1) would cause the triage to stop and recommend closure.

The triage proceeds to:
- Step 5 (Version Lifecycle Check)
- Step 6 (Already Fixed Check)
- Step 7 (Concurrent Triage Detection)
- Step 8 (Remediation) -- where remediation tasks would be proposed for the 2.1.x stream based on version impact analysis
