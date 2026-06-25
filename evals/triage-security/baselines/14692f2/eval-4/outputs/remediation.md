# Step 7 -- Remediation: TC-8004

## Triage Outcome

**Case A: Affected -- create remediation tasks** for the 2.1.x stream only.

The version impact analysis shows:
- **2.1.x stream**: AFFECTED (h2 0.4.5 < fix threshold 0.4.8) -- remediation required
- **2.2.x stream**: NOT AFFECTED (h2 >= 0.4.8 in all versions) -- no remediation needed

Since the issue is **unscoped** (covers all streams), there is no cross-stream impact notice (Case B does not apply). The unscoped issue already spans all streams, so there are no "other streams outside this issue's scope." Remediation tasks are created only for the actually affected stream (2.1.x).

## Ecosystem

**Cargo** (source dependency) -- two tasks required per the remediation templates:
1. Upstream backport task (fix in source repo)
2. Downstream propagation subtask (update reference in Konflux release repo)

---

## Task 1: Upstream Backport (2.1.x stream)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Task Description

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 versions before 0.4.8) must be updated
to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- h2 is a transitive dependency via hyper -- check if hyper needs
  a version bump or if h2 can be pinned directly
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

### Post-Creation Actions

1. Post description digest comment per `shared/description-digest-protocol.md`
2. Link to TC-8004 with "Depend" link type

---

## Task 2: Downstream Propagation (2.1.x stream)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Task Description

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.8 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

### Post-Creation Actions

1. Post description digest comment per `shared/description-digest-protocol.md`
2. Link to TC-8004 with "Depend" link type
3. Link upstream task to this downstream task with "Blocks" link type (upstream blocks downstream)

---

## No Remediation for 2.2.x Stream

The 2.2.x stream does NOT require remediation. All versions in the 2.2.x stream ship h2 >= 0.4.8:

| Version | h2 version | Status |
|---------|------------|--------|
| 2.2.0 | 0.4.8 | Ships fix version |
| 2.2.1 | 0.4.8 | Ships fix version |
| 2.2.2 | -- | Retag of 2.2.1 (ships fix) |
| 2.2.3 | 0.4.9 | Above fix version |
| 2.2.4 | 0.4.9 | Above fix version |

No tasks are created for this stream.

---

## Post-Triage Summary

### Label Addition

Add `ai-cve-triaged` label to TC-8004.

### Summary Comment (proposed)

```
Triage complete for CVE-2026-33501 (h2 memory exhaustion via CONTINUATION frames).

Version Impact:

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | |
| 2.1.1 | 2.1.x | 0.4.5 | YES | |
| 2.2.0 | 2.2.x | 0.4.8 | NO | ships fix version |
| 2.2.1 | 2.2.x | 0.4.8 | NO | ships fix version |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | above fix version |
| 2.2.4 | 2.2.x | 0.4.9 | NO | above fix version |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]

Outcome: Remediation tasks created for 2.1.x stream only.
- <upstream-task-key>: Upstream backport (bump h2 to 0.4.8 on release/0.3.z)
- <downstream-task-key>: Downstream propagation (update rhtpa-backend ref in rhtpa-release.0.3.z, blocked by upstream task)

2.2.x stream: No remediation needed -- all versions ship h2 >= 0.4.8.

No sibling issues found (JQL returned empty).

---
[sdlc-workflow:triage-security]
```
