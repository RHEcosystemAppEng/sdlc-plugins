# Step 8 -- Remediation

## Case A: Standard Remediation Tasks (current stream rhtpa-2.2)

Since the current stream (rhtpa-2.2) has affected versions, create standard remediation tasks.

### Upstream Backport Task (rhtpa-2.2)

**Proposed Jira issue creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Labels:** `["ai-generated-jira", "Security", "CVE-2026-55123"]`

**Task Description:**

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: tokio use-after-free in task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (parent tracking issue)

---

**Post-creation steps:**
1. Re-fetch description from Jira API
2. Compute SHA-256 digest via `python3 scripts/sha256-digest.py`
3. Post digest comment: `[sdlc-workflow] Description digest: <tagged-digest>`
4. Create Depend link: TC-8020 -> <upstream-task-key>

### Downstream Propagation Subtask (rhtpa-2.2)

**Proposed Jira issue creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Labels:** `["ai-generated-jira", "Security", "CVE-2026-55123"]`

**Task Description:**

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps tokio to 1.42.0
on release/0.4.z. Once that PR merges, update the source pinning in this
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
- Depends on: TC-8020 (parent tracking issue)

---

**Post-creation steps:**
1. Re-fetch description from Jira API
2. Compute SHA-256 digest via `python3 scripts/sha256-digest.py`
3. Post digest comment: `[sdlc-workflow] Description digest: <tagged-digest>`
4. Create Depend link: TC-8020 -> <downstream-task-key>
5. Create Blocks link: <upstream-task-key> -> <downstream-task-key>

---

## Case B: Proactive Preemptive Remediation (stream rhtpa-2.1)

Cross-stream version impact analysis reveals that stream **rhtpa-2.1** is also affected (tokio 1.40.0, threshold 1.42.0). A JQL search for sibling CVE Jiras with label `CVE-2026-55123` in stream rhtpa-2.1 returns **no results** -- no CVE Jira exists for that stream.

Per Step 8 Case B, create proactive preemptive remediation tasks for stream rhtpa-2.1.

### Preemptive Upstream Backport Task (rhtpa-2.1)

**Proposed Jira issue creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Labels:** `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`

**Task Description:**

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-55123: tokio use-after-free in task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)

---

**Post-creation steps:**
1. Re-fetch description from Jira API
2. Compute SHA-256 digest via `python3 scripts/sha256-digest.py`
3. Post digest comment: `[sdlc-workflow] Description digest: <tagged-digest>`
4. Create **Related** link (not Depend): TC-8020 <-> <preemptive-upstream-task-key>

### Preemptive Downstream Propagation Subtask (rhtpa-2.1)

**Proposed Jira issue creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Labels:** `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`

**Task Description:**

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps tokio to 1.42.0
on release/0.3.z. Once that PR merges, update the source pinning in this
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

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)

---

**Post-creation steps:**
1. Re-fetch description from Jira API
2. Compute SHA-256 digest via `python3 scripts/sha256-digest.py`
3. Post digest comment: `[sdlc-workflow] Description digest: <tagged-digest>`
4. Create **Related** link: TC-8020 <-> <preemptive-downstream-task-key>
5. Create Blocks link: <preemptive-upstream-task-key> -> <preemptive-downstream-task-key>

---

All actions above are **proposals** requiring engineer confirmation before execution.
