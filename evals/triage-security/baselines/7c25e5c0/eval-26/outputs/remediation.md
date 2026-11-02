# Step 8 — Remediation (Case B: Affected — create remediation tasks)

All 2.2.x versions ship criterion 0.5.1 (< 0.5.2 fix threshold). Remediation is required.

**Dependency scope override applied**: criterion is a dev-only dependency ([dev-dependencies]). Per the dependency scope decision tree:
- Add `dev-dependency` label to all remediation tasks
- Set priority to **Normal** (overriding the CVE severity of CVSS 5.3 Medium)
- Include a dev/build-only note in each task description

Cargo is a source dependency ecosystem → 2 tasks per stream.

---

## Task 1: Upstream Backport Task

**Jira Issue Creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-99001: bump criterion to 0.5.2 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"],
  priority: "Normal"
)
```

**Task Description:**

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: path traversal in benchmark output in criterion.
The vulnerable dependency (criterion < 0.5.2) must be updated to the fixed version (0.5.2+).

> **Note**: This dependency is dev/build-only and is not shipped in production.
> Remediation priority is Normal (supply chain risk only).

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (dev-only)
- **Dependency scope**: `[dev-dependencies]` — criterion is used for benchmarks only and is NOT shipped in production builds
- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml `[dev-dependencies]` section
- Run `cargo update -p criterion` to update Cargo.lock

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)

---

### Post-creation: Description Digest

After creating the upstream task:
1. Re-fetch the task description from Jira: `jira.get_issue(<upstream-task-key>, fields=["description"])`
2. Compute SHA-256 digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
3. Post digest comment BEFORE creating issue links: `jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: sha256-md:<hex>")`

---

## Task 2: Downstream Propagation Subtask

**Jira Issue Creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"],
  priority: "Normal"
)
```

**Task Description:**

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99001 fix from the upstream task.

> **Note**: This dependency is dev/build-only and is not shipped in production.
> Remediation priority is Normal (supply chain risk only).

The upstream backport bumps criterion to 0.5.2 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct (dev-only) — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)

---

### Post-creation: Description Digest

After creating the downstream task:
1. Re-fetch the task description from Jira: `jira.get_issue(<downstream-task-key>, fields=["description"])`
2. Compute SHA-256 digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
3. Post digest comment BEFORE creating issue links: `jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: sha256-md:<hex>")`

---

## Jira Linkage

After task creation and digest comments:

1. Link upstream task to CVE: `jira.create_link(inwardIssue: TC-8050, outwardIssue: <upstream-task-key>, type: "Depend")`
2. Link downstream task to CVE: `jira.create_link(inwardIssue: TC-8050, outwardIssue: <downstream-task-key>, type: "Depend")`
3. Link downstream as blocked by upstream: `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`

## Summary of Dev-Dependency Handling

| Attribute | Standard | Dev-Dependency (Applied) |
|-----------|----------|--------------------------|
| Labels | ai-generated-jira, Security, CVE-ID | ai-generated-jira, Security, CVE-2026-99001, **dev-dependency** |
| Priority | Inherited from CVE severity | **Normal** (overridden) |
| Description note | _(none)_ | **"This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."** |
| Task creation | Yes | **Yes** (supply chain risk) |
