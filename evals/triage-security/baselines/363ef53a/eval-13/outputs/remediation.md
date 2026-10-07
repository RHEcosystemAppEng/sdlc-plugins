# Step 8 -- Remediation: CVE-2026-31812

## Triage Decision

- Issue scoped to stream: **2.2.x**
- Affected versions in scope: 2.2.0, 2.2.1, 2.2.2
- Cross-stream impact: 2.1.x (versions 2.1.0, 2.1.1 also affected)
- Ecosystem: Cargo (source dependency)
- Upstream fix status on release/0.4.z: **YES** (0.11.14 at HEAD)
- Upstream fix status on release/0.3.z: **NO** (0.11.9 at HEAD)
- Path: **Case A** (cross-stream impact) then **Case B** (create remediation tasks)

## Case A: Cross-Stream Impact Comment

The following comment would be posted to TC-8001:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x
> based on lock file analysis. These streams are tracked by companion issues
> (see Related links) or may require separate PSIRT triage.

Since no sibling CVE Jira exists for stream 2.1.x, preemptive remediation tasks
are created for that stream (see below).

---

## Case B: Remediation Tasks for Stream 2.2.x (In-Scope)

Since the upstream branch `release/0.4.z` already ships quinn-proto 0.11.14
(Step 2.5 confirms fix is available), the **dependency bump** variant is used
instead of the upstream backport variant.

### Task 1: Dependency Bump (2.2.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

```markdown
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Jira linkage:**
```
jira.create_link(inwardIssue: "TC-8001", outwardIssue: "<bump-task-key>", type: "Depend")
```

#### Description Digest Comment for Task 1

After creating the dependency bump task, the following steps would be performed:

1. Re-fetch the created task's description from Jira:
   ```
   jira.get_issue(<bump-task-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This produces a tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`
3. Post the digest as a standalone comment on the task (before any other comments or links):
   ```
   jira.add_comment(<bump-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py`.

---

### Task 2: Downstream Propagation (2.2.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

```markdown
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <bump-task-key>.

The dependency bump (<bump-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <bump-task-key> (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Jira linkage:**
```
jira.create_link(inwardIssue: "TC-8001", outwardIssue: "<downstream-task-key>", type: "Depend")
jira.create_link(inwardIssue: "<bump-task-key>", outwardIssue: "<downstream-task-key>", type: "Blocks")
```

#### Description Digest Comment for Task 2

After creating the downstream propagation task, the following steps would be performed:

1. Re-fetch the created task's description from Jira:
   ```
   jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This produces a tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`
3. Post the digest as a standalone comment on the task (before any other comments or links):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py`.

---

## Case A: Preemptive Remediation Tasks for Stream 2.1.x (Out-of-Scope)

Stream 2.1.x has no sibling CVE Jira for CVE-2026-31812, so preemptive tasks
are created. The upstream branch `release/0.3.z` does NOT have the fix at HEAD
(quinn-proto 0.11.9), so the **upstream backport** variant is used.

### Task 3: Upstream Backport -- Preemptive (2.1.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

```markdown
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto - Panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0, 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Jira linkage (preemptive -- uses "Related" not "Depend"):**
```
jira.create_link(inwardIssue: "TC-8001", outwardIssue: "<preemptive-upstream-task-key>", type: "Related")
```

#### Description Digest Comment for Task 3

After creating the preemptive upstream backport task, the following steps would be performed:

1. Re-fetch the created task's description from Jira:
   ```
   jira.get_issue(<preemptive-upstream-task-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This produces a tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`
3. Post the digest as a standalone comment on the task (before any other comments or links):
   ```
   jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py`.

---

### Task 4: Downstream Propagation -- Preemptive (2.1.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Jira linkage (preemptive -- uses "Related" not "Depend"):**
```
jira.create_link(inwardIssue: "TC-8001", outwardIssue: "<preemptive-downstream-task-key>", type: "Related")
jira.create_link(inwardIssue: "<preemptive-upstream-task-key>", outwardIssue: "<preemptive-downstream-task-key>", type: "Blocks")
```

#### Description Digest Comment for Task 4

After creating the preemptive downstream propagation task, the following steps would be performed:

1. Re-fetch the created task's description from Jira:
   ```
   jira.get_issue(<preemptive-downstream-task-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This produces a tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`
3. Post the digest as a standalone comment on the task (before any other comments or links):
   ```
   jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py`.

---

## Preemptive Tasks Comment on TC-8001

The following comment would be posted to TC-8001 after creating preemptive tasks:

> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: <preemptive-upstream-task-key> (upstream backport, security-preemptive),
>   <preemptive-downstream-task-key> (downstream propagation, security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive
> label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
> reconciliation will link them and remove the label.

---

## Pre-Creation Checklist

- [x] **Task count per stream**: 2.2.x has 2 tasks (dependency bump + downstream propagation); 2.1.x has 2 preemptive tasks (upstream backport + downstream propagation). Matches ecosystem classification table (source dependency = 2 tasks).
- [x] **Cross-stream coverage**: 2.1.x (outside issue scope) has preemptive tasks created (no existing sibling CVE Jira found).
- [x] **Link types**: "Depend" for tasks linked to TC-8001 (in-scope 2.2.x tasks), "Related" for preemptive tasks linked to TC-8001 (out-of-scope 2.1.x tasks), "Blocks" for upstream-to-downstream within each stream.
- [x] **Preemptive labels**: 2.1.x tasks carry the `security-preemptive` label.
- [x] **Coordination guidance**: each task includes upstream coordination guidance (deployment context defaults to upstream since Source Repositories table has no Deployment Context column).
- [x] **Release Jira linking**: would be performed after Step 7.5 orchestration (not shown in this eval since no release Epic/Task data is provided in fixtures).
- [x] **Dedup consistency**: no dedup detected (no prior remediation tasks exist for this component in fixtures).

## Summary of All Tasks

| # | Task | Stream | Type | Labels | Link to TC-8001 |
|---|------|--------|------|--------|-----------------|
| 1 | Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2) | 2.2.x | Dependency bump | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 2 | Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2) | 2.2.x | Downstream propagation | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 3 | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1) | 2.1.x | Upstream backport (preemptive) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| 4 | Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | 2.1.x | Downstream propagation (preemptive) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
