# Triage Outcome – Step 4.2 handling of the pre-existing link (TC-8006)

## Summary

TC-8006 (CVE-2026-31812, quinn-proto, `[rhtpa-2.1]`) has one sibling, TC-8001 (`[rhtpa-2.2]`, In Progress). The two are in different streams, so TC-8001 is a **cross-stream companion tracker** and not a duplicate. TC-8006 stays open and triage continues.

## How Step 4.2 handled the pre-existing Related link

1. **Checked before creating.** Step 4.2.1 says to read the current issue's `issuelinks` (already fetched in Step 1) before creating any link.
2. **Found a match.** TC-8006 already has link ID 1990401 with `type.name = "Related"` and `outwardIssue.key = TC-8001`. This meets both match conditions: the type is Related, and either side of the link (here the outward side) is the sibling key.
3. **Skipped creation (idempotent).** The skill logged:
   > "Related link to TC-8001 already exists — skipping"

   No `jira.create_link(inwardIssue: TC-8006, outwardIssue: TC-8001, type: "Related")` call was made. No duplicate link was created, so no confirmation prompt was needed for a link mutation.
4. **Direction does not matter.** The check accepts the sibling on either the inward or the outward side. The existing outward link (TC-8006 -> TC-8001) therefore counts, even though the skill's own create call would put the keys in the opposite order.
5. **Rest of 4.2 still ran.**
   - Affects Versions overlap check: TC-8006 {2.1.0, proposed +2.1.1} vs TC-8001 {2.2.0, 2.2.1}. They share no versions, so no overlap was flagged.
   - The sibling landscape table was shown to the engineer (see sibling-check.md).

## Related outcomes from other steps

- Step 4.1: there are no same-stream siblings, so the issue is not closed as Duplicate.
- Step 4.3: skipped, because the Upstream Affected Component field is not configured.
- Step 4.4: no preemptive task was found, so there was nothing to reconcile.
- Step 3 (proposed, needs confirmation): Affects Versions `[RHTPA 2.1.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]`. Both 2.1.x builds ship quinn-proto 0.11.9, which is below 0.11.14.
- Expected remediation path (Step 8, Case B, Cargo): two tasks for stream 2.1.x. The first bumps quinn-proto to >= 0.11.14 upstream on `release/0.3.z` in rhtpa-backend. The second propagates the fix downstream in rhtpa-release.0.3.z. Both need engineer confirmation.
- Informational for TC-8001's owner: RHTPA 2.2.2 (a retag of v0.4.8, quinn-proto 0.11.12) is also affected but is missing from TC-8001's Affects Versions.

## Jira mutations in this eval

None were executed. The only link operation Step 4.2 considered was skipped because the link already existed.
