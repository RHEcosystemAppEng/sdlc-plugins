# Triage Outcome -- Step 4.2 Pre-Existing Link Handling for TC-8006

## Summary

TC-8006 (CVE-2026-31812 quinn-proto, stream [rhtpa-2.1]) has a pre-existing Related link to its cross-stream sibling TC-8001 (stream [rhtpa-2.2]). Step 4.2 correctly handled this by detecting the existing link and skipping duplicate link creation, demonstrating the idempotent linking behavior specified in the skill procedure.

## How Step 4.2 Handled the Pre-Existing Link

### The Idempotent Check

Step 4.2 specifies that before creating a Related link to a different-stream sibling, the skill must first check the current issue's `issuelinks` array for an existing link matching ALL of the following criteria:
1. `type.name` is `"Related"`
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key

### Application to TC-8006

1. **Sibling identified:** The JQL search returned TC-8001 as a sibling issue with the same CVE label (CVE-2026-31812) but a different stream suffix ([rhtpa-2.2] vs [rhtpa-2.1]). This makes TC-8001 a different-stream companion, not a duplicate.

2. **Existing link inspection:** The skill inspected TC-8006's `issuelinks` array (fetched during Step 1 data extraction). The array contains one link:
   - Link ID: 1990401
   - Type: Related
   - Direction: outward (TC-8006 -> TC-8001)

3. **Match evaluation:** The existing link satisfies both criteria:
   - `type.name` = "Related" -- matches the required link type
   - `outwardIssue.key` = "TC-8001" -- matches the sibling key being processed

4. **Skip decision:** Because a matching link was found, Step 4.2 logs "Related link to TC-8001 already exists -- skipping" and does NOT attempt to create a duplicate link.

### Why This Matters

The idempotent check prevents duplicate link creation in scenarios where:
- A prior triage run (or a different skill invocation) already created the Related link
- PSIRT or another user manually linked the sibling issues before triage began
- A partial triage was interrupted and is being re-run

Without this check, each triage run would attempt to create a new Related link, potentially resulting in errors (Jira rejects duplicate links of the same type between the same issues) or unnecessary API calls.

### Remaining Step 4.2 Actions

After skipping link creation, Step 4.2 continued with its other duties:
- **Affects Versions overlap verification:** Confirmed no overlap. TC-8006 owns RHTPA 2.1.0 (stream 2.1.x), TC-8001 owns RHTPA 2.2.0 and RHTPA 2.2.1 (stream 2.2.x). Each issue correctly carries versions only from its own stream.
- **Sibling landscape presentation:** Displayed the companion issue table showing both TC-8006 (2.1.x, New) and TC-8001 (2.2.x, In Progress) for engineer review.

## Overall Triage Flow Impact

The pre-existing link does not alter the triage flow. TC-8006 is a scoped issue for stream 2.1.x. The triage proceeds through Steps 5-8 normally:
- Step 5 (Lifecycle Check) would verify 2.1.x version support status
- Step 6 (Already Fixed Check) would check TC-8001's status; since TC-8001 is "In Progress" (not Closed/Done), it does not indicate an already-fixed scenario
- Steps 7/7.5/8 would proceed with remediation task creation for the 2.1.x stream, since version impact analysis shows quinn-proto 0.11.9 in versions 2.1.0 and 2.1.1, both below the fix threshold of 0.11.14
