# Step 8 — Remediation

## Case A: Standard Remediation Tasks for Current Stream (rhtpa-2.2)

Since versions in the 2.2.x stream are affected, create standard remediation tasks for the issue's scoped stream.

### Task 1: Upstream Backport Task (rhtpa-2.2)

**Proposed Jira creation (not executed — eval mode):**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Task Description:**

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: tokio use-after-free in task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- Update tokio dependency to >= 1.42.0 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

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
1. Re-fetch description from Jira after create_issue
2. Compute SHA-256 digest using `python3 scripts/sha256-digest.py`
3. Post digest comment: `[sdlc-workflow] Description digest: sha256-md:<hex>`
4. Then create issue links

---

### Task 2: Downstream Propagation Subtask (rhtpa-2.2)

**Proposed Jira creation (not executed — eval mode):**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Task Description:**

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-55123 fix from the upstream backport task.

The upstream backport bumps tokio to 1.42.0 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)

---

**Post-creation steps:**
1. Re-fetch description from Jira after create_issue
2. Compute SHA-256 digest using `python3 scripts/sha256-digest.py`
3. Post digest comment: `[sdlc-workflow] Description digest: sha256-md:<hex>`
4. Then create issue links

---

### Jira Linkage (rhtpa-2.2 standard tasks)

- `Depend`: TC-8020 (inward) → upstream backport task (outward)
- `Depend`: TC-8020 (inward) → downstream propagation task (outward)
- `Blocks`: upstream backport task (inward) → downstream propagation task (outward)

---

## Case B: Preemptive Remediation Tasks for Stream rhtpa-2.1 (No CVE Jira)

Cross-stream analysis detected that stream **rhtpa-2.1** is also affected (tokio 1.40.0 < 1.42.0) but **no sibling CVE Jira exists** for that stream. Per Step 8 Case B, proactive preemptive remediation tasks are created.

### Task 3: Preemptive Upstream Backport Task (rhtpa-2.1)

**Proposed Jira creation (not executed — eval mode):**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Task Description:**

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-55123: tokio use-after-free in task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Update tokio dependency to >= 1.42.0 in Cargo.toml

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8020 (originating CVE from stream rhtpa-2.2)

---

**Post-creation steps:**
1. Re-fetch description from Jira after create_issue
2. Compute SHA-256 digest using `python3 scripts/sha256-digest.py`
3. Post digest comment: `[sdlc-workflow] Description digest: sha256-md:<hex>`
4. Then create issue links

---

### Task 4: Preemptive Downstream Propagation Subtask (rhtpa-2.1)

**Proposed Jira creation (not executed — eval mode):**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Task Description:**

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-55123 fix from the preemptive upstream backport task.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: preemptive upstream backport task (must merge first)
- Related to: TC-8020 (originating CVE from stream rhtpa-2.2)

---

**Post-creation steps:**
1. Re-fetch description from Jira after create_issue
2. Compute SHA-256 digest using `python3 scripts/sha256-digest.py`
3. Post digest comment: `[sdlc-workflow] Description digest: sha256-md:<hex>`
4. Then create issue links

---

### Jira Linkage (rhtpa-2.1 preemptive tasks)

- `Related`: TC-8020 (inward) → preemptive upstream backport task (outward) — **Related** link (not Depend) because the originating CVE belongs to stream rhtpa-2.2, not rhtpa-2.1
- `Related`: TC-8020 (inward) → preemptive downstream propagation task (outward)
- `Blocks`: preemptive upstream backport task (inward) → preemptive downstream propagation task (outward)

### Label Distinction

- **Standard tasks (rhtpa-2.2)**: `["ai-generated-jira", "Security", "CVE-2026-55123"]`
- **Preemptive tasks (rhtpa-2.1)**: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`
