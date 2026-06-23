# Triage Outcome -- TC-8006 (Step 4.2 Pre-Existing Link Handling)

## How Step 4.2 Handled the Pre-Existing Link

### Context

TC-8006 (stream `[rhtpa-2.1]`) has a pre-existing "Related" link to TC-8001 (stream `[rhtpa-2.2]`). Both issues track the same CVE (CVE-2026-31812) but for different product version streams. PSIRT intentionally creates one Vulnerability issue per stream, and these are companion trackers -- not duplicates.

### Step 4.2 Procedure Applied

Step 4.2 specifies the following procedure for cross-stream siblings:

> "Check for existing link before creating one. Read the current issue's `issuelinks` array from the `jira.get_issue` response (already fetched in Step 1). Check if any existing link satisfies all of:
> - `type.name` is `"Related"`
> - `inwardIssue.key` or `outwardIssue.key` matches the sibling key
>
> If a matching link exists, skip link creation and log:
> 'Related link to [sibling-key] already exists -- skipping'"

### What Was Found

TC-8006's `issuelinks` array (from the Step 1 `get_issue` response) contains:

- **Link type**: Related (type.name = "Related")
- **Direction**: outward
- **outwardIssue.key**: TC-8001
- **Link ID**: 1990401

This matches the sibling key TC-8001 returned by the JQL search. Both conditions are satisfied:
1. `type.name` is "Related" -- confirmed
2. `outwardIssue.key` matches the sibling key TC-8001 -- confirmed

### Decision

**Related link to TC-8001 already exists -- skipping link creation.**

No `jira.create_link` call is proposed. The skill recognized the pre-existing link and behaved idempotently. This is the correct behavior per Step 4.2's guard clause: the link check prevents duplicate "Related" links from being created when PSIRT or a prior triage run has already linked the companion issues.

### Affects Versions Overlap Check

After the link check, Step 4.2 also verifies no Affects Versions overlap between the current issue and the sibling. The results:

| Issue | Stream | Affects Versions |
|-------|--------|------------------|
| TC-8006 | 2.1.x | RHTPA 2.1.0 |
| TC-8001 | 2.2.x | RHTPA 2.2.0, RHTPA 2.2.1 |

No overlap detected. Each issue owns versions exclusively from its own stream.

### Sibling Landscape Summary

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions | Link Status |
|-------|--------|--------|------------------|-------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 | Pre-existing Related link (link ID 1990401) |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 | -- |

## Overall Triage Outcome for TC-8006

### Affects Versions Correction (Step 3)

The version impact analysis shows both RHTPA 2.1.0 and RHTPA 2.1.1 are affected (both ship quinn-proto 0.11.9, which is < 0.11.14). PSIRT only assigned RHTPA 2.1.0.

PROPOSED correction:
- Current: `[RHTPA 2.1.0]`
- Proposed: `[RHTPA 2.1.0, RHTPA 2.1.1]`

This is scoped to the 2.1.x stream per the issue suffix `[rhtpa-2.1]`.

### Sibling Coordination (Step 4)

- TC-8001 is a cross-stream companion (2.2.x stream), not a duplicate.
- Pre-existing "Related" link detected -- no new link needed (idempotent).
- No Affects Versions overlap between the two issues.
- TC-8001 is In Progress, meaning 2.2.x remediation is already underway.
- Cross-CVE overlap detection (Step 4.3) skipped -- required custom fields not configured.
- No preemptive tasks found for reconciliation (Step 4.4).

### Remediation (Step 7 -- Case A)

Since both 2.1.x versions (2.1.0 and 2.1.1) are affected and the issue is scoped to the 2.1.x stream, this is **Case A: Affected -- create remediation tasks**.

The ecosystem is Cargo (source dependency), so two tasks would be created:

1. **Upstream backport task**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
   - Repository: rhtpa-backend
   - Target branch: `release/0.3.z` (from Ecosystem Mappings Upstream Branch)
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`

2. **Downstream propagation task**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)
   - Repository: rhtpa-release.0.3.z
   - Target branch: main
   - Blocked by the upstream task
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`

Both tasks would be linked to TC-8006 with "Depend" link type. The downstream task would be linked to the upstream task with "Blocks" link type.

### Cross-Stream Impact (Step 7 -- Case B check)

The 2.2.x stream is also affected (versions 2.2.0 and 2.2.1 ship vulnerable quinn-proto). However, TC-8001 already exists as a companion CVE Jira for the 2.2.x stream and is In Progress. Therefore, no proactive remediation tasks are needed for the 2.2.x stream -- it will be handled through its own CVE issue.

PROPOSED cross-stream impact comment on TC-8006:
```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.2.x based on lock file analysis.
Stream 2.2.x is tracked by companion issue TC-8001 (In Progress) -- see Related link.
```

### Post-Triage Summary

PROPOSED actions (all require engineer confirmation):
1. Correct Affects Versions: `[RHTPA 2.1.0]` -> `[RHTPA 2.1.0, RHTPA 2.1.1]`
2. Create upstream backport task for 2.1.x stream
3. Create downstream propagation task for 2.1.x stream (blocked by upstream)
4. Link both tasks to TC-8006 with "Depend"
5. Post cross-stream impact comment noting 2.2.x is tracked by TC-8001
6. Add `ai-cve-triaged` label to TC-8006
7. Post triage summary comment to TC-8006
8. Transition TC-8006 to In Progress
