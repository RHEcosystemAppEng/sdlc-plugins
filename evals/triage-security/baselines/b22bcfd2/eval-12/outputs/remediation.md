# Step 8 -- Remediation

## Triage Outcome

**Case A: Affected -- create remediation tasks** for the 2.2.x stream.

Version 2.2.0 ships h2 0.4.5, which is below the enriched fix threshold of 0.4.8 (from Step 1.5 external CVE data enrichment). Remediation tasks are required.

The fix threshold used here (0.4.8) comes from the cross-validated external CVE data (MITRE + OSV.dev agreement), not from the imprecise Jira description which stated only "versions prior to the fix."

## Ecosystem: Cargo (Source Dependency)

Since h2 is a Cargo (Rust) dependency, two tasks are created per the source dependency ecosystem flow: an upstream backport task and a downstream propagation subtask.

---

## Task 1: Upstream Backport Task

**Proposed Jira issue creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-48901"]
)
```

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.2.0
Source commit(s): v0.4.5 (from supportability matrix)

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.4.z (from Ecosystem Mappings)
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (parent tracking issue)

---

### Post-creation procedure (description digest protocol)

After creating the upstream backport task:

1. **Re-fetch the task description from Jira** (the rendered description, not the input string):
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. **Write the re-fetched description** to a temporary file:
   ```
   Write description to /tmp/task-desc.md
   ```
3. **Compute SHA-256 digest** from the re-fetched description using `scripts/sha256-digest.py`:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This produces a tagged digest (e.g., `sha256-md:<hex>` or `sha256-adf:<hex>`).
4. **Post the digest comment** (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
5. **Then create issue links**:
   ```
   jira.create_link(
     inwardIssue: TC-8030,
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

---

## Task 2: Downstream Propagation Subtask

**Proposed Jira issue creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-48901"]
)
```

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-48901 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.8
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8030 (parent tracking issue)

---

### Post-creation procedure (description digest protocol)

After creating the downstream propagation subtask:

1. **Re-fetch the task description from Jira** (the rendered description, not the input string):
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. **Write the re-fetched description** to a temporary file:
   ```
   Write description to /tmp/task-desc.md
   ```
3. **Compute SHA-256 digest** from the re-fetched description using `scripts/sha256-digest.py`:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This produces a tagged digest (e.g., `sha256-md:<hex>` or `sha256-adf:<hex>`).
4. **Post the digest comment** (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
5. **Then create issue links**:
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   jira.create_link(
     inwardIssue: TC-8030,
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

---

## Linkage Summary

| Link | From | To | Type |
|------|------|----|------|
| Vulnerability to upstream task | TC-8030 | <upstream-task-key> | Depend |
| Vulnerability to downstream task | TC-8030 | <downstream-task-key> | Depend |
| Upstream blocks downstream | <upstream-task-key> | <downstream-task-key> | Blocks |

## Post-Triage Actions (proposed)

The following actions are proposed for engineer confirmation:

1. **Add label** `ai-cve-triaged` to TC-8030
2. **Transition** TC-8030 to In Progress
3. **Assign** TC-8030 to current user
4. **Post summary comment** to TC-8030 documenting the version impact table, Affects Versions correction, triage outcome, and links to all created remediation tasks

## Affects Versions Correction (from Step 3)

The current Affects Versions on TC-8030 is `[RHTPA 2.2.0]`. Based on the version impact analysis, only version 2.2.0 is affected. The PSIRT-assigned value is correct and complete for the 2.2.x stream scope -- no correction is needed.

**Proposed**: Current: [RHTPA 2.2.0] -- no change required.
