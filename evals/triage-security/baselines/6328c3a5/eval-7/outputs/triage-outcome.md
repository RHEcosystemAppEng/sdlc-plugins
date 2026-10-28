# Triage Outcome -- Step 4.2 Pre-Existing Link Handling for TC-8006

## Summary

Step 4.2 (Cross-Stream Coordination) detected that TC-8006 already has a
pre-existing "Related" link to sibling issue TC-8001 (link ID 1990401). The
skill's idempotent linking logic correctly identified this existing link and
**skipped creating a duplicate link**.

## How Step 4.2 Handled the Pre-Existing Link

### The Procedure

Step 4.2 of `jira-triage-operations.md` specifies the following idempotent
check before creating a cross-stream sibling link:

1. Read the current issue's `issuelinks` array (already fetched in Step 1).
2. Check if any existing link satisfies **all** of:
   - `type.name` is `"Related"`
   - `inwardIssue.key` or `outwardIssue.key` matches the sibling key
3. If a matching link exists, **skip link creation** and log:
   `"Related link to [sibling-key] already exists -- skipping"`
4. If no matching link exists, create the link via `jira.create_link()`.

### What Was Found

TC-8006's `issuelinks` array contains:

| Link ID | Type | Direction | Target |
|---------|------|-----------|--------|
| 1990401 | Related | outward (TC-8006 -> TC-8001) | TC-8001 |

The existing link satisfies all three criteria:
- `type.name` = "Related" -- matches
- `outwardIssue.key` = "TC-8001" -- matches the sibling key
- Link is active and valid

### Decision

**Link creation was skipped.** The log message produced:

> "Related link to TC-8001 already exists -- skipping"

No `jira.create_link()` call was made. This is the correct idempotent behavior
-- the skill must not create duplicate links when a matching relationship
already exists.

### Why This Matters

PSIRT or other tooling may pre-create Related links between companion CVE
issues for the same vulnerability across different version streams. Step 4.2's
idempotent check ensures that:

1. **No duplicate links are created** -- Jira allows duplicate links of the
   same type between the same issues, which would create noise and confusion.
2. **The triage proceeds normally** -- skipping the link does not block any
   subsequent steps. The cross-stream coordination relationship is already
   recorded.
3. **The existing link direction is respected** -- whether the link is inward
   or outward, the check covers both directions (checking both
   `inwardIssue.key` and `outwardIssue.key`).

## Remaining Triage Steps

After Step 4.2, the triage continues with:

- **Step 4.3 (Cross-CVE Overlap)**: Skipped -- Upstream Affected Component
  custom field not configured.
- **Step 4.4 (Preemptive Task Reconciliation)**: No preemptive tasks found for
  this CVE and stream.
- **Step 5 (Version Lifecycle Check)**: Verify RHTPA 2.1.0 support status.
- **Step 6 (Already Fixed Check)**: TC-8001 is In Progress (not Closed/Done),
  so no already-fixed scenario applies.
- **Step 7 (Concurrent Triage Detection)**: Skipped -- Upstream Affected
  Component custom field not configured.
- **Step 8 (Remediation)**: Both 2.1.x versions are affected. Case B applies
  (Cargo ecosystem, 2 tasks: dependency bump or upstream backport +
  downstream propagation). Since this is a scoped issue and the 2.2.x stream
  is also affected but already has its own CVE Jira (TC-8001, In Progress),
  Case A cross-stream impact applies but no preemptive tasks are needed for
  the 2.2.x stream.
