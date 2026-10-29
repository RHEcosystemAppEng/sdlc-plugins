# Triage Outcome: TC-8011 (CVE-2026-45678)

## Decision: Needs Remediation (Case B -- Affected)

The vulnerability in webpack (CVE-2026-45678, CVSS 7.8 High) requires new remediation because:

1. The fix threshold is **webpack >= 5.98.0**.
2. The only existing related remediation (TC-8013, from CVE-2026-43210) bumps webpack to **5.96.1**, which does **not** meet the fix threshold.
3. The issue is scoped to stream **2.2.x** (suffix `[rhtpa-2.2]`).

## Cross-CVE Overlap Result

A related CVE (TC-8012 / CVE-2026-43210) was found affecting the same upstream component (webpack) in the same stream and PS Component. Its remediation task TC-8013 bumps webpack to 5.96.1, but the current CVE requires >= 5.98.0. The version gap (5.96.1 vs 5.98.0) means the existing remediation is insufficient -- new remediation tasks must be created.

## Ecosystem Classification

webpack is an **npm** ecosystem package (source dependency). Per the ecosystem classification table, source dependency ecosystems with an available upstream fix produce **two remediation tasks per stream**:

1. **Dependency bump task** -- bump webpack to >= 5.98.0 in the rhtpa-ui source repository
2. **Downstream propagation task** -- propagate the bumped dependency into the Konflux release repo for the rhtpa-2.2 stream

## PROPOSED Jira Mutations (Not Executed)

The following mutations are presented as proposals. They have not been executed and require engineer confirmation before any Jira changes are made.

### Step 0.8 -- Assignment and Transition

| # | Action | Detail |
|---|--------|--------|
| 1 | PROPOSAL: Assign TC-8011 | Assign to current user |
| 2 | PROPOSAL: Transition TC-8011 | New --> Assigned |

### Step 3 -- Affects Versions Correction

| # | Action | Detail |
|---|--------|--------|
| 3 | PROPOSAL: Correct Affects Versions on TC-8011 | Current: [RHTPA 2.2.0] --> Proposed: all affected 2.2.x versions based on lock file evidence (scoped to stream 2.2.x per issue suffix) |
| 4 | PROPOSAL: Post comment on TC-8011 | Document the Affects Versions correction with lock file evidence |

### Step 4.3 -- Cross-CVE Overlap

No covering remediation exists. TC-8013 bumps to 5.96.1 but the fix threshold is 5.98.0.

| # | Action | Detail |
|---|--------|--------|
| 5 | No overlap closure | Existing remediation does not cover this CVE -- new tasks required |

### Step 8 -- Remediation Task Creation

| # | Action | Detail |
|---|--------|--------|
| 6 | PROPOSAL: Create remediation Task 1 | Bump webpack to >= 5.98.0 in rhtpa-ui (npm dependency bump for stream rhtpa-2.2) |
| 7 | PROPOSAL: Create remediation Task 2 | Downstream propagation -- propagate webpack bump into Konflux release repo rhtpa-release.0.4.z for stream 2.2.x |
| 8 | PROPOSAL: Link Task 1 to TC-8011 | Link type: Depend |
| 9 | PROPOSAL: Link Task 2 to TC-8011 | Link type: Depend |
| 10 | PROPOSAL: Link Task 2 Blocks Task 1 | Task 1 (upstream bump) blocks Task 2 (downstream propagation) |

### Step 7.5 -- Release Jira Orchestration

| # | Action | Detail |
|---|--------|--------|
| 11 | PROPOSAL: Find or create release Epic | Pattern: "RHTPA 2.2.x Release Tasks" for stream 2.2.x |
| 12 | PROPOSAL: Find or create release Task | Pattern: "RHTPA 2.2.x CVE triage" under the release Epic |
| 13 | PROPOSAL: Link remediation Tasks to release Task | Link type: Blocks |
| 14 | PROPOSAL: Link TC-8011 to release Task | Link type: Related |

### Post-Triage Summary

| # | Action | Detail |
|---|--------|--------|
| 15 | PROPOSAL: Add label to TC-8011 | ai-cve-triaged |
| 16 | PROPOSAL: Post summary comment on TC-8011 | Version impact table, Affects Versions correction, remediation task links, release Jira references, and @mention of reporter |

## Rationale

The triage concludes **Case B (Affected -- create remediation tasks)** because:

- The vulnerable library (webpack) is shipped at a version below the fix threshold (5.98.0).
- The existing remediation from CVE-2026-43210 (TC-8013) only bumps to 5.96.1, leaving a version gap.
- No other remediation or overlap covers the required fix threshold.
- The issue is scoped to the 2.2.x stream, so remediation tasks are created only for that stream.
- As a scoped issue, Case A (cross-stream impact) should also be evaluated: if other streams (e.g., 2.1.x) also ship webpack below 5.98.0, a cross-stream impact comment would be posted and preemptive tasks created for those streams (if no sibling CVE Jira exists for them).
