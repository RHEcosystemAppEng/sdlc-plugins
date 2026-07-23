# Triage Outcome: TC-8006 -- Step 4.2 Pre-Existing Link Handling

## Summary

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) has a pre-existing "Related" link to sibling issue TC-8001 (stream [rhtpa-2.2]). Step 4.2 of the triage-security skill handled this link idempotently by detecting it and skipping redundant link creation.

## How Step 4.2 Handled the Pre-Existing Link

### The Idempotency Protocol

Step 4.2 of `jira-triage-operations.md` specifies an explicit idempotency check before creating cross-stream sibling links:

> "Check for existing link before creating one. Read the current issue's issuelinks array from the jira.get_issue response (already fetched in Step 1). Check if any existing link satisfies all of:
> - type.name is "Related"
> - inwardIssue.key or outwardIssue.key matches the sibling key"

### Application to TC-8006

1. **Sibling identification**: The JQL search for issues with label `CVE-2026-31812` (excluding TC-8006) returned TC-8001 with stream suffix `[rhtpa-2.2]`. Since `[rhtpa-2.2]` differs from TC-8006's `[rhtpa-2.1]`, TC-8001 is classified as a different-stream sibling (companion tracker), not a duplicate.

2. **Existing link check**: The issue's `issuelinks` array (from the Step 1 `get_issue` response) was inspected. It contains:
   - Link ID 1990401, type "Related", direction outward, outwardIssue.key = TC-8001

3. **Criteria evaluation**:
   - `type.name` is `"Related"` -- MATCH
   - `outwardIssue.key` is `TC-8001` -- MATCH (matches the sibling key)

4. **Decision**: Both criteria are satisfied. The link already exists.

5. **Action**: Link creation was **skipped**. The skill logged:
   > "Related link to TC-8001 already exists -- skipping"

No Jira mutation was performed for link creation. This is the correct idempotent behavior -- running triage on an issue that already has the expected sibling link does not create a duplicate link or fail.

### Why This Matters

The idempotency check prevents two failure modes:
- **Duplicate links**: Without the check, re-triaging TC-8006 (or triaging it after someone manually linked the sibling) would create a second "Related" link to TC-8001.
- **API errors**: Some Jira configurations reject duplicate links, which would cause the triage to fail unnecessarily.

## Remaining Triage Steps

After Step 4.2 completed (with the link skip), the triage would continue:

- **Step 4.3 (Cross-CVE overlap)**: Skipped -- Upstream Affected Component, PS Component, and Stream custom fields are not configured.
- **Step 4.4 (Preemptive task reconciliation)**: No preemptive tasks found for CVE-2026-31812 on stream 2.1.x.
- **Step 5 (Version Lifecycle)**: Would check product lifecycle page for RHTPA 2.1.0 support status.
- **Step 6 (Already Fixed)**: TC-8001 is "In Progress" (not Closed/Done), so no already-fixed scenario applies.
- **Step 7 (Concurrent Triage Detection)**: Skipped -- Upstream Affected Component field not configured.
- **Step 8 (Remediation)**: This is a **Case A + Case B** scenario:
  - **Case A**: Both RHTPA 2.1.0 and RHTPA 2.1.1 (per the version impact analysis from the supportability matrix -- both ship quinn-proto 0.11.9) are affected within the issue's 2.1.x stream scope. Two remediation tasks would be created: one upstream backport task (fix quinn-proto in rhtpa-backend on branch release/0.3.z) and one downstream propagation subtask (update reference in rhtpa-release.0.3.z).
  - **Case B**: The 2.2.x stream is also affected (RHTPA 2.2.0, 2.2.1 ship vulnerable versions). However, a sibling CVE Jira (TC-8001) already exists for the 2.2.x stream and is "In Progress", so no preemptive remediation tasks are needed for that stream. A cross-stream impact comment would be posted noting that TC-8001 covers the 2.2.x stream.

### Affects Versions Correction (Step 3)

The current Affects Versions on TC-8006 is [RHTPA 2.1.0]. The version impact analysis shows both RHTPA 2.1.0 and RHTPA 2.1.1 are affected (both ship quinn-proto 0.11.9 at tags v0.3.8 and v0.3.12 respectively). The proposed correction:

```
Current: [RHTPA 2.1.0] -> Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]
```

RHTPA 2.1.1 is missing from the PSIRT-assigned Affects Versions and would need to be added after engineer confirmation.
