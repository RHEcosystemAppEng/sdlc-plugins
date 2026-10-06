# Step 8 -- Remediation for CVE-2026-31812 (TC-8001)

## Triage Outcome

The issue is scoped to stream **2.2.x**. Within the 2.2.x stream, versions 2.2.0, 2.2.1, and 2.2.2 are affected (quinn-proto < 0.11.14). Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14) and are not affected.

Cross-stream impact: Stream **2.1.x** (versions 2.1.0, 2.1.1) is also affected. Since the issue is scoped to 2.2.x, this triggers **Case A** (cross-stream impact with proactive remediation) for 2.1.x.

Ecosystem: **Cargo** (source dependency) -- requires **2 tasks per stream** (upstream backport + downstream propagation).

## Case A: Cross-Stream Impact Comment

The following comment would be posted to TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Versions 2.1.0 and 2.1.1 both ship
quinn-proto 0.11.9. This stream is tracked by companion issues
(see Related links) or may require separate PSIRT triage.
```

---

## Case B: Remediation Tasks for Stream 2.2.x (In-Scope)

### Task 1: Upstream Backport (2.2.x)

**Jira creation call:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9),
RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12),
RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (or transitive -- to be verified via Cargo.lock dependency chain analysis)
- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
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

**Note:** The upstream fix is already present on release/0.4.z as of tag v0.4.11. The upstream backport task may already be complete if the branch HEAD has quinn-proto >= 0.11.14.

#### Description Digest Comment for Task 1

After creating the upstream backport task, the following steps would be performed to post the description digest comment:

1. **Re-fetch the description** from Jira after issue creation:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the description** to a temp file:
   ```
   Write description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest** using the script:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a format-tagged digest such as `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.

4. **Post the digest comment** to the newly created task (before any links or other comments):
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from step 3 (e.g., `sha256-md:a1b2c3d4...64 hex chars`).

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
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Comment for Task 2

After creating the downstream propagation task, the following steps would be performed:

1. **Re-fetch the description** from Jira after issue creation:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the description** to a temp file:
   ```
   Write description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest** using the script:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

4. **Post the digest comment** to the newly created task (before any links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

#### Linkage for 2.2.x Tasks

After both tasks are created and digest comments are posted:

1. **Link upstream task to CVE Jira:**
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

2. **Link downstream task to CVE Jira:**
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")
   ```

3. **Link downstream blocked by upstream:**
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

---

## Case A: Preemptive Remediation Tasks for Stream 2.1.x (Cross-Stream)

Since the issue is scoped to 2.2.x but stream 2.1.x is also affected, and assuming no existing CVE Jira exists for 2.1.x (no sibling found with suffix `[rhtpa-2.1]`), preemptive remediation tasks are created with the `security-preemptive` label and "Related" link type.

### Task 3: Preemptive Upstream Backport (2.1.x)

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
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9),
RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (or transitive -- to be verified via Cargo.lock dependency chain analysis)
- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14

**Fallback: pin the transitive dependency directly**
- Cargo: `cargo add quinn-proto@0.11.14`
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

- Depends on: TC-8001 (originating CVE, cross-stream)
```

#### Description Digest Comment for Task 3

After creating the preemptive upstream backport task:

1. **Re-fetch the description** from Jira:
   ```
   preemptive_upstream_desc = jira.get_issue(<preemptive-upstream-task-key>, fields=["description"])
   ```

2. **Write the description** to a temp file and compute the digest:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

3. **Post the digest comment** (before any links or other comments):
   ```
   jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

### Task 4: Preemptive Downstream Propagation (2.1.x)

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
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (originating CVE, cross-stream)
```

#### Description Digest Comment for Task 4

After creating the preemptive downstream propagation task:

1. **Re-fetch the description** from Jira:
   ```
   preemptive_downstream_desc = jira.get_issue(<preemptive-downstream-task-key>, fields=["description"])
   ```

2. **Write the description** to a temp file and compute the digest:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

3. **Post the digest comment** (before any links or other comments):
   ```
   jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

#### Linkage for 2.1.x Preemptive Tasks

After both preemptive tasks are created and digest comments are posted:

1. **Link preemptive upstream task to originating CVE Jira (Related, not Depend):**
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <preemptive-upstream-task-key>, type: "Related")
   ```

2. **Link preemptive downstream task to originating CVE Jira (Related, not Depend):**
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <preemptive-downstream-task-key>, type: "Related")
   ```

3. **Link preemptive downstream blocked by preemptive upstream:**
   ```
   jira.create_link(inwardIssue: <preemptive-upstream-task-key>, outwardIssue: <preemptive-downstream-task-key>, type: "Blocks")
   ```

---

## Preemptive Task Comment on TC-8001

After creating the preemptive tasks for 2.1.x, the following comment would be posted on TC-8001:

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <preemptive-upstream-task-key> (upstream backport, security-preemptive),
         <preemptive-downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.9.
```

---

## Post-Triage Summary Comment on TC-8001

After all triage actions are complete, the `ai-cve-triaged` label would be added to TC-8001 and the following summary comment posted:

```
## CVE-2026-31812 Triage Summary

### Version Impact Table

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
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

### Triage Outcome

Case B (Affected) + Case A (Cross-stream impact).

**Stream 2.2.x (in-scope) remediation tasks:**
- <upstream-task-key>: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2) -- upstream backport
- <downstream-task-key>: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2) -- downstream propagation, blocked by <upstream-task-key>

**Stream 2.1.x (cross-stream, preemptive) remediation tasks:**
- <preemptive-upstream-task-key>: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1) -- upstream backport (security-preemptive)
- <preemptive-downstream-task-key>: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1) -- downstream propagation (security-preemptive), blocked by <preemptive-upstream-task-key>

@reporter-mention

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.9.
```

---

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) -> 2 tasks per stream (upstream backport + downstream propagation). 2.2.x: 2 tasks. 2.1.x: 2 preemptive tasks. Total: 4 tasks.
- [x] **Cross-stream coverage**: Issue is scoped to 2.2.x. Stream 2.1.x is affected and has no sibling CVE Jira -- preemptive tasks created.
- [x] **Link types**: "Depend" for 2.2.x tasks linked to TC-8001. "Related" for 2.1.x preemptive tasks linked to TC-8001. "Blocks" for upstream -> downstream within each stream.
- [x] **Preemptive labels**: 2.1.x tasks carry the `security-preemptive` label.
- [x] **Coordination guidance**: Each task includes upstream deployment context guidance (repository default).
