# Triage Outcome for TC-8021

## Summary

CVE-2026-31812 affects quinn-proto versions before 0.11.14 (denial of service via panic on large stream counts). The issue is scoped to the **2.2.x** stream. Three versions within that stream are affected (2.2.0, 2.2.1, 2.2.2), while two versions are already fixed (2.2.3, 2.2.4). The 2.1.x stream is also affected (both 2.1.0 and 2.1.1) but falls outside this issue's scope.

## Triage Decision: Case B (Affected) + Case A (Cross-Stream Impact)

### Case B -- Remediation Tasks for 2.2.x (In-Scope Stream)

Since quinn-proto is a **Cargo** (source dependency) ecosystem, **two tasks** are created per the ecosystem classification table:

#### Task 1: Upstream Backport

- **Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)
- **Repository**: rhtpa-backend
- **Target Branch**: release/0.4.z
- **Description**: Bump quinn-proto dependency to >= 0.11.14 in Cargo.lock on the release/0.4.z branch. The upstream fix is available at quinn-rs/quinn#2048. Advisory: GHSA-2026-qp73-x4mq.
- **Affected versions**: 2.2.0 (v0.4.5, quinn-proto 0.11.9), 2.2.1 (v0.4.8, quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1)
- **Labels**: ai-generated-jira, Security, CVE-2026-31812
- **Link**: Depend on TC-8021

Note: The upstream branch (release/0.4.z) already has the fix at v0.4.11+ (quinn-proto 0.11.14). The upstream backport task verifies the fix is present and creates any necessary commits if needed. Since v0.4.11 already ships 0.11.14, the upstream fix may already be merged, and the task may be immediately closable after verification.

#### Task 2: Downstream Propagation

- **Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
- **Repository**: rhtpa-release.0.4.z (Konflux release repo)
- **Target Branch**: main
- **Description**: Update the rhtpa-backend source reference in the Konflux release repo to pick up the quinn-proto fix. Source pinning method: artifacts.lock.yaml (download URL contains tag).
- **Labels**: ai-generated-jira, Security, CVE-2026-31812
- **Links**: Depend on TC-8021, Blocked by upstream task
- **Note**: Since versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already ship the fixed quinn-proto 0.11.14, no new downstream propagation is needed for the latest releases. This task applies only if a rebuild of 2.2.0-2.2.2 era images is required.

### Case A -- Cross-Stream Impact for 2.1.x

The version impact analysis reveals that the **2.1.x stream** is also affected:
- 2.1.0 (v0.3.8): quinn-proto 0.11.9 -- AFFECTED
- 2.1.1 (v0.3.12): quinn-proto 0.11.9 -- AFFECTED

Since this issue is scoped to 2.2.x, the 2.1.x impact triggers Case A (cross-stream impact):

1. **Cross-stream impact comment** posted to TC-8021:
   > Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by a companion issue (see Related links) or may require separate PSIRT triage.

2. **Check for sibling CVE Jiras** for 2.1.x:
   - Search: `project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8021`
   - If a sibling exists for 2.1.x (with suffix `[rhtpa-2.1]`): link as Related and skip preemptive task creation for that stream
   - If no sibling exists: create preemptive remediation tasks for 2.1.x

3. **Preemptive remediation tasks for 2.1.x** (if no sibling CVE Jira exists):

   - **Upstream backport (preemptive)**:
     - Summary: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)
     - Repository: rhtpa-backend
     - Target Branch: release/0.3.z
     - Labels: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
     - Link type: Related to TC-8021 (not Depend, since this is cross-stream)
     - Description prefix: Preemptive remediation from cross-stream analysis of TC-8021 (stream 2.2.x)

   - **Downstream propagation (preemptive)**:
     - Summary: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
     - Repository: rhtpa-release.0.3.z
     - Target Branch: main
     - Labels: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
     - Link type: Related to TC-8021, Blocked by upstream preemptive task

### Affects Versions Correction (Step 3)

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Proposed (scoped to 2.2.x)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Rationale**: RHTPA 2.0.0 does not exist in the supportability matrix. Lock file analysis at pinned commits shows quinn-proto 0.11.9 in 2.2.0, 0.11.12 in 2.2.1, and 2.2.2 is a retag of 2.2.1. All three versions ship quinn-proto below the fix threshold of 0.11.14. Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14) and are excluded.

### Step 7 -- Concurrent Triage

No concurrent triages detected for the quinn-proto component (zero JQL results). Proceeded to remediation without delay.

### Post-Triage Actions

1. **Add label** `ai-cve-triaged` to TC-8021
2. **Transition** TC-8021 to In Progress
3. **Post summary comment** to TC-8021 documenting:
   - Version impact table (all streams)
   - Affects Versions correction (RHTPA 2.0.0 to RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Remediation tasks created (upstream + downstream for 2.2.x)
   - Cross-stream impact notice (2.1.x also affected)
   - Preemptive tasks created for 2.1.x (if applicable)
   - @mention of the issue reporter (PSIRT analyst)
   - Comment Footnote per shared/comment-footnote.md (skill: triage-security)

## Version Impact Table (Complete)

| Stream | Version | quinn-proto | Affected? | Notes |
|--------|---------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.11.9 | YES | Outside issue scope (cross-stream) |
| 2.1.x | 2.1.1 | 0.11.9 | YES | Outside issue scope (cross-stream) |
| 2.2.x | 2.2.0 | 0.11.9 | YES | In scope |
| 2.2.x | 2.2.1 | 0.11.12 | YES | In scope |
| 2.2.x | 2.2.2 | -- | YES | Retag of 2.2.1; in scope |
| 2.2.x | 2.2.3 | 0.11.14 | NO | Fixed version |
| 2.2.x | 2.2.4 | 0.11.14 | NO | Fixed version |
