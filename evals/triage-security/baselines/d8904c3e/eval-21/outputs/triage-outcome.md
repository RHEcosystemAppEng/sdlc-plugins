# Triage Outcome -- TC-8020 (CVE-2026-31812)

## Issue Summary

| Field | Value |
|-------|-------|
| Issue Key | TC-8020 |
| CVE ID | CVE-2026-31812 |
| Vulnerable Library | quinn-proto |
| Fixed Version | 0.11.14 |
| CVSS | 7.5 (High) |
| Stream Scope | 2.2.x (from summary suffix `[rhtpa-2.2]`) |
| Ecosystem | Cargo (source dependency) |
| Upstream Affected Component | quinn-proto (customfield_10632) |

## Version Impact Summary

### Stream 2.2.x (in scope)

| Version | quinn-proto Version | Affected? |
|---------|---------------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | 0.11.12 (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO (ships fixed version) |
| 2.2.4 | 0.11.14 | NO (ships fixed version) |

### Stream 2.1.x (out of scope -- cross-stream impact)

| Version | quinn-proto Version | Affected? |
|---------|---------------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

## Affects Versions Correction (Step 3)

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Proposed (from lock file analysis)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Rationale**: RHTPA 2.0.0 does not correspond to any configured version stream. Lock file analysis at pinned commits confirms versions 2.2.0 through 2.2.2 ship quinn-proto < 0.11.14. Versions 2.2.3 and 2.2.4 ship the fixed version 0.11.14 and are excluded.

## Triage Decision

### Applicable Cases

**Case B (Affected)**: Supported versions within the issue's stream scope (2.2.0, 2.2.1, 2.2.2) are affected. Remediation tasks are needed.

**Case A (Cross-stream impact)**: The 2.1.x stream is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). Since this is a scoped issue (`[rhtpa-2.2]`), Case A applies -- a cross-stream impact comment should be posted, and proactive remediation tasks should be considered for 2.1.x if no sibling CVE Jira exists for that stream.

### Step 7 -- Concurrent Triage Gate

Before proceeding to Case A/B task creation, Step 7 detected a concurrent triage:

- **TC-8019** is In Progress, assigned to engineer-b@example.com, and also affects the quinn-proto upstream component.
- The engineer must choose one of three options (wait, skip, or proceed with `concurrent-triage-overlap` label) before remediation tasks can be created.

### Remediation Plan (contingent on Step 7 resolution)

If the engineer chooses to **proceed** (Option 3) or **wait** and then re-run:

#### For stream 2.2.x (in scope -- Case B):

Since quinn-proto is a Cargo (source dependency) ecosystem, **2 tasks** would be created:

1. **Upstream backport task**: Bump quinn-proto to >= 0.11.14 on the `release/0.4.z` branch of rhtpa-backend. This addresses the vulnerability in the source repository.

2. **Downstream propagation task**: Update `artifacts.lock.yaml` in rhtpa-release.0.4.z to reference the new backend build that includes the quinn-proto fix. This task is blocked by the upstream backport task.

Both tasks would be linked to TC-8020 with link type "Depend".

#### For stream 2.1.x (out of scope -- Case A):

A cross-stream impact comment would be posted to TC-8020:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. Stream 2.1.x ships quinn-proto 0.11.9 in all versions (2.1.0, 2.1.1). These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

If no sibling CVE Jira exists for 2.1.x, proactive remediation tasks would be created with the `security-preemptive` label and "Related" link type to TC-8020.

### If the engineer chooses to **skip** (Option 2):

No remediation tasks would be created. A Jira comment would be added to TC-8020 explaining that task creation was skipped due to concurrent triage on the same component (TC-8019 in progress by engineer-b@example.com).

### If the engineer chooses to **wait** (Option 1):

Execution stops. The engineer should re-run triage after TC-8019's triage completes. At that point, Step 4.3 (cross-CVE overlap detection) may find that TC-8019's remediation already bumps quinn-proto past 0.11.14, potentially covering TC-8020's fix threshold and eliminating the need for new remediation tasks.

## Post-Triage Actions (after Step 7 resolution and task creation)

1. **Add `ai-cve-triaged` label** to TC-8020
2. **Post summary comment** to TC-8020 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - Triage outcome and links to remediation tasks
   - @mention of the issue reporter (PSIRT analyst)
   - Comment Footnote per `shared/comment-footnote.md`
