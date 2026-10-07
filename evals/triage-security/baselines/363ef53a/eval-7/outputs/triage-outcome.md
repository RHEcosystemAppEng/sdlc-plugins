# Triage Outcome -- Step 4.2 Pre-Existing Link Handling for TC-8006

## Summary

Step 4.2 (Cross-Stream Coordination) detected that a "Related" link between TC-8006 and its sibling TC-8001 already exists. The skill's idempotent linking logic correctly skipped link creation, avoiding a duplicate link error.

## How Step 4.2 Handled the Pre-Existing Link

### The Idempotency Protocol

Step 4.2 specifies:

> "Check for existing link before creating one. Read the current issue's `issuelinks` array from the `jira.get_issue` response (already fetched in Step 1). Check if any existing link satisfies all of:
> - `type.name` is `"Related"`
> - `inwardIssue.key` or `outwardIssue.key` matches the sibling key"

### What Happened

1. **Sibling identified**: The JQL search returned TC-8001 as a different-stream sibling (stream [rhtpa-2.2] vs TC-8006's [rhtpa-2.1]).

2. **Existing links inspected**: TC-8006's `issuelinks` array (fetched during Step 1 data extraction) contains one link:
   - Link ID: 1990401
   - Type: Related
   - Direction: outward (TC-8006 -> TC-8001)

3. **Match found**: The existing link satisfies both conditions:
   - `type.name` is `"Related"` -- YES
   - `outwardIssue.key` matches sibling key `TC-8001` -- YES

4. **Link creation skipped**: Because a matching link already exists, Step 4.2 skipped the `jira.create_link()` call and logged:
   > "Related link to TC-8001 already exists -- skipping"

5. **Remaining Step 4.2 actions proceeded normally**:
   - Verified no Affects Versions overlap between TC-8006 (RHTPA 2.1.0) and TC-8001 (RHTPA 2.2.0, RHTPA 2.2.1) -- no overlap found
   - Presented the sibling landscape table showing both companion issues

### Why This Matters

Without the idempotency check, calling `jira.create_link()` for a link that already exists would either:
- Create a duplicate link (cluttering the issue)
- Return an error from the Jira API (breaking the triage flow)

The idempotency check ensures that re-triaging an issue (or triaging an issue where PSIRT or another engineer already created sibling links) proceeds without errors or duplicates. The skill reads the existing `issuelinks` data that was already fetched in Step 1, so no additional API call is needed for the check.

### Downstream Impact

The pre-existing link has no effect on subsequent steps:
- **Step 4.3** (Cross-CVE Overlap): Skipped because the Upstream Affected Component custom field is not configured.
- **Step 4.4** (Preemptive Task Reconciliation): No preemptive tasks found for CVE-2026-31812 in the 2.1.x stream.
- **Steps 5-8**: Proceed as normal. The sibling TC-8001 is already linked, so the cross-stream relationship is recorded regardless of whether the link was created in this triage session or pre-existed.
