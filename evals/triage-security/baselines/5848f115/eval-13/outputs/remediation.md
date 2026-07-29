# Step 8 -- Remediation: CVE-2026-31812

## Triage Outcome

**Case B (Affected)** -- supported versions in the scoped stream (2.2.x) are affected. Remediation tasks are required.

**Case A (Cross-stream impact)** -- stream 2.1.x is also affected but is outside this issue's scope. Preemptive remediation tasks are created for 2.1.x (assuming no existing CVE Jira covers that stream).

quinn-proto is a **Cargo** (source dependency) ecosystem, so each stream requires **2 tasks**: upstream backport + downstream propagation.

---

## Stream 2.2.x Remediation Tasks (Standard -- linked to TC-8001)

### Task 1: Upstream Backport (2.2.x)

**Jira Creation Call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <upstream-task-description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- The fix is already present at v0.4.11+ on this branch (quinn-proto 0.11.14).
  The upstream backport may already be merged -- verify branch HEAD before starting.

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
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

**Linkage:**
```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

#### Description Digest Comment for Task 1

After creating the upstream backport task, post the description digest comment:

1. Re-fetch the created task's description from Jira:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.
3. Post the digest as a standalone comment on the task (before creating issue links or other comments):
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `sha256-digest.py` (e.g., `sha256-md:a1b2c3...64 hex chars...`).

---

### Task 2: Downstream Propagation (2.2.x)

**Jira Creation Call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <downstream-task-description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

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
# Link downstream task to CVE Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

# Link downstream task as blocked by upstream task
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

#### Description Digest Comment for Task 2

After creating the downstream propagation task, post the description digest comment:

1. Re-fetch the created task's description from Jira:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
3. Post the digest as a standalone comment on the task (before creating issue links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

## Stream 2.1.x Preemptive Remediation Tasks (Case A -- linked as "Related" to TC-8001)

These tasks are created proactively because stream 2.1.x is affected but has no stream-specific CVE Jira. They carry the `security-preemptive` label and use "Related" link type (not "Depend").

### Task 3: Upstream Backport (2.1.x, preemptive)

**Jira Creation Call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <upstream-task-description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task Description:**

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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- The upstream branch release/0.3.z currently ships quinn-proto 0.11.9 at the
  latest tag (v0.3.12). An upstream backport is required to bump quinn-proto
  to >= 0.11.14 on this branch.

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue -- Related link, not Depend)
```

**Linkage (preemptive -- uses "Related" link type):**
```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)
```

#### Description Digest Comment for Task 3

After creating the preemptive upstream backport task, post the description digest comment:

1. Re-fetch the created task's description from Jira:
   ```
   preemptive_upstream_desc = jira.get_issue(<preemptive-upstream-task-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
3. Post the digest as a standalone comment on the task (before creating issue links or other comments):
   ```
   jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

### Task 4: Downstream Propagation (2.1.x, preemptive)

**Jira Creation Call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <downstream-task-description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task Description:**

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

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue -- Related link, not Depend)
```

**Linkage (preemptive -- uses "Related" link type):**
```
# Link downstream task to originating CVE with "Related"
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Related"
)

# Link downstream task as blocked by upstream task
jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)
```

#### Description Digest Comment for Task 4

After creating the preemptive downstream propagation task, post the description digest comment:

1. Re-fetch the created task's description from Jira:
   ```
   preemptive_downstream_desc = jira.get_issue(<preemptive-downstream-task-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
3. Post the digest as a standalone comment on the task (before creating issue links or other comments):
   ```
   jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

## Preemptive Task Summary Comment on TC-8001

After creating the preemptive tasks for stream 2.1.x, a comment would be posted to TC-8001:

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

After all triage actions are complete, the following actions would be performed on TC-8001:

1. **Add `ai-cve-triaged` label** to TC-8001.

2. **Post summary comment** to TC-8001 documenting:
   - Version impact table (all versions across all streams)
   - Affects Versions correction: `[RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
   - Triage outcome: remediation tasks created for 2.2.x (standard) and 2.1.x (preemptive)
   - Links to all remediation tasks:
     - 2.2.x: <upstream-task-key> (upstream backport), <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>)
     - 2.1.x (preemptive): <preemptive-upstream-task-key>, <preemptive-downstream-task-key>
   - @mention of the vulnerability issue reporter (using ADF mention node with the reporter's account ID from the Jira issue)
   - Comment Footnote (see below)

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) -> 2 tasks per stream (upstream backport + downstream propagation). 2 streams affected = 4 tasks total.
- [x] **Cross-stream coverage**: Issue is scoped to 2.2.x. Stream 2.1.x is affected and has preemptive tasks created (assuming no existing sibling CVE Jira).
- [x] **Link types**: "Depend" for 2.2.x tasks linked to TC-8001. "Related" for 2.1.x preemptive tasks linked to TC-8001. "Blocks" for upstream -> downstream within each stream.
- [x] **Preemptive labels**: 2.1.x tasks carry the `security-preemptive` label.
- [x] **Coordination guidance**: Source Repositories table has no Deployment Context column -- coordination guidance subsection is omitted from all task descriptions.

## Description Digest Protocol Summary

For every remediation task created (Tasks 1-4), the description digest protocol requires:

1. **Re-fetch** the task description from Jira after creation (do not hash the input string -- Jira normalizes content during storage).
2. **Compute** the digest using `python3 scripts/sha256-digest.py` with the re-fetched description written to a temp file. The script auto-detects whether the input is ADF JSON or markdown and outputs a format-tagged digest (`sha256-adf:<64-hex>` or `sha256-md:<64-hex>`).
3. **Post** the digest as a standalone comment: `[sdlc-workflow] Description digest: <tagged-digest>`.
4. **Post the digest comment before** creating issue links or other comments on the task.
5. The digest comment must be exactly one line -- no extra text, no abbreviated hashes, no placeholder values.
