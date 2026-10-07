# Triage Outcome for TC-8020 (CVE-2026-31812 / quinn-proto)

## Issue Summary

- **Issue key**: TC-8020
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Affected range**: versions before 0.11.14
- **Fixed version**: 0.11.14
- **CVSS**: 7.5 (High)
- **Stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Ecosystem**: Cargo (source dependency)
- **Upstream Affected Component**: quinn-proto (customfield_10632)

## Version Impact Summary

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | Outside issue scope |
| 2.1.1 | 2.1.x | 0.11.9 | YES | Outside issue scope |
| 2.2.0 | 2.2.x | 0.11.9 | YES | In scope |
| 2.2.1 | 2.2.x | 0.11.12 | YES | In scope |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1, in scope |
| 2.2.3 | 2.2.x | 0.11.14 | NO | Fixed version shipped |
| 2.2.4 | 2.2.x | 0.11.14 | NO | Fixed version shipped |

## Affects Versions Correction (Step 3)

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Problem**: RHTPA 2.0.0 does not correspond to any configured version stream. The configured streams are 2.1.x and 2.2.x. The PSIRT assignment is incorrect.
- **Proposed correction**: Since the issue is scoped to stream 2.2.x, the corrected Affects Versions should include only 2.2.x versions that are affected:
  - `RHTPA 2.2.0`
  - `RHTPA 2.2.1`
  - `RHTPA 2.2.2` (if registered in Jira)
- **Correction**: `Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
- Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14, the fixed version) and should not be in Affects Versions.

## Triage Decision Path

### Step 7 -- Concurrent Triage Detection: BLOCKED

A concurrent triage was detected:

- **TC-8019** is In Progress, assigned to engineer-b@example.com, and affects the same upstream component (`quinn-proto` via customfield_10632).
- The engineer must choose one of three options before triage can proceed:
  1. **Wait** -- pause until TC-8019 completes
  2. **Skip** -- skip remediation task creation
  3. **Proceed** -- create tasks with `concurrent-triage-overlap` label

**The triage is gated at Step 7. No remediation tasks can be created until the engineer makes a decision.**

### Triage Outcome (contingent on Step 7 resolution)

If the engineer chooses to **proceed** (Option 3), the following triage path applies:

#### Case determination

- Supported versions in scope (2.2.x) are affected (2.2.0, 2.2.1, 2.2.2): **YES**
- Issue is stream-scoped (2.2.x): **YES**
- Other streams also affected (2.1.x): **YES**

This triggers **Case A (cross-stream impact)** followed by **Case B (create remediation tasks)**.

#### Case A: Cross-stream impact

The version impact analysis shows that stream 2.1.x is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

Actions:
1. Post cross-stream impact comment to TC-8020:
   > "Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream 2.1.x based on lock file analysis."
2. Check for existing sibling CVE Jiras for stream 2.1.x with label CVE-2026-31812.
3. If no sibling CVE Jira exists for 2.1.x, create preemptive remediation tasks with `security-preemptive` label and "Related" link type to TC-8020.

#### Case B: Create remediation tasks (for 2.2.x stream)

Ecosystem: Cargo (source dependency) -- 2 tasks per stream.

Depending on Step 2.5 (upstream fix check):
- If upstream branch `release/0.4.z` already ships quinn-proto >= 0.11.14: **dependency bump + downstream propagation** (2 tasks)
- If upstream branch does not yet have the fix: **upstream backport + downstream propagation** (2 tasks)

Based on the mock data, v0.4.11 and v0.4.12 already ship 0.11.14, suggesting the upstream fix is available on the release/0.4.z branch. This would use the **dependency bump variant**.

**Remediation tasks for 2.2.x (if proceeding):**

1. **Dependency bump task**: "Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)"
   - Repository: backend
   - Target branch: release/0.4.z
   - Action: `cargo update -p quinn-proto` to pull in >= 0.11.14
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`

2. **Downstream propagation task**: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)"
   - Repository: rhtpa-release.0.4.z
   - Target branch: main
   - Blocked by the dependency bump task
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Preemptive remediation tasks for 2.1.x (if no sibling CVE Jira exists):**

1. **Dependency bump task**: "Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.1)"
   - Repository: backend
   - Target branch: release/0.3.z
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
   - Link type: "Related" to TC-8020

2. **Downstream propagation task**: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)"
   - Repository: rhtpa-release.0.3.z
   - Target branch: main
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
   - Link type: "Related" to TC-8020

#### Step 7.5: Release Jira Orchestration

Before creating remediation tasks, find or create the release Jira structure:
- For 2.2.x: Search for existing release Epic matching "RHTPA 2.2.* Release Tasks"
- If found, find or create release Task "RHTPA <version> CVE triage" under it
- Link remediation tasks to the release Task (Blocks)
- Link TC-8020 to the release Task (Related)

#### VEX Justification

Not applicable -- supported versions ARE affected, so this is not a "Not a Bug" closure.

#### Post-Triage Summary

After all actions complete:
- Add `ai-cve-triaged` label to TC-8020
- Post summary comment with version impact table, Affects Versions correction, remediation task links, and @mention of the issue reporter
- Transition TC-8020 to In Progress

## Key Findings

1. **PSIRT Affects Version is wrong**: RHTPA 2.0.0 does not exist in any configured stream. Must be corrected to RHTPA 2.2.0, 2.2.1, 2.2.2.
2. **Partial impact within scope**: Only 2.2.0, 2.2.1, and 2.2.2 are affected in the 2.2.x stream. Versions 2.2.3+ already ship the fix.
3. **Cross-stream impact**: Stream 2.1.x is also affected and needs preemptive remediation (Case A) if no sibling CVE Jira exists.
4. **Concurrent triage blocks progress**: TC-8019 is actively being triaged on the same upstream component (quinn-proto). The engineer must decide whether to wait, skip, or proceed with overlap labeling before any remediation tasks can be created.
5. **Embargo check triggered**: CVSS 7.5 (High) meets the Critical/Important threshold (>= 7.0). If an Embargo policy URL were configured, Step 1.7 would present an embargo warning gate. The fixture CLAUDE.md does not configure an embargo policy URL, so Step 1.7 is skipped.
