# Step 8 -- Remediation: CVE-2026-31812

## Triage Outcome

The issue TC-8001 is scoped to stream **2.2.x**. Version impact analysis shows:

- **Stream 2.2.x**: versions 2.2.0, 2.2.1, 2.2.2 are affected (quinn-proto < 0.11.14). Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14).
- **Stream 2.1.x**: versions 2.1.0, 2.1.1 are also affected (quinn-proto 0.11.9), but this stream is outside the issue's scope.

This triggers:
- **Case A**: Create standard remediation tasks for stream 2.2.x
- **Case B**: Post cross-stream impact comment and create preemptive remediation tasks for stream 2.1.x

Ecosystem is **Cargo** (source dependency), so each stream gets **two tasks**: an upstream backport task and a downstream propagation subtask.

---

## Case A -- Standard Remediation Tasks (Stream 2.2.x)

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

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Comment (Task 1)

After creating the upstream backport task, perform the following steps to post the description digest comment:

1. **Re-fetch the description** from Jira (required because Jira normalizes content during storage):
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the digest:
   ```bash
   # Write description to temp file
   # Then compute digest:
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex> or sha256-adf:<64-char-hex>
   ```

3. **Post the digest comment** as a standalone comment on the task (before any links or other comments):
   ```
   jira.add_comment(<upstream-task-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `sha256-digest.py` (e.g., `sha256-md:a1b2c3...64chars`).

---

### Task 2: Downstream Propagation (2.2.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

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
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Comment (Task 2)

After creating the downstream propagation task, perform the following steps to post the description digest comment:

1. **Re-fetch the description** from Jira:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the digest:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

3. **Post the digest comment** as a standalone comment (before any links or other comments):
   ```
   jira.add_comment(<downstream-task-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

### Jira Linkage (2.2.x tasks)

After creating both tasks and posting their digest comments:

1. **Link upstream task to CVE**:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

2. **Link downstream task to CVE**:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")
   ```

3. **Link downstream as blocked by upstream**:
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

---

## Case B -- Cross-Stream Impact (Stream 2.1.x)

### Cross-Stream Impact Comment

Post the following comment to TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Stream 2.1.x ships quinn-proto 0.11.9
in all supported versions (2.1.0, 2.1.1).

These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

Since no sibling CVE Jira exists for stream 2.1.x (Step 4 search would find none with suffix `[rhtpa-2.1]`), preemptive remediation tasks are created.

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

```
## Repository

rhtpa-backend

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

Affected versions: 2.1.0, 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Comment (Task 3)

After creating the preemptive upstream backport task:

1. **Re-fetch the description** from Jira:
   ```
   preemptive_upstream_desc = jira.get_issue(<preemptive-upstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the digest:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

3. **Post the digest comment** as a standalone comment (before any links or other comments):
   ```
   jira.add_comment(<preemptive-upstream-task-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

### Task 4: Preemptive Downstream Propagation (2.1.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

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

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
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
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Comment (Task 4)

After creating the preemptive downstream propagation task:

1. **Re-fetch the description** from Jira:
   ```
   preemptive_downstream_desc = jira.get_issue(<preemptive-downstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the digest:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

3. **Post the digest comment** as a standalone comment (before any links or other comments):
   ```
   jira.add_comment(<preemptive-downstream-task-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

### Jira Linkage (2.1.x preemptive tasks)

After creating both preemptive tasks and posting their digest comments:

1. **Link preemptive upstream task to originating CVE** (Related, not Depend):
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <preemptive-upstream-task-key>, type: "Related")
   ```

2. **Link preemptive downstream task to originating CVE** (Related):
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <preemptive-downstream-task-key>, type: "Related")
   ```

3. **Link preemptive downstream as blocked by preemptive upstream**:
   ```
   jira.create_link(inwardIssue: <preemptive-upstream-task-key>, outwardIssue: <preemptive-downstream-task-key>, type: "Blocks")
   ```

### Preemptive Task Summary Comment

Post the following comment to TC-8001:

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <preemptive-upstream-task-key> (upstream backport, security-preemptive),
         <preemptive-downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Post-Triage Summary

After all remediation actions are complete:

1. **Add the `ai-cve-triaged` label** to TC-8001.

2. **Post summary comment** to TC-8001 documenting:
   - Version impact table (all streams)
   - Affects Versions correction: `[RHTPA 2.0.0]` -> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
   - Triage outcome: remediation tasks created
   - Standard remediation (2.2.x): <upstream-task-key> (upstream backport), <downstream-task-key> (downstream propagation, blocked by upstream)
   - Preemptive remediation (2.1.x): <preemptive-upstream-task-key>, <preemptive-downstream-task-key> (security-preemptive)
   - @mention of the vulnerability issue's reporter (PSIRT analyst)
   - Comment Footnote: "This comment was AI-generated by sdlc-workflow/triage-security v0.13.4."

All Jira comments include the Comment Footnote per `shared/comment-footnote.md`, using skill name `triage-security` and version `0.13.4`.
