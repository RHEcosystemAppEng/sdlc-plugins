# Step 4.2 Outcome -- Pre-Existing Link Handling

## Summary

When processing the cross-stream coordination for TC-8006 (stream [rhtpa-2.1]) and its sibling TC-8001 (stream [rhtpa-2.2]), Step 4.2 detected a **pre-existing Related link** and handled it idempotently.

## Classification Decision

TC-8001 was classified as a **different-stream companion**, not a same-stream duplicate:

- TC-8006 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- TC-8001 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)

The streams differ, so TC-8001 is a companion tracker for stream 2.2.x. This is the expected PSIRT pattern -- one Vulnerability issue per stream for the same CVE.

## Pre-Existing Link Detection (Step 4.2 Idempotency)

Step 4.2 prescribes checking the current issue's `issuelinks` array (already fetched in Step 1) before attempting to create a "Related" link to each different-stream sibling.

**Check performed:** Scanned TC-8006's `issuelinks` for any link where:
- `type.name` is `"Related"`
- `inwardIssue.key` or `outwardIssue.key` matches `TC-8001`

**Found:** Pre-existing link (Link ID: 1990401)
- Type: Related
- Direction: outward (TC-8006 --> TC-8001)

**Action taken:**

> Related link to TC-8001 already exists -- skipping

The `jira.create_link()` API call was **not** invoked. Creating a duplicate link would result in an unnecessary API call and potentially a redundant link in Jira. The idempotency check prevents this.

## What Was Still Presented

The idempotent check only affects link creation. The following outputs were still produced and presented to the engineer:

1. **Sibling classification** -- TC-8001 correctly identified as a different-stream companion
2. **Affects Versions overlap check** -- verified no version overlap between the two issues
3. **Sibling landscape table** -- the full companion issue table was presented showing both TC-8006 and TC-8001 with their respective streams, statuses, and Affects Versions

The sibling landscape table provides essential context regardless of whether links existed before triage began. Skipping the table because a link already exists would deprive the engineer of cross-stream visibility.

## Triage Continuation

After Step 4 completes (with link creation skipped but all analysis performed), the triage continues through the remaining steps:

- **Step 5** -- Version Lifecycle Check: verify 2.1.x versions are still supported
- **Step 6** -- Already Fixed Check: cross-reference resolved siblings
- **Step 7** -- Concurrent Triage Detection: check for active triages on same component
- **Step 8** -- Remediation: create remediation tasks for stream 2.1.x if versions are affected

The pre-existing link does not alter any subsequent triage behavior -- it only prevents a duplicate "Related" link from being created in Jira.
