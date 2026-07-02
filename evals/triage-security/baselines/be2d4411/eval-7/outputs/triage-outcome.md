# Triage Outcome -- Step 4.2 Pre-Existing Link Handling for TC-8006

## Summary

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) has a pre-existing Related link to sibling TC-8001 (stream [rhtpa-2.2]). Step 4.2 of the triage procedure detected this existing link and skipped link creation, ensuring idempotent behavior.

## How Step 4.2 Handled the Pre-Existing Link

### Procedure followed

1. **Sibling classification**: TC-8001 was identified as a different-stream companion (stream [rhtpa-2.2] vs current [rhtpa-2.1]). It is NOT a same-stream duplicate -- PSIRT intentionally creates one Vulnerability issue per stream.

2. **Link existence check**: Before attempting to create a Related link, Step 4.2 inspected TC-8006's `issuelinks` array from the `jira.get_issue` response (fetched in Step 1). The check looks for any existing link where:
   - `type.name` is `"Related"`
   - `inwardIssue.key` or `outwardIssue.key` matches the sibling key (TC-8001)

3. **Match found**: Link ID 1990401 matched all criteria:
   - Type: Related
   - Direction: outward (TC-8006 -> TC-8001)
   - Target: TC-8001

4. **Link creation skipped**: Because a matching Related link already exists, link creation was skipped. The log message produced:

   > "Related link to TC-8001 already exists -- skipping"

5. **Sibling landscape still presented**: Despite the link already existing, the sibling landscape table was still presented to the engineer. The table provides situational awareness about all companion issues tracking the same CVE across streams, regardless of whether links needed to be created:

   | Issue      | Stream | Status      | Affects Versions              |
   |------------|--------|-------------|-------------------------------|
   | TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                   |
   | TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |

6. **No Affects Versions overlap**: The two issues carry versions from their own respective streams only (RHTPA 2.1.0 vs RHTPA 2.2.0/2.2.1), so no overlap was flagged.

## Why Idempotency Matters

The pre-existing link check prevents:
- **Duplicate links** in Jira, which would clutter the issue's link panel
- **API errors** from Jira when attempting to create an already-existing link
- **Re-triage failures** -- when an issue is re-triaged (e.g., to verify version impact after a matrix update), Step 4.2 must not fail or create duplicate links

This idempotent behavior ensures the triage-security skill can be safely re-run on the same issue without side effects on existing cross-stream relationships.

## Next Steps After Step 4.2

With the sibling check complete:
- Step 4.3 (Cross-CVE Overlap Detection) was skipped because the Upstream Affected Component custom field is not configured in Security Configuration.
- Step 4.4 (Preemptive Task Reconciliation) found no matching preemptive tasks.
- Triage proceeds to Step 5 (Version Lifecycle Check) and subsequent steps.
