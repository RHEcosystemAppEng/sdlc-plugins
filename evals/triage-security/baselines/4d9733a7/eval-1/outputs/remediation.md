# Step 8 -- Remediation

## Triage Outcome: Case A -- Affected, create remediation tasks

The 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2). Since the ecosystem is **Cargo** (a source dependency ecosystem), two tasks are created: an upstream backport task and a downstream propagation subtask (Important Rule 8).

Additionally, the 2.1.x stream is also affected (Case B cross-stream impact). Since this issue is scoped to [rhtpa-2.2], a cross-stream impact comment would be posted (Case B).

---

## Task 1: Upstream Backport Task (Source Repository Fix)

**PROPOSED** Jira issue creation:

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

```markdown
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z (from Ecosystem Mappings Upstream Branch)
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

### Post-creation digest protocol

1. Re-fetch the created task's description from Jira API:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
3. Post digest comment (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

### Post-digest linkage

4. Link to the Vulnerability issue:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

---

## Task 2: Downstream Propagation Subtask (Konflux Release Repo Update)

**PROPOSED** Jira issue creation:

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

```markdown
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
- Depends on: TC-8001 (parent tracking issue)
```

### Post-creation digest protocol

1. Re-fetch the created task's description from Jira API:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
3. Post digest comment (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

### Post-digest linkage

4. Link to the Vulnerability issue:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")
   ```
5. Link downstream as blocked by upstream:
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

---

## Post-Triage Summary

**PROPOSED** actions after remediation task creation:

1. Add `ai-cve-triaged` label to TC-8001
2. Post summary comment on TC-8001 documenting version impact, Affects Versions correction, and remediation tasks created
3. Transition TC-8001 to In Progress

All actions above are **proposals** requiring engineer confirmation before execution.
