# Step 8 -- Remediation

## Triage Outcome: Case A -- Affected, create remediation tasks

The version impact analysis shows mixed results:
- **2.1.x stream**: ALL versions affected (h2 0.4.5, < 0.4.8)
- **2.2.x stream**: NO versions affected (h2 >= 0.4.8, already ships the fix)

**Cross-stream impact notice (Case B) is NOT generated** because this issue is unscoped -- it covers all streams by definition. Case B applies only to scoped issues (those with a stream suffix). For unscoped issues, remediation tasks are created directly for all affected streams without a cross-stream notice.

Remediation tasks are created **only for the affected stream (2.1.x)**, not for the 2.2.x stream which already ships the patched version. Since the ecosystem is **Cargo** (a source dependency ecosystem), two tasks are created per affected stream: an upstream backport task and a downstream propagation subtask (Important Rule 8).

---

## Task 1: Upstream Backport Task (Source Repository Fix -- 2.1.x stream)

**PROPOSED** Jira issue creation:

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

```markdown
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed
version (0.4.8+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z (from Ecosystem Mappings Upstream Branch)
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.toml / Cargo.lock
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

### Post-creation linkage

1. Post description digest comment (BEFORE links)
2. Link to TC-8004 via "Depend"

---

## Task 2: Downstream Propagation Subtask (Konflux Release Repo Update -- 2.1.x stream)

**PROPOSED** Jira issue creation:

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

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.8 on
release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
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

### Post-creation linkage

1. Post description digest comment (BEFORE links)
2. Link downstream blocked by upstream via "Blocks"
3. Link to TC-8004 via "Depend"

---

## No Tasks for 2.2.x Stream

No remediation tasks are created for the 2.2.x stream because all versions in that stream already ship h2 >= 0.4.8 (the fixed version). The 2.2.x stream is not affected.

---

## Post-Triage Summary

**PROPOSED** actions after remediation task creation:

1. Add `ai-cve-triaged` label to TC-8004
2. Post summary comment on TC-8004 documenting version impact, Affects Versions correction, and remediation tasks created
3. Transition TC-8004 to In Progress

All actions above are **proposals** requiring engineer confirmation before execution.
