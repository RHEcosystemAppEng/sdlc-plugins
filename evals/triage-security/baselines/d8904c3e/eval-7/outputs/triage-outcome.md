# Triage Outcome -- Step 4.2 Pre-Existing Link Handling

## Summary

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) has a pre-existing "Related" link to sibling TC-8001 (stream [rhtpa-2.2]). Step 4.2 correctly detected this link and skipped redundant link creation, demonstrating idempotent behavior.

## Step 4.2 Decision Logic

The Step 4.2 cross-stream coordination protocol requires an idempotent link check before creating any new links. The procedure is:

1. Read the current issue's `issuelinks` array from the `jira.get_issue` response (already fetched in Step 1).
2. Check if any existing link satisfies **all** of:
   - `type.name` is `"Related"`
   - `inwardIssue.key` or `outwardIssue.key` matches the sibling key
3. If a matching link exists, **skip link creation** and log the skip.
4. If no matching link exists, create the link.

## Application to TC-8006

TC-8006's existing issue links include:

- Type: **Related**
- Direction: outward (TC-8006 -> TC-8001)
- Linked issue: **TC-8001**
- Link ID: 1990401

Checking the conditions:
- `type.name` is `"Related"` -- **satisfied**
- `outwardIssue.key` matches sibling key TC-8001 -- **satisfied**

Both conditions are met. The existing link fully satisfies the cross-stream coordination requirement.

## Outcome

**Link creation was skipped.** The skill logged:

> Related link to TC-8001 already exists -- skipping

No Jira `create_link` call was made. This is the correct idempotent behavior specified by Step 4.2: the pre-existing Related link (ID 1990401) already establishes the cross-stream relationship between TC-8006 (2.1.x) and TC-8001 (2.2.x). Creating a duplicate link would be redundant and could cause Jira API errors.

## Why This Matters

Without the idempotent check, re-running triage on an issue that already has sibling links would either:
- Fail with a Jira API error (duplicate link)
- Create redundant duplicate links cluttering the issue

The Step 4.2 protocol prevents both scenarios by checking existing links before attempting creation. This is consistent with the same idempotent pattern used in Step 4.3 (cross-CVE overlap) for Related and Depend links.

## Remaining Triage Path

After Step 4.2 completes (with the link skip), the triage continues:
- Step 4.3 (Cross-CVE Overlap): **Skipped** -- Upstream Affected Component, PS Component, and Stream custom fields are not configured
- Step 4.4 (Preemptive Task Reconciliation): No preemptive tasks found for this CVE and stream
- Steps 5-8 would continue with version lifecycle check, already-fixed check, concurrent triage detection, and remediation task creation for the 2.1.x stream
