# Triage Outcome -- Step 4.2 Pre-Existing Link Handling for TC-8006

## Summary

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) has a pre-existing Related link
to sibling issue TC-8001 (stream [rhtpa-2.2]). Step 4.2 correctly identified
this existing link and skipped link creation, demonstrating idempotent behavior.

## How Step 4.2 Handled the Pre-Existing Link

### The Procedure

Step 4.2 specifies an explicit idempotency check before creating cross-stream
Related links. The procedure is:

1. Read the current issue's `issuelinks` array from the `jira.get_issue`
   response (already fetched in Step 1).
2. Check if any existing link satisfies ALL of:
   - `type.name` is "Related"
   - `inwardIssue.key` or `outwardIssue.key` matches the sibling key
3. If a matching link exists, **skip link creation** and log:
   > "Related link to [sibling-key] already exists -- skipping"
4. If no matching link exists, create the link via `jira.create_link`.

### What Happened for TC-8006

The `issuelinks` array on TC-8006 (fetched in Step 1) contains:

```
Link ID:   1990401
Type:      Related
Direction: outward (TC-8006 -> TC-8001)
```

When Step 4.2 processed the sibling TC-8001:

1. It checked TC-8006's `issuelinks` for a link where `type.name` is "Related"
   and `outwardIssue.key` matches "TC-8001".
2. Link ID 1990401 matched all criteria.
3. Link creation was **skipped**.
4. Log message: "Related link to TC-8001 already exists -- skipping"

No `jira.create_link` API call was made. This is the correct idempotent
behavior -- re-running triage on an issue that already has the appropriate
cross-stream link does not produce duplicate links or errors.

### Why This Matters

Idempotent link handling is important because:

- **Re-triage scenarios**: An engineer may re-run triage-security on an issue
  that was previously triaged (e.g., to verify version impact after a new
  release). Without the idempotency check, this would create duplicate Related
  links.
- **PSIRT pre-linking**: PSIRT tooling may pre-populate Related links between
  companion issues when creating them. The skill must respect these existing
  links rather than attempting to recreate them.
- **Error avoidance**: Some Jira configurations reject duplicate links, which
  would cause the skill to fail unnecessarily.

## Sibling Landscape (Still Presented)

Even though the link already existed and creation was skipped, the sibling
landscape table is still presented to the engineer for situational awareness:

```
CVE-2026-31812 companion issues:

| Issue       | Stream | Status      | Affects Versions              |
|-------------|--------|-------------|-------------------------------|
| TC-8001     | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <-  | 2.1.x  | New         | RHTPA 2.1.0                   |
```

The landscape table is always shown regardless of whether links were created or
skipped. It gives the engineer visibility into the full set of companion issues
tracking the same CVE across streams.

## Overall Triage Flow Impact

The pre-existing link does not alter the triage flow. After Step 4.2:

- Step 4.3 (Cross-CVE Overlap) is skipped because required custom fields are
  not configured.
- Step 4.4 (Preemptive Task Reconciliation) proceeds normally.
- Steps 5-8 proceed as they would for any affected-stream issue.

The issue is affected (quinn-proto 0.11.9 < 0.11.14 in both RHTPA 2.1.0 and
2.1.1), so the expected triage outcome is Case A (create remediation tasks for
the 2.1.x stream). The sibling TC-8001 is already tracking remediation for the
2.2.x stream independently.
