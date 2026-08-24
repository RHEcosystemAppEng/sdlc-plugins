# Step 8 -- Remediation: CVE-2026-31812

## Triage Outcome

**Case A + Case B**: The issue is scoped to stream 2.2.x and affected versions exist within that stream (2.2.0, 2.2.1, 2.2.2). Additionally, the 2.1.x stream is also affected (cross-stream impact), requiring proactive remediation tasks.

Since quinn-proto is a **Cargo** (source dependency) ecosystem package, each stream requires **2 tasks**: an upstream backport task and a downstream propagation task.

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks per stream (Cargo = source dependency ecosystem)
- [x] **Cross-stream coverage**: 2.1.x stream has no sibling CVE Jira -- preemptive tasks will be created
- [x] **Link types**: "Depend" for 2.2.x tasks linked to TC-8001; "Related" for 2.1.x preemptive tasks linked to TC-8001; "Blocks" for upstream -> downstream within each stream
- [x] **Preemptive labels**: 2.1.x tasks carry `security-preemptive` label
- [x] **Coordination guidance**: upstream deployment context -- public upstream coordination guidance included

---

## Case A: Cross-Stream Impact Comment

The following comment would be posted on TC-8001:

> Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream(s) 2.1.x based on lock file analysis.
> These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

---

## Case B: Remediation Tasks for 2.2.x Stream (Scoped)

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

**Task Description:**

```markdown
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- The upstream fix is already present in later tags on this branch (v0.4.11+ ship quinn-proto 0.11.14). A cherry-pick or backport from upstream may be available.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Linkage:**
```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

#### Description Digest Comment for Task 1

After creating the upstream backport task, the following steps would be performed to post the description digest comment:

1. **Re-fetch the description** from Jira to get the stored representation:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the digest:
   ```bash
   # Write the fetched description to a temp file
   # (content written is the Jira-stored description, not the input)
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex-digest> or sha256-adf:<64-char-hex-digest>
   ```

3. **Post the digest comment** on the newly created task (before any links or other comments):
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `sha256-digest.py` (e.g., `sha256-md:a1b2c3...64chars`).

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

**Task Description:**

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

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Linkage:**
```
# Link downstream to the Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

# Link downstream as blocked by upstream
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

#### Description Digest Comment for Task 2

After creating the downstream propagation task, the following steps would be performed:

1. **Re-fetch the description** from Jira:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the digest:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex-digest> or sha256-adf:<64-char-hex-digest>
   ```

3. **Post the digest comment** on the task (before links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

## Case A: Preemptive Remediation Tasks for 2.1.x Stream

The 2.1.x stream is also affected but has no stream-specific CVE Jira. Preemptive remediation tasks are created with `security-preemptive` label and "Related" link type.

### Task 3: Upstream Backport (2.1.x -- Preemptive)

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

**Task Description:**

```markdown
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
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9), RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- The upstream fix has NOT been backported to release/0.3.z yet. The fix must be backported from upstream (quinn-rs/quinn#2048) or the dependency bumped directly.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue -- cross-stream, Related link)
```

**Linkage (preemptive -- "Related" not "Depend"):**
```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)
```

#### Description Digest Comment for Task 3

1. **Re-fetch the description** from Jira:
   ```
   preemptive_upstream_desc = jira.get_issue(<preemptive-upstream-task-key>, fields=["description"])
   ```

2. **Compute the digest**:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

3. **Post the digest comment** (before links or other comments):
   ```
   jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

### Task 4: Downstream Propagation (2.1.x -- Preemptive)

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

**Task Description:**

```markdown
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

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue -- cross-stream, Related link)
```

**Linkage (preemptive -- "Related" not "Depend"):**
```
# Link downstream preemptive task to the originating CVE with "Related"
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Related"
)

# Link downstream as blocked by upstream (within the 2.1.x stream)
jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)
```

#### Description Digest Comment for Task 4

1. **Re-fetch the description** from Jira:
   ```
   preemptive_downstream_desc = jira.get_issue(<preemptive-downstream-task-key>, fields=["description"])
   ```

2. **Compute the digest**:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

3. **Post the digest comment** (before links or other comments):
   ```
   jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

## Preemptive Tasks Comment on TC-8001

After creating the preemptive tasks, the following comment would be posted on TC-8001:

> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: <preemptive-upstream-task-key> (upstream backport, security-preemptive), <preemptive-downstream-task-key> (downstream propagation, security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive
> label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
> reconciliation will link them and remove the label.

---

## Post-Triage Summary

After all triage actions are complete:

1. **Add `ai-cve-triaged` label** to TC-8001
2. **Post summary comment** on TC-8001:

> **Triage Summary for CVE-2026-31812 (quinn-proto)**
>
> **Version Impact:**
>
> | Version | quinn-proto | Affected? | Notes |
> |---------|-------------|-----------|-------|
> | 2.1.0 | 0.11.9 | YES | |
> | 2.1.1 | 0.11.9 | YES | |
> | 2.2.0 | 0.11.9 | YES | |
> | 2.2.1 | 0.11.12 | YES | |
> | 2.2.2 | 0.11.12 | YES | retag of 2.2.1 |
> | 2.2.3 | 0.11.14 | NO | fixed version |
> | 2.2.4 | 0.11.14 | NO | fixed version |
>
> **Affects Versions Correction:** RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
> (scoped to 2.2.x stream per issue suffix [rhtpa-2.2])
>
> **Triage Outcome:** Remediation tasks created
>
> **Remediation Tasks (2.2.x -- scoped):**
> - <upstream-task-key> (upstream backport: bump quinn-proto to 0.11.14 on release/0.4.z)
> - <downstream-task-key> (downstream propagation: update backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)
>
> **Preemptive Remediation Tasks (2.1.x -- cross-stream):**
> - <preemptive-upstream-task-key> (upstream backport: bump quinn-proto to 0.11.14 on release/0.3.z, security-preemptive)
> - <preemptive-downstream-task-key> (downstream propagation: update backend ref in rhtpa-release.0.3.z, blocked by <preemptive-upstream-task-key>, security-preemptive)
>
> @reporter-mention (ADF mention node with reporter account ID from TC-8001)
>
> ---
> This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.8.

All Jira comments posted during this triage include the Comment Footnote.
