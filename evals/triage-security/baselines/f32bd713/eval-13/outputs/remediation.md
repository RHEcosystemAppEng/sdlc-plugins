# Step 8 -- Remediation for TC-8001

## Triage Decision

- **In-scope stream (2.2.x)**: Versions 2.2.0, 2.2.1, 2.2.2 are affected --> **Case B** (create remediation tasks)
- **Cross-stream (2.1.x)**: Versions 2.1.0, 2.1.1 are affected, no stream-specific CVE Jira exists --> **Case A** (cross-stream impact, preemptive remediation tasks)
- Ecosystem: Cargo (source dependency) --> 2 tasks per stream
- Upstream fix on release/0.4.z (2.2.x): YES --> dependency bump + downstream propagation
- Upstream fix on release/0.3.z (2.1.x): NO --> upstream backport + downstream propagation (preemptive)

---

## Task 1: Dependency Bump -- Stream 2.2.x (in-scope, standard)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8)

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

### Description Digest Comment (Task 1)

After creating the task, perform the following steps to post the description digest:

1. **Fetch the created task's description from Jira:**
   ```
   upstream_desc = jira.get_issue(<bump-task-key>, fields=["description"])
   ```
2. **Write the description content to a temporary file:**
   Write the returned description to `/tmp/task-desc.md`
3. **Compute the SHA-256 digest:**
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs either `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>` depending on the format returned by Jira.
4. **Post the digest as a comment on the created task (before any links or other comments):**
   ```
   jira.add_comment(<bump-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   The comment is posted in ADF format:
   ```json
   {
     "type": "doc",
     "version": 1,
     "content": [
       {
         "type": "paragraph",
         "content": [
           {
             "type": "text",
             "text": "[sdlc-workflow] Description digest: <tagged-digest>"
           }
         ]
       }
     ]
   }
   ```

### Jira Links (Task 1)

After posting the digest comment:
```
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <bump-task-key>, type: "Depend")
```

---

## Task 2: Downstream Propagation -- Stream 2.2.x (in-scope, standard)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
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

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <bump-task-key>.

The dependency bump (<bump-task-key>) updates quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <bump-task-key> (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Comment (Task 2)

After creating the task, perform the following steps to post the description digest:

1. **Fetch the created task's description from Jira:**
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. **Write the description content to a temporary file:**
   Write the returned description to `/tmp/task-desc.md`
3. **Compute the SHA-256 digest:**
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
4. **Post the digest as a comment on the created task (before any links or other comments):**
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Same ADF format as Task 1.

### Jira Links (Task 2)

After posting the digest comment:
```
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")
jira.create_link(inwardIssue: <bump-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
```

---

## Task 3: Upstream Backport -- Stream 2.1.x (cross-stream, preemptive)

This task is created under Case A (cross-stream impact). Stream 2.1.x is affected but has no
stream-specific CVE Jira. The upstream branch release/0.3.z does NOT have the fix, so an upstream
backport is required.

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

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

Remediate CVE-2026-31812: quinn-proto denial of service via excessive stream counts.
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

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
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

### Description Digest Comment (Task 3)

After creating the task, perform the following steps to post the description digest:

1. **Fetch the created task's description from Jira:**
   ```
   upstream_desc = jira.get_issue(<upstream-backport-task-key>, fields=["description"])
   ```
2. **Write the description content to a temporary file:**
   Write the returned description to `/tmp/task-desc.md`
3. **Compute the SHA-256 digest:**
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
4. **Post the digest as a comment on the created task (before any links or other comments):**
   ```
   jira.add_comment(<upstream-backport-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Same ADF format as Task 1.

### Jira Links (Task 3)

After posting the digest comment. Preemptive tasks use "Related" (not "Depend") because the
originating CVE TC-8001 belongs to a different stream (2.2.x):
```
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-backport-task-key>, type: "Related")
```

---

## Task 4: Downstream Propagation -- Stream 2.1.x (cross-stream, preemptive)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
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

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <upstream-backport-task-key>.

The upstream backport (<upstream-backport-task-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-backport-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Comment (Task 4)

After creating the task, perform the following steps to post the description digest:

1. **Fetch the created task's description from Jira:**
   ```
   downstream_desc = jira.get_issue(<downstream-preemptive-task-key>, fields=["description"])
   ```
2. **Write the description content to a temporary file:**
   Write the returned description to `/tmp/task-desc.md`
3. **Compute the SHA-256 digest:**
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
4. **Post the digest as a comment on the created task (before any links or other comments):**
   ```
   jira.add_comment(<downstream-preemptive-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Same ADF format as Task 1.

### Jira Links (Task 4)

After posting the digest comment. Preemptive tasks use "Related" for CVE link; upstream-to-downstream
uses "Blocks":
```
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-preemptive-task-key>, type: "Related")
jira.create_link(inwardIssue: <upstream-backport-task-key>, outwardIssue: <downstream-preemptive-task-key>, type: "Blocks")
```

---

## Cross-Stream Impact Comment (Case A)

After creating all preemptive tasks, post a comment on TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s)
2.1.x based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-backport-task-key> (upstream backport, security-preemptive),
         <downstream-preemptive-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

This comment MUST include the Comment Footnote per `shared/comment-footnote.md`.

---

## Post-Triage Summary Comment

After all triage actions are complete, post a summary comment on TC-8001 and add the
`ai-cve-triaged` label:

```
jira.edit_issue("TC-8001", labels=["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"])
```

Summary comment on TC-8001:

```
## CVE-2026-31812 Triage Summary

### Version Impact

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | preemptive |
| 2.1.1 | 2.1.x | 0.11.9 | YES | preemptive |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

### Affects Versions Correction

- Removed: RHTPA 2.0.0 (no such version in supportability matrix)
- Added: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

### Triage Outcome

Remediation tasks created (Case B + Case A cross-stream):

**Stream 2.2.x (in-scope, standard):**
- <bump-task-key>: dependency bump -- update quinn-proto to 0.11.14
- <downstream-task-key>: downstream propagation -- update backend ref in rhtpa-release.0.4.z (blocked by <bump-task-key>)

**Stream 2.1.x (cross-stream, preemptive):**
- <upstream-backport-task-key>: upstream backport -- bump quinn-proto to 0.11.14 on release/0.3.z (security-preemptive)
- <downstream-preemptive-task-key>: downstream propagation -- update backend ref in rhtpa-release.0.3.z (blocked by <upstream-backport-task-key>, security-preemptive)
```

This summary comment MUST include:
- An @mention of the vulnerability issue's reporter (using ADF mention node with their account ID)
- The Comment Footnote per `shared/comment-footnote.md`

---

## Task Creation Order and Digest-Before-Link Rule

The strict ordering for all task creation is:

1. Create remediation task (Jira `create_issue`)
2. Fetch description back from Jira (`get_issue` with `fields=["description"]`)
3. Write description to temp file
4. Compute digest (`python3 scripts/sha256-digest.py /tmp/task-desc.md`)
5. Post digest comment (`add_comment` with marker `[sdlc-workflow] Description digest: <tagged-digest>`)
6. **Only then** create issue links (`create_link`)
7. **Only then** post any other comments on the task

This order is repeated for each of the 4 tasks. The digest comment MUST be posted before
any links or other comments are created on the task, per the description-digest-protocol.

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo (source dependency) --> 2 tasks per stream (correct)
  - 2.2.x: 1 dependency bump + 1 downstream propagation = 2 tasks
  - 2.1.x: 1 upstream backport + 1 downstream propagation = 2 tasks (preemptive)
- [x] **Cross-stream coverage**: 2.1.x has preemptive tasks (no sibling CVE Jira exists)
- [x] **Link types**: "Depend" for tasks linked to their own CVE (2.2.x tasks), "Related" for preemptive tasks linked to TC-8001 (2.1.x tasks), "Blocks" for upstream --> downstream within each stream
- [x] **Preemptive labels**: 2.1.x tasks carry `security-preemptive` label
- [x] **Coordination guidance**: omitted (Source Repositories table lacks Deployment Context column)
- [x] **Dedup consistency**: no dedup applicable (no prior remediation tasks exist)
