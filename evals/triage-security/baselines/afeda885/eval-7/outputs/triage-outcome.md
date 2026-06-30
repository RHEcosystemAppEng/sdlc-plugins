# Triage Outcome -- TC-8006

## How Step 4.2 Handled the Pre-Existing Link

### Context

TC-8006 (stream [rhtpa-2.1]) arrived with a pre-existing "Related" link to sibling TC-8001 (stream [rhtpa-2.2]). Both issues track the same CVE (CVE-2026-31812) but for different product version streams.

### Step 4.2 Idempotent Link Check

The Step 4.2 procedure specifies that before creating a cross-stream "Related" link, the skill must first check the current issue's `issuelinks` array (already fetched in Step 1) for an existing link that satisfies all of:

1. `type.name` is "Related"
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key

TC-8006's issue links contain:
- **Type**: Related
- **Direction**: outward (TC-8006 -> TC-8001)
- **Link ID**: 1990401

Since an existing Related link to TC-8001 was found, the skill logs:

> "Related link to TC-8001 already exists -- skipping"

**No `jira.create_link` call is made.** This is the idempotent behavior specified in Step 4.2 -- the skill detects the pre-existing link and avoids creating a duplicate. This prevents Jira API errors (duplicate link rejection) and unnecessary mutations.

### Affects Versions Overlap Check

Step 4.2 also verifies no Affects Versions overlap between companion issues:

- TC-8006: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

No overlap detected -- each issue correctly owns only its own stream's versions. No corrective action needed.

### Sibling Landscape

The complete companion landscape for CVE-2026-31812:

| Issue | Stream | Status | Affects Versions | Link Status |
|-------|--------|--------|------------------|-------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 | Pre-existing Related link (link ID 1990401) |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 | -- |

### Overall Triage Outcome Summary

1. **Data Extraction (Step 1)**: CVE-2026-31812 affects quinn-proto < 0.11.14. TC-8006 is scoped to stream 2.1.x. Ecosystem is Cargo (Rust crate).

2. **Version Impact (Step 2)**: Both versions in stream 2.1.x are affected:
   - RHTPA 2.1.0 (tag v0.3.8): quinn-proto 0.11.9 -- AFFECTED
   - RHTPA 2.1.1 (tag v0.3.12): quinn-proto 0.11.9 -- AFFECTED

3. **Affects Versions Correction (Step 3)**: Current Affects Versions is [RHTPA 2.1.0]. The version impact analysis shows RHTPA 2.1.1 is also affected. Proposed correction: [RHTPA 2.1.0, RHTPA 2.1.1] (add RHTPA 2.1.1).

4. **Sibling Check (Step 4)**: One cross-stream sibling found (TC-8001, stream 2.2.x, status In Progress). Pre-existing Related link detected and preserved (no duplicate link created). No same-stream duplicates. Step 4.3 skipped (custom fields not configured). No preemptive tasks found (Step 4.4).

5. **Remediation (Step 7, Case A)**: Both versions in stream 2.1.x are affected. Remediation tasks would be created:
   - **Upstream backport task**: Bump quinn-proto to >= 0.11.14 on branch `release/0.3.z` in the `backend` source repository.
   - **Downstream propagation subtask**: Update the backend source reference in `rhtpa-release.0.3.z` (Konflux release repo) to pick up the upstream fix. Blocked by the upstream task.
   - Both tasks linked to TC-8006 with "Depend" link type.
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`

6. **Cross-stream impact (Step 7, Case B)**: The 2.2.x stream is also affected (RHTPA 2.2.0, 2.2.1), but TC-8001 already exists as a companion CVE Jira for that stream and is already In Progress. No preemptive remediation tasks needed for stream 2.2.x -- it has its own CVE tracker.

7. **Post-triage**: Add `ai-cve-triaged` label to TC-8006. Post summary comment with version impact table, Affects Versions correction, remediation task links, and reporter @mention.
