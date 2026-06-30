# Step 7 -- Post-Triage Summary: TC-8001

## Triage Outcome

**Case A (Affected) + Case B (Cross-stream impact)**

The 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2) that ship quinn-proto < 0.11.14. Remediation tasks are needed for the scoped stream. Additionally, the 2.1.x stream is also affected (cross-stream impact).

## Proposed Actions

### 1. Add `ai-cve-triaged` label to TC-8001

```
jira.edit_issue("TC-8001", fields={
  "labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 2. Remediation Tasks for Stream 2.2.x (scoped stream)

Since quinn-proto is a Cargo (source dependency) ecosystem, **two tasks** are created:

#### Task 1: Upstream Backport Task

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"],
  description: <see below>
)
```

**Description:**

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

#### Task 2: Downstream Propagation Subtask

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"],
  description: <see below>
)
```

**Description:**

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

### 3. Jira Linkage (proposed)

```
# Link upstream task to vulnerability
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")

# Link downstream subtask as blocked by upstream task
jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")

# Link downstream task to vulnerability
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")

# Transition vulnerability to In Progress
jira.transition_issue("TC-8001", status: "In Progress")
```

### 4. Cross-Stream Impact Notice (Case B)

Stream 2.1.x is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). Since this issue is scoped to 2.2.x, the 2.1.x impact is reported as cross-stream impact.

**Proposed cross-stream comment on TC-8001:**

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. Versions 2.1.0 (v0.3.8, quinn-proto 0.11.9) and 2.1.1 (v0.3.12, quinn-proto 0.11.9) are affected. This stream is tracked by a companion issue (see Related links) or may require separate PSIRT triage.

If no companion CVE Jira exists for the 2.1.x stream, preemptive remediation tasks would be created with the `security-preemptive` label and "Related" link type (per Case B procedures).

---

## Post-Triage Summary Comment

The following summary comment would be posted to TC-8001:

---

**CVE-2026-31812 Triage Summary -- quinn-proto < 0.11.14**

**Version Impact:**

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | out-of-scope stream |
| 2.1.1 | 2.1.x | 0.11.9 | YES | out-of-scope stream |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

**Affects Versions Correction:**
[RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
RHTPA 2.0.0 was removed (no 2.0.x stream exists). Corrected to stream 2.2.x affected versions based on lock file evidence.

**Triage Outcome:** Remediation required (Case A -- affected versions found in scoped stream 2.2.x).

**Remediation Tasks Created:**
- Upstream backport task: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)
- Downstream propagation task: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2) (blocked by upstream task)

**Cross-Stream Impact (Case B):**
Stream 2.1.x is also affected (2.1.0, 2.1.1 ship quinn-proto 0.11.9). Preemptive remediation tasks created for 2.1.x or tracked by companion PSIRT issue.

{"type":"mention","attrs":{"id":"557058:psirt-analyst-mock-id","text":"@psirt-analyst"}}

---

This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/mrizzi/sdlc-plugins) v0.11.0.
