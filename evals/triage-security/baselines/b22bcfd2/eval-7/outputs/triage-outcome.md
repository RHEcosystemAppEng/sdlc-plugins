# Triage Outcome -- TC-8006

## Step 4.2 Pre-Existing Link Handling

### Context

TC-8006 (stream `[rhtpa-2.1]`) was found to have a sibling issue TC-8001 (stream `[rhtpa-2.2]`) via JQL search for issues with label `CVE-2026-31812`. TC-8001 is classified as a **different-stream companion** -- not a duplicate -- because the two issues track different streams (2.1.x vs 2.2.x).

### Idempotent Link Check (Step 4.2)

Per the Step 4.2 procedure, before creating a "Related" link to a cross-stream companion, the skill checks the current issue's existing `issuelinks` array from the `jira.get_issue` response (already fetched in Step 1).

**Check performed:**

1. Read TC-8006's `issuelinks` array
2. Found existing link:
   - Link ID: 1990401
   - `type.name`: `"Related"` -- matches required type
   - `outwardIssue.key`: `TC-8001` -- matches the sibling key
3. All criteria satisfied -- link already exists

**Decision**: Link creation was **skipped** because a matching "Related" link to TC-8001 already exists on TC-8006.

> Related link to TC-8001 already exists -- skipping link creation.

No `jira.create_link` call was made. This is the expected idempotent behavior -- running triage on an issue that already has the correct sibling links should not create duplicate links.

### What Was NOT Skipped

The following actions were still performed despite the link already existing:

1. **Sibling classification** -- TC-8001 was still classified as a different-stream companion (not a duplicate)
2. **Affects Versions overlap check** -- verified no version overlap between TC-8006 (RHTPA 2.1.0) and TC-8001 (RHTPA 2.2.0, RHTPA 2.2.1)
3. **Sibling landscape table** -- presented to the engineer showing all companion issues, their streams, statuses, and link status

The idempotent link check only affects the link creation action in Step 4.2. It does not suppress the sibling landscape summary or any other analysis. The engineer retains full visibility into the cross-stream companion landscape.

### Sibling Landscape (Presented to Engineer)

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions              | Link Status |
|------------|--------|-------------|-------------------------------|-------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     | Related (pre-existing) |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0                   | (current issue) |
```

### Triage Continuation

After Step 4.2 completes (with link creation skipped), triage continues with:

- **Step 5**: Version Lifecycle Check -- verify affected versions (RHTPA 2.1.0) are still within support lifecycle
- **Step 6**: Already Fixed Check -- check for resolved siblings (TC-8001 is In Progress, not resolved, so no already-fixed scenario)
- **Step 7**: Concurrent Triage Detection -- check for other in-progress triages on the same upstream component (skipped if Upstream Affected Component field not configured)
- **Step 8**: Remediation -- create remediation tasks for the 2.1.x stream if versions are affected

The pre-existing link does not alter the triage flow beyond skipping the redundant `jira.create_link` call. All subsequent steps proceed as normal.

## Proposed Actions

The following actions are proposed (not yet executed) pending engineer confirmation:

1. **Affects Versions**: Verify and correct based on version impact analysis (Step 3)
2. **Remediation tasks**: Create upstream backport + downstream propagation tasks for the 2.1.x stream if affected (Step 8, Case A)
3. **Post-triage label**: Add `ai-cve-triaged` label to TC-8006
4. **Summary comment**: Post triage summary to TC-8006 with version impact table and remediation task links

All Jira mutations are presented as proposals and require explicit engineer approval before execution.
