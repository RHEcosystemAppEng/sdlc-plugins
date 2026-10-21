# Triage Outcome -- Step 4.2 Pre-Existing Link Handling

## Summary

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) has a pre-existing Related link to sibling TC-8001 (stream [rhtpa-2.2]). Step 4.2 of the triage-security skill detected this existing link and handled it idempotently by skipping link creation.

## How Step 4.2 Handled the Pre-Existing Link

### The Idempotency Mechanism

Step 4.2 (Cross-stream coordination) requires a link existence check before creating any Related link to a different-stream sibling. The procedure is:

1. For each different-stream sibling found by the JQL search (TC-8001 in this case), the skill reads the current issue's `issuelinks` array from the `jira.get_issue` response already fetched in Step 1.

2. It checks whether any existing link satisfies ALL of the following criteria:
   - `type.name` is "Related"
   - `inwardIssue.key` or `outwardIssue.key` matches the sibling key

3. **In this case**: TC-8006's `issuelinks` array contains a Related link (link ID 1990401) with `outwardIssue.key` = TC-8001. Both criteria are satisfied.

4. **Action taken**: Link creation is skipped. The skill logs:
   > "Related link to TC-8001 already exists -- skipping"

5. **No `jira.create_link` call is made.** The pre-existing link is functionally equivalent to one the skill would have created, so no mutation is needed.

### Why This Matters

This idempotency check prevents duplicate links when:
- PSIRT or another process has already linked sibling issues before triage runs
- The triage skill is re-run on an issue that was partially triaged previously
- Multiple triage sessions process sibling issues in overlapping timeframes

Without the check, the skill would attempt to create a second Related link between TC-8006 and TC-8001, which could result in a Jira API error (duplicate link) or a redundant link entry.

### Subsequent Steps Unaffected

The pre-existing link does not change the behavior of any subsequent step:

- **Step 4.1** (Same-stream duplicate check): TC-8001 is classified as a different-stream sibling, not a same-stream duplicate, based on stream suffix comparison ([rhtpa-2.2] vs [rhtpa-2.1]).
- **Step 4.3** (Cross-CVE overlap): Skipped because the required custom fields (Upstream Affected Component, PS Component, Stream) are not configured.
- **Step 4.4** (Preemptive task reconciliation): No preemptive tasks found for CVE-2026-31812 in stream 2.1.x.
- **Steps 5-8**: Proceed normally. The sibling landscape is correctly recorded and presented to the engineer regardless of whether the link was pre-existing or newly created.

## Overall Triage Path

Based on the full analysis:

1. **Data Extraction (Step 1)**: CVE-2026-31812 affects quinn-proto < 0.11.14, ecosystem Cargo, scoped to stream 2.1.x.
2. **Version Impact (Step 2)**: Both versions in 2.1.x (2.1.0 and 2.1.1) ship quinn-proto 0.11.9, which is vulnerable. Cross-stream: 2.2.x is partially affected (2.2.0-2.2.2) but already tracked by sibling TC-8001 (In Progress).
3. **Affects Versions Correction (Step 3)**: PSIRT assigned RHTPA 2.1.0 only. The version impact table shows both RHTPA 2.1.0 and RHTPA 2.1.1 are affected. Correction needed: add RHTPA 2.1.1 to Affects Versions.
4. **Sibling Check (Step 4)**: One sibling (TC-8001, stream 2.2.x, In Progress). Pre-existing Related link detected and preserved (no new link created). No duplicates, no overlap, no preemptive tasks.
5. **Expected outcome (Step 8)**: Case B -- create remediation tasks for the 2.1.x stream (2 tasks for Cargo ecosystem: upstream backport/dependency bump + downstream propagation). Case A cross-stream comment applies because 2.2.x is also affected, but it already has its own CVE Jira (TC-8001), so no preemptive tasks are needed for that stream.
