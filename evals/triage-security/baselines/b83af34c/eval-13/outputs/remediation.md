# Step 8 - Remediation: CVE-2026-31812

## Triage Outcome

- Issue is **scoped** to stream 2.2.x (suffix `[rhtpa-2.2]`)
- Stream 2.2.x has affected versions (2.2.0, 2.2.1, 2.2.2) -- **Case B**: create remediation tasks
- Stream 2.1.x is also affected but out of scope -- **Case A**: cross-stream impact
- Ecosystem: Cargo (source dependency) -- **2 tasks per stream** (upstream backport + downstream propagation)

---

## Case B: Remediation Tasks for Stream 2.2.x (In Scope)

### Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Description**:

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8, v0.4.9

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock

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

**Labels**: `["ai-generated-jira", "Security", "CVE-2026-31812"]`

#### Jira API Calls for Upstream Backport Task

```
# 1. Create the upstream backport task
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <upstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

#### Description Digest Protocol for Upstream Backport Task

After creating the upstream backport task, the description digest comment MUST be posted BEFORE creating any issue links (Depend, Blocks) or other comments. The procedure is:

1. **Re-fetch the task description from Jira** -- do NOT hash the description string passed to `create_issue`, because Jira normalizes content during storage. Always re-fetch via the API after creation:

   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temporary file**:

   ```
   # Write the re-fetched description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest using scripts/sha256-digest.py**:

   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex> or sha256-adf:<64-char-hex>
   ```

4. **Post the digest comment** with the exact marker string:

   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3...64chars`).

5. **THEN (only after the digest comment is posted)** create issue links and other comments:

   ```
   # Link upstream task to CVE Vulnerability issue with "Depend"
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

---

### Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

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

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Labels**: `["ai-generated-jira", "Security", "CVE-2026-31812"]`

#### Jira API Calls for Downstream Propagation Subtask

```
# 2. Create the downstream propagation subtask
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <downstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

#### Description Digest Protocol for Downstream Propagation Subtask

After creating the downstream propagation subtask, the description digest comment MUST be posted BEFORE creating any issue links (Depend, Blocks) or other comments. The procedure is:

1. **Re-fetch the task description from Jira** -- do NOT hash the description string passed to `create_issue`, because Jira normalizes content during storage. Always re-fetch via the API after creation:

   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temporary file**:

   ```
   # Write the re-fetched description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest using scripts/sha256-digest.py**:

   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex> or sha256-adf:<64-char-hex>
   ```

4. **Post the digest comment** with the exact marker string:

   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3...64chars`).

5. **THEN (only after the digest comment is posted)** create issue links and other comments:

   ```
   # Link downstream subtask to CVE Vulnerability issue with "Depend"
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )

   # Link downstream subtask as blocked by upstream task with "Blocks"
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## Case A: Cross-Stream Impact (Stream 2.1.x)

Stream 2.1.x is also affected (versions 2.1.0, 2.1.1 ship quinn-proto 0.11.9 < 0.11.14) but is outside this issue's scope.

### Cross-stream impact comment on TC-8001

```
Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream(s)
2.1.x based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

### Preemptive remediation (if no sibling CVE Jira exists for 2.1.x)

If no sibling Vulnerability issue exists for stream 2.1.x, create preemptive remediation tasks using the same templates above but with:
- Labels include `security-preemptive` alongside standard labels
- Link type is "Related" (not "Depend") to TC-8001
- Description includes preemptive remediation prefix

Each preemptive task also follows the description digest protocol as described above for the standard tasks.

---

## Complete Task Creation Sequence (Summary)

The full sequence for each remediation task is:

### For the upstream backport task:

1. `jira.create_issue(...)` -- create the task
2. `jira.get_issue(<upstream-task-key>, fields=["description"])` -- re-fetch the description from Jira (do NOT use the description string passed to create_issue)
3. Write re-fetched description to `/tmp/task-desc.md`
4. `python3 scripts/sha256-digest.py /tmp/task-desc.md` -- compute SHA-256 digest
5. `jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")` -- post digest comment
6. `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")` -- link to CVE

### For the downstream propagation subtask:

1. `jira.create_issue(...)` -- create the task
2. `jira.get_issue(<downstream-task-key>, fields=["description"])` -- re-fetch the description from Jira (do NOT use the description string passed to create_issue)
3. Write re-fetched description to `/tmp/task-desc.md`
4. `python3 scripts/sha256-digest.py /tmp/task-desc.md` -- compute SHA-256 digest
5. `jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")` -- post digest comment
6. `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")` -- link to CVE
7. `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")` -- block on upstream

Note: The digest is always computed from the **re-fetched** description (retrieved via `jira.get_issue` after `create_issue`), never from the description string originally passed to `create_issue`. This is because Jira normalizes content during storage, so the stored representation may differ from what was submitted.
