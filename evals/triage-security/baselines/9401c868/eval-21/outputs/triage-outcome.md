# Triage Outcome for TC-8020

## Issue Summary

- **Issue**: TC-8020
- **CVE**: CVE-2026-31812
- **Summary**: CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
- **Library**: quinn-proto
- **Affected range**: versions before 0.11.14
- **Fixed version**: 0.11.14
- **CVSS**: 7.5 (High)
- **Stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Ecosystem**: Cargo (source dependency)
- **Upstream Affected Component**: quinn-proto (customfield_10632)

## Version Impact Summary

### Stream 2.2.x (in scope -- this issue's stream)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 0.11.14 | NO | ships fixed version |

Three versions within the scoped stream are affected (2.2.0, 2.2.1, 2.2.2). Two versions already ship the fixed version (2.2.3, 2.2.4).

### Stream 2.1.x (out of scope -- cross-stream impact)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |

Both 2.1.x versions are affected. These are outside the issue's stream scope and trigger Case A (cross-stream impact).

## Affects Versions Correction (Step 3)

```
Current (PSIRT-assigned): [RHTPA 2.0.0]
Proposed:                 [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

RHTPA 2.0.0 does not correspond to any version in the supportability matrix and is incorrect. The correction is scoped to stream 2.2.x per the issue suffix `[rhtpa-2.2]`. Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14 (the fixed version).

## Triage Decision

### Step 7 -- Concurrent Triage Detection (BLOCKING GATE)

Before proceeding to Case A/B/C branching, Step 7 detected a concurrent triage on the same upstream component (`quinn-proto`):

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

This is a **blocking gate**. The engineer must choose one of three options before any remediation tasks can be created:

1. **Wait** -- Pause until TC-8019's triage completes, then re-run Step 4.3 to detect any cross-CVE overlap. If TC-8019's remediation already bumps quinn-proto >= 0.11.14, TC-8020 can be linked to the existing task instead of creating duplicates.

2. **Skip** -- Skip remediation task creation entirely. Add a Jira comment explaining that task creation was deferred due to concurrent triage on TC-8019.

3. **Proceed** -- Create tasks with a `concurrent-triage-overlap` label so that TC-8019's Step 4.3 cross-CVE overlap detection can catch the overlap later.

**Recommended option**: Wait (Option 1), to avoid duplicate remediation tasks.

### Primary: Case B -- Affected, create remediation tasks (stream 2.2.x)

Pending resolution of the Step 7 concurrent triage gate, the triage outcome for the scoped stream is:

Supported versions within stream 2.2.x (2.2.0, 2.2.1, 2.2.2) ship a vulnerable version of quinn-proto (< 0.11.14). Remediation is required.

**Upstream fix status**: The upstream branch `release/0.4.z` already ships the fixed version (quinn-proto 0.11.14 at tags v0.4.11 and v0.4.12), so the remediation uses the **dependency bump variant** (not upstream backport).

**Planned remediation tasks for stream 2.2.x** (2 tasks -- Cargo source dependency):

1. **Dependency bump task**: "Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)"
   - Repository: rhtpa-backend (backend)
   - Target branch: release/0.4.z
   - Action: `cargo update -p quinn-proto` to pull in version >= 0.11.14
   - Labels: ai-generated-jira, Security, CVE-2026-31812
   - Link: Depend -> TC-8020

2. **Downstream propagation task**: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)"
   - Repository: rhtpa-release.0.4.z (Konflux release repo)
   - Target branch: main
   - Source pinning method: artifacts.lock.yaml (download URL contains tag)
   - Action: Update backend source reference to the merged commit or new release tag
   - Labels: ai-generated-jira, Security, CVE-2026-31812
   - Link: Blocks -> dependency bump task; Depend -> TC-8020

### Secondary: Case A -- Cross-stream impact (stream 2.1.x)

The version impact analysis reveals that stream 2.1.x (outside this issue's scope) is also affected: versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9.

Planned actions:

1. Post a cross-stream impact comment on TC-8020:
   > Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

2. Search for existing CVE Jiras for stream 2.1.x with label CVE-2026-31812.

3. If no sibling CVE Jira exists for stream 2.1.x, create **preemptive remediation tasks**:
   - **Upstream backport task** (since release/0.3.z does NOT ship the fix):
     "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)"
     Labels include `security-preemptive`; linked as "Related" (not "Depend") to TC-8020
   - **Downstream propagation task**:
     "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)"
     Labels include `security-preemptive`; linked as "Related" to TC-8020

4. If a sibling CVE Jira already exists for stream 2.1.x, skip preemptive task creation.

## Release Jira Orchestration (Step 7.5)

If the engineer proceeds past Step 7, Step 7.5 will execute before task creation:

- **Stream 2.2.x**: Resolve to the next patch version based on the latest released version in the supportability matrix (2.2.4 -> default to RHTPA 2.2.5). Search for or create a release Epic ("RHTPA 2.2.5 Release Tasks") and release Task ("RHTPA 2.2.5 CVE triage"). All non-preemptive remediation tasks will be linked to this release Task.
- Step 7.5.3 (Cross-CVE dedup) will check whether an existing remediation Task under the release Task already covers quinn-proto.

## Post-Triage Actions

After all remediation actions are confirmed and executed:

1. **Add `ai-cve-triaged` label** to TC-8020
2. **Post summary comment** to TC-8020 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - Triage outcome and remediation task links
   - Cross-stream impact notice for 2.1.x
   - Concurrent triage detection result and chosen action
   - Release Jira references (Epic and Task keys)
   - @mention of the issue reporter
   - Comment Footnote per shared/comment-footnote.md
3. **Transition** TC-8020 to In Progress (after remediation tasks are created)
