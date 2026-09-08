# Step 8 -- Remediation for CVE-2026-31812

## Triage Outcome: Case B (Affected) + Case A (Cross-Stream Impact)

The issue is scoped to **2.2.x**. Within this stream, versions 2.2.0, 2.2.1, and 2.2.2 are affected. The ecosystem is **Cargo** (source dependency), which requires **2 tasks per stream**: an upstream backport task and a downstream propagation task.

Additionally, the **2.1.x** stream is also affected (Case A -- cross-stream impact), requiring preemptive remediation tasks for that stream (assuming no sibling CVE Jira exists for 2.1.x).

---

## Tasks for Stream 2.2.x (In-Scope -- Standard Remediation)

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5, quinn-proto 0.11.9), 2.2.1 (v0.4.8, quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct or transitive (to be determined by inspecting Cargo.toml)

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (see dependency
  chain above)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes,
no release available with the fix):
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct
  dependency, overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Linkage**: Link to TC-8001 with type "Depend"

#### Description Digest Comment for Task 1

After creating this task, the following steps would be performed to post a description digest comment:

1. **Fetch the created task's description** from Jira:
   ```
   jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. **Write the description** to a temp file (`/tmp/task-desc.md`)
3. **Compute the digest** using:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a tagged digest like `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`
4. **Post the digest comment** on the newly created task:
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from step 3 (e.g., `sha256-md:a1b2c3d4...64chars`)

This digest comment is posted **before** creating issue links or other comments on the task.

---

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct or transitive -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Linkage**:
- Link to TC-8001 with type "Depend"
- Link to upstream-task-key with type "Blocks" (upstream blocks downstream)

#### Description Digest Comment for Task 2

After creating this task, the following steps would be performed:

1. **Fetch the created task's description** from Jira:
   ```
   jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. **Write the description** to a temp file (`/tmp/task-desc.md`)
3. **Compute the digest** using:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
4. **Post the digest comment** on the newly created task:
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

This digest comment is posted **before** creating issue links or other comments on the task.

---

## Tasks for Stream 2.1.x (Out-of-Scope -- Preemptive Remediation, Case A)

Since the 2.1.x stream is affected but outside the issue's scope (TC-8001 is scoped to 2.2.x), these are **preemptive** remediation tasks. They carry the `security-preemptive` label and use "Related" link type to TC-8001 (not "Depend").

### Task 3: Upstream Backport (2.1.x) -- Preemptive

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8, quinn-proto 0.11.9), 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct or transitive (to be determined by inspecting Cargo.toml)

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (see dependency
  chain above)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes,
no release available with the fix):
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct
  dependency, overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating CVE -- Related link, not Depend)
```

**Linkage**: Link to TC-8001 with type "Related" (preemptive -- not scoped to this CVE issue's stream)

#### Description Digest Comment for Task 3

After creating this task, the following steps would be performed:

1. **Fetch the created task's description** from Jira:
   ```
   jira.get_issue(<preemptive-upstream-task-key>, fields=["description"])
   ```
2. **Write the description** to a temp file (`/tmp/task-desc.md`)
3. **Compute the digest** using:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
4. **Post the digest comment** on the newly created task:
   ```
   jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

This digest comment is posted **before** creating issue links or other comments on the task.

---

### Task 4: Downstream Propagation (2.1.x) -- Preemptive

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct or transitive -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (originating CVE -- Related link, not Depend)
```

**Linkage**:
- Link to TC-8001 with type "Related" (preemptive)
- Link to preemptive-upstream-task-key with type "Blocks" (upstream blocks downstream)

#### Description Digest Comment for Task 4

After creating this task, the following steps would be performed:

1. **Fetch the created task's description** from Jira:
   ```
   jira.get_issue(<preemptive-downstream-task-key>, fields=["description"])
   ```
2. **Write the description** to a temp file (`/tmp/task-desc.md`)
3. **Compute the digest** using:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
4. **Post the digest comment** on the newly created task:
   ```
   jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

This digest comment is posted **before** creating issue links or other comments on the task.

---

## Post-Triage Summary

After all tasks are created, the following actions would be performed on TC-8001:

1. **Add label** `ai-cve-triaged` to TC-8001

2. **Post summary comment** to TC-8001:

> Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):
>
> | Version | quinn-proto | Affected? | Notes |
> |---------|-------------|-----------|-------|
> | 2.1.0 | 0.11.9 | YES | |
> | 2.1.1 | 0.11.9 | YES | |
> | 2.2.0 | 0.11.9 | YES | |
> | 2.2.1 | 0.11.12 | YES | |
> | 2.2.2 | -- | YES | retag of 2.2.1 |
> | 2.2.3 | 0.11.14 | NO | |
> | 2.2.4 | 0.11.14 | NO | |
>
> Affects Versions corrected: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
> Based on lock file analysis at pinned commits from security-matrix.md.
> Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
>
> Remediation tasks created (2.2.x stream):
> - <upstream-task-key> (upstream backport: bump quinn-proto to 0.11.14 on release/0.4.z)
> - <downstream-task-key> (downstream propagation: update rhtpa-backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)
>
> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: <preemptive-upstream-task-key> (security-preemptive, upstream backport on release/0.3.z)
> - 2.1.x: <preemptive-downstream-task-key> (security-preemptive, downstream propagation in rhtpa-release.0.3.z)
>
> These preemptive tasks use the "Related" link type and carry the security-preemptive
> label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will
> link them and remove the label.
>
> @<reporter-name> (reporter mention via ADF mention node)
>
> ---
> This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.9.

3. **Post cross-stream impact comment** to TC-8001:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.
>
> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: <preemptive-upstream-task-key> (security-preemptive)
> - 2.1.x: <preemptive-downstream-task-key> (security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive
> label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
> reconciliation will link them and remove the label.
>
> ---
> This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.9.
