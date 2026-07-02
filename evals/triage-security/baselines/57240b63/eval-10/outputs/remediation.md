# Remediation — TC-8020 (Case A: Current Stream)

## Triage Outcome

**Case A: Affected -- create remediation tasks** for the scoped stream (rhtpa-2.2 / 2.2.x).

All versions in stream 2.2.x (RHTPA 2.2.0, RHTPA 2.2.1) ship tokio 1.41.1, which is below the fix threshold of 1.42.0.

Ecosystem: **Cargo** (source dependency) -- requires **two tasks**: upstream backport + downstream propagation.

---

## Task 1: Upstream Backport Task (rhtpa-2.2)

### PROPOSAL: Create Jira Task

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: Use-after-free in task abort in the tokio crate.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1)
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1)

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Update tokio dependency to >= 1.42.0 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (parent tracking issue)

### Post-Creation Actions

```
# Post description digest comment
jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: sha256-md:<hex>")

# Link to Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

---

## Task 2: Downstream Propagation Subtask (rhtpa-2.2)

### PROPOSAL: Create Jira Task

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps tokio to 1.42.0
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

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)

### Post-Creation Actions

```
# Post description digest comment
jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: sha256-md:<hex>")

# Link downstream subtask as blocked by upstream task
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)

# Link to Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)
```

---

## Post-Triage Actions

### Add ai-cve-triaged label

```
PROPOSAL: jira.edit_issue("TC-8020", fields={
  "labels": ["CVE-2026-55123", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### Post Summary Comment

```
PROPOSAL: jira.add_comment("TC-8020", <summary-comment>)
```

Summary comment content:

---

**Triage Summary for TC-8020 (CVE-2026-55123)**

**Version Impact:**

| Version | tokio version | Affected? | Notes |
|---------|---------------|-----------|-------|
| RHTPA 2.1.0 | 1.40.0 | YES | stream rhtpa-2.1 (out of scope) |
| RHTPA 2.1.1 | 1.40.0 | YES | stream rhtpa-2.1 (out of scope) |
| RHTPA 2.2.0 | 1.41.1 | YES | stream rhtpa-2.2 (in scope) |
| RHTPA 2.2.1 | 1.41.1 | YES | stream rhtpa-2.2 (in scope) |

**Affects Versions:** RHTPA 2.2.0, RHTPA 2.2.1 (correct as assigned by PSIRT)

**Triage outcome:** Case A -- remediation tasks created for stream rhtpa-2.2.

**Remediation tasks created:**
- <upstream-task-key> -- upstream backport: bump tokio to >= 1.42.0 on release/0.4.z
- <downstream-task-key> -- downstream propagation: update backend ref in rhtpa-release.0.4.z (blocked by <upstream-task-key>)

**Cross-stream impact:** Stream rhtpa-2.1 is also affected (tokio 1.40.0). Preemptive remediation tasks created (see cross-stream comment).

@<reporter> (reporter mention via ADF mention node)

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/mrizzi/sdlc-plugins) v0.11.1.
