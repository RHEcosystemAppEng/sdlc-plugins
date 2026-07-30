# Step 8 -- Remediation: CVE-2026-31812

## Triage Outcome

**Case B** -- Affected versions exist in the scoped stream (2.2.x). Create remediation tasks.

Additionally, **Case A** applies -- the 2.1.x stream is also affected but outside the issue's scope. Post cross-stream impact comment and create preemptive remediation tasks for 2.1.x if no companion CVE Jira exists.

## Ecosystem Classification

- **Ecosystem**: Cargo (source dependency)
- **Tasks per stream**: 2 (upstream backport + downstream propagation)

---

## Remediation Tasks for Stream 2.2.x (Scoped Stream)

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (retag of v0.4.8)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (quinn-proto is a direct dependency in Cargo.toml)

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Jira API call**:
```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <upstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

#### Description Digest Comment (upstream backport 2.2.x)

After creating the upstream backport task, post the description digest comment:

1. **Re-fetch the description** from the newly created task:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write description to temp file and compute digest**:
   ```bash
   # Write the fetched description to a temp file
   cat > /tmp/task-desc.md << 'DESCEOF'
   <fetched description content>
   DESCEOF

   # Compute the SHA-256 digest using the project script
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex> (or sha256-adf:<64-char-hex> if REST API returned ADF)
   ```

3. **Post the digest comment** on the upstream task:
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3...64chars`).

4. **Post digest comment before any links or other comments** -- this comment must be the first comment on the task.

---

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Jira API call**:
```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <downstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

#### Description Digest Comment (downstream propagation 2.2.x)

After creating the downstream propagation task, post the description digest comment:

1. **Re-fetch the description** from the newly created task:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write description to temp file and compute digest**:
   ```bash
   cat > /tmp/task-desc.md << 'DESCEOF'
   <fetched description content>
   DESCEOF

   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex> (or sha256-adf:<64-char-hex>)
   ```

3. **Post the digest comment** on the downstream task:
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

4. **Post digest comment before any links or other comments** -- this comment must be the first comment on the task.

---

## Jira Linkage (2.2.x Tasks)

After creating both tasks and posting their digest comments:

1. **Link upstream task to Vulnerability issue**:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

2. **Link downstream task to Vulnerability issue**:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

3. **Link downstream task as blocked by upstream task**:
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## Preemptive Remediation Tasks for Stream 2.1.x (Case A -- Cross-Stream Impact)

The 2.1.x stream is also affected (2.1.0 and 2.1.1 ship quinn-proto 0.11.9) but has no companion CVE Jira (would be verified via JQL search in Step 4). Preemptive tasks are created with the `security-preemptive` label and linked via "Related" (not "Depend").

### Cross-Stream Impact Comment on TC-8001

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s)
2.1.x based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

### Task 3: Upstream Backport (2.1.x -- Preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (quinn-proto is a direct dependency in Cargo.toml)

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating CVE -- cross-stream)
```

**Jira API call**:
```
preemptive_upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
  description: <preemptive-upstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

#### Description Digest Comment (preemptive upstream backport 2.1.x)

After creating the preemptive upstream task, post the description digest comment:

1. **Re-fetch the description** from the newly created task:
   ```
   preemptive_upstream_desc = jira.get_issue(<preemptive-upstream-task-key>, fields=["description"])
   ```

2. **Write description to temp file and compute digest**:
   ```bash
   cat > /tmp/task-desc.md << 'DESCEOF'
   <fetched description content>
   DESCEOF

   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex> (or sha256-adf:<64-char-hex>)
   ```

3. **Post the digest comment** on the preemptive upstream task:
   ```
   jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

4. **Post digest comment before any links or other comments** -- this comment must be the first comment on the task.

---

### Task 4: Downstream Propagation (2.1.x -- Preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (originating CVE -- cross-stream)
```

**Jira API call**:
```
preemptive_downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <preemptive-downstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

#### Description Digest Comment (preemptive downstream propagation 2.1.x)

After creating the preemptive downstream task, post the description digest comment:

1. **Re-fetch the description** from the newly created task:
   ```
   preemptive_downstream_desc = jira.get_issue(<preemptive-downstream-task-key>, fields=["description"])
   ```

2. **Write description to temp file and compute digest**:
   ```bash
   cat > /tmp/task-desc.md << 'DESCEOF'
   <fetched description content>
   DESCEOF

   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex> (or sha256-adf:<64-char-hex>)
   ```

3. **Post the digest comment** on the preemptive downstream task:
   ```
   jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

4. **Post digest comment before any links or other comments** -- this comment must be the first comment on the task.

---

## Jira Linkage (2.1.x Preemptive Tasks)

After creating both preemptive tasks and posting their digest comments:

1. **Link preemptive upstream task to originating CVE with "Related"** (not "Depend" -- different stream):
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <preemptive-upstream-task-key>,
     type: "Related"
   )
   ```

2. **Link preemptive downstream task to originating CVE with "Related"**:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <preemptive-downstream-task-key>,
     type: "Related"
   )
   ```

3. **Link preemptive downstream task as blocked by preemptive upstream task**:
   ```
   jira.create_link(
     inwardIssue: <preemptive-upstream-task-key>,
     outwardIssue: <preemptive-downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## Preemptive Task Comment on TC-8001

After creating the preemptive tasks, post a comment on TC-8001:

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <preemptive-upstream-task-key> (upstream backport, security-preemptive),
         <preemptive-downstream-task-key> (downstream propagation, security-preemptive,
         blocked by <preemptive-upstream-task-key>)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.7.
```

---

## Post-Triage Summary

After all triage actions are complete:

1. **Add the `ai-cve-triaged` label** to TC-8001.

2. **Post summary comment** on TC-8001:

```
## Triage Summary for CVE-2026-31812

### Version Impact

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

### Affects Versions Correction

Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

### Triage Outcome

Remediation tasks created (2.2.x -- scoped stream):
- <upstream-task-key> (upstream backport: bump quinn-proto to 0.11.14 on release/0.4.z)
- <downstream-task-key> (downstream propagation: update backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)

Preemptive remediation tasks created (2.1.x -- cross-stream):
- <preemptive-upstream-task-key> (upstream backport: bump quinn-proto to 0.11.14 on release/0.3.z, security-preemptive)
- <preemptive-downstream-task-key> (downstream propagation: update backend ref in rhtpa-release.0.3.z, security-preemptive, blocked by <preemptive-upstream-task-key>)

@<reporter-account-id> (PSIRT reporter mention via ADF mention node)

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.7.
```

---

## Task Summary

| # | Task | Stream | Type | Labels | Link to TC-8001 |
|---|------|--------|------|--------|-----------------|
| 1 | Upstream backport (2.2.x) | 2.2.x | Standard | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 2 | Downstream propagation (2.2.x) | 2.2.x | Standard | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 3 | Upstream backport (2.1.x) | 2.1.x | Preemptive | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| 4 | Downstream propagation (2.1.x) | 2.1.x | Preemptive | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
