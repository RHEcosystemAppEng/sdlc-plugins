# Triage Outcome -- Step 4.2 Pre-Existing Link Handling: TC-8006

## Summary

Step 4.2 (Cross-Stream Coordination) detected a pre-existing Related link between TC-8006 and its sibling TC-8001 and correctly skipped link creation, demonstrating idempotent behavior.

## What Happened

TC-8006 (`[rhtpa-2.1]`) arrived with a pre-existing Related link to TC-8001 (`[rhtpa-2.2]`). Both issues track the same CVE (CVE-2026-31812) for different product version streams.

When Step 4.2 processed the cross-stream sibling TC-8001, it followed the skill's idempotent linking protocol:

1. **Read the existing issuelinks** from the `jira.get_issue` response already fetched in Step 1. TC-8006's `issuelinks` array contains one entry:
   - Link ID: 1990401
   - Type: Related
   - Direction: outward (TC-8006 -> TC-8001)

2. **Checked for a matching link** against the criteria defined in Step 4.2 of `jira-triage-operations.md`:
   - `type.name` is "Related" -- matched
   - `outwardIssue.key` matches the sibling key "TC-8001" -- matched

3. **Skipped link creation** because all criteria were satisfied. Logged:
   > "Related link to TC-8001 already exists -- skipping"

4. **No Jira mutation was proposed or executed** for link creation. The existing link is preserved as-is.

## Why This Matters

The idempotent check prevents:
- **Duplicate links**: Creating a second Related link between the same two issues
- **API errors**: Some Jira configurations reject duplicate links with a 400/409 error
- **Audit noise**: Unnecessary link creation events in the issue's activity history

This is consistent with the skill's guardrail that every Jira mutation requires confirmation -- by detecting the link already exists, no confirmation prompt is needed and the triage proceeds without interruption.

## Remaining Step 4 Actions

After the link idempotency check, Step 4.2 continued with:
- **Affects Versions overlap check**: No overlap detected (TC-8006 has RHTPA 2.1.0; TC-8001 has RHTPA 2.2.0, RHTPA 2.2.1)
- **Sibling landscape presentation**: Both companion issues shown to the engineer for awareness

Step 4.3 (Cross-CVE Overlap Detection) was **skipped** because the required custom fields (Upstream Affected Component, PS Component, Stream) are not configured in the project's Security Configuration.

Step 4.4 (Preemptive Task Reconciliation) found no matching preemptive tasks for CVE-2026-31812 in the 2.1.x stream.

## PROPOSALS (Jira Mutations)

No Jira mutations were proposed in Step 4 for TC-8006. The pre-existing Related link to TC-8001 is already correct and no changes are needed.

Subsequent steps (Steps 5-8) would propose mutations for:
- Affects Versions correction (Step 3, if needed after version impact analysis)
- Remediation task creation (Step 8, Case A -- since quinn-proto 0.11.9 in the 2.1.x stream is below the fix threshold of 0.11.14)
