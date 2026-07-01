# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix

Loaded from security-matrix-mock.md. All versions from both streams are included per Important Rule 4.

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Using pinned commit tags from the supportability matrix (Important Rule 13), not branch HEAD.

For each version, the quinn-proto version is extracted from `Cargo.lock` at the pinned tag:

| Version | Tag | quinn-proto version | Affected? (< 0.11.14) | Notes |
|---------|-----|---------------------|-----------------------|-------|
| 2.1.0 | `v0.3.8` | 0.11.9 | **YES** | |
| 2.1.1 | `v0.3.12` | 0.11.9 | **YES** | |
| 2.2.0 | `v0.4.5` | 0.11.9 | **YES** | |
| 2.2.1 | `v0.4.8` | 0.11.12 | **YES** | |
| 2.2.2 | `v0.4.8` | 0.11.12 | **YES** | retag of 2.2.1 -- same as 2.2.1 (Important Rule 5) |
| 2.2.3 | `v0.4.11` | 0.11.14 | **NO** | ships fixed version |
| 2.2.4 | `v0.4.12` | 0.11.14 | **NO** | ships fixed version |

## 2.4 -- Version Impact Table

```
Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0   | 0.11.9      | YES       |       |
| 2.1.1   | 0.11.9      | YES       |       |
| 2.2.0   | 0.11.9      | YES       |       |
| 2.2.1   | 0.11.12     | YES       |       |
| 2.2.2   | 0.11.12     | YES       | retag of 2.2.1 |
| 2.2.3   | 0.11.14     | NO        |       |
| 2.2.4   | 0.11.14     | NO        |       |
```

### Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto (Cargo):
  Ecosystem: Cargo (source dependency)
  Lock file: Cargo.lock
  Profile: production (runtime dependency)
  
  Affected versions: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2
  Not affected: 2.2.3, 2.2.4 (ship quinn-proto 0.11.14, the fixed version)
```

---

# Step 3 -- Affects Versions Correction

The issue is scoped to stream **2.2.x**. Only versions from this stream are included in the Affects Versions correction (Important Rule 6 -- use version names from the supportability matrix, discovered dynamically).

**Current Affects Versions**: RHTPA 2.0.0
**Proposed Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

Diff: `Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

RHTPA 2.0.0 does not exist in the supportability matrix -- PSIRT assigned an incorrect version. The lock-file-verified affected versions in the 2.2.x stream are 2.2.0, 2.2.1, and 2.2.2.

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14, which is outside the affected range.

**Proposed action**: Replace Affects Versions with the lock-file-verified values. This is a proposal requiring engineer confirmation before execution.

No ProdSec Jira account ID is configured -- @mention is omitted silently.

---

# Step 4 -- Duplicate, Sibling, and Overlap Check

_(No sibling search results provided in eval scenario. Proceeding to Step 5.)_

### Step 4.3 -- Cross-CVE Overlap Detection

Upstream Affected Component custom field is not configured in Security Configuration. Skipping Step 4.3 entirely.

### Step 4.4 -- Preemptive Task Reconciliation

_(No preemptive task search results provided. Proceeding to Step 5.)_

---

# Step 5 -- Version Lifecycle Check

_(Skipped -- eval prohibits external API calls via WebFetch.)_

---

# Step 6 -- Already Fixed Check

_(No resolved sibling issues found. Proceeding to Step 7.)_

---

# Step 7 -- Concurrent Triage Detection

Upstream Affected Component custom field is not configured in Security Configuration. Skipping Step 7 entirely.

---

# Step 8 -- Remediation

## Triage Outcome: Case A -- Affected, Create Remediation Tasks

The version impact table shows affected versions in the 2.2.x stream (2.2.0, 2.2.1, 2.2.2). The 2.1.x stream is also affected (2.1.0, 2.1.1) but is outside this issue's scope (scoped to 2.2.x via `[rhtpa-2.2]`).

### Cross-stream impact notice (Case B)

Stream 2.1.x is also affected (quinn-proto 0.11.9, within affected range < 0.11.14). This would be noted via a cross-stream impact comment on TC-8001:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

### Ecosystem: Cargo (Source Dependency)

Per the skill rules (Important Rule 8), Cargo ecosystem remediation creates **two** tasks:
1. **Upstream backport task** -- fix in the source repo (rhtpa-backend)
2. **Downstream propagation subtask** -- update the source reference in the Konflux release repo, blocked by the upstream task

---

## Remediation Task 1: Upstream Backport Task

**Proposed Jira creation:**

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

Remediate CVE-2026-31812: quinn-proto - Panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
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

**Note**: No Coordination Guidance subsection is included in Implementation Notes. The Source Repositories table does not have a Deployment Context column, so coordination guidance is omitted entirely for backward compatibility. The default deployment context of `upstream` does not trigger guidance generation when the column itself is absent.

### Description Digest Protocol (Post-Creation)

After creating the upstream backport task, the following digest steps would be performed:

1. **Re-fetch the description** from Jira after `create_issue`:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file** and compute a SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The digest is computed from the **re-fetched** description (via Jira API after create_issue), not from the description string originally passed to create_issue.

3. **Post the digest comment** with the marker `[sdlc-workflow] Description digest:` before creating issue links or other comments:
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

4. **Then** create the Depend link to TC-8001:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

---

## Remediation Task 2: Downstream Propagation Subtask

**Proposed Jira creation:**

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

**Note**: No Coordination Guidance subsection is included in Implementation Notes. The Source Repositories table does not have a Deployment Context column, so coordination guidance is omitted entirely for backward compatibility.

### Description Digest Protocol (Post-Creation)

After creating the downstream propagation subtask, the following digest steps would be performed:

1. **Re-fetch the description** from Jira after `create_issue`:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file** and compute a SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The digest is computed from the **re-fetched** description (via Jira API after create_issue), not from the description string originally passed to create_issue.

3. **Post the digest comment** with the marker `[sdlc-workflow] Description digest:` before creating issue links or other comments:
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

4. **Then** create the links:
   - Blocks link (downstream blocked by upstream):
     ```
     jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
     ```
   - Depend link to the vulnerability issue:
     ```
     jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")
     ```

---

## Post-Triage Summary

### Proposed actions (all require engineer confirmation):

1. **Add label**: `ai-cve-triaged` to TC-8001
2. **Correct Affects Versions**: `[RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
3. **Create upstream backport task**: Remediate CVE-2026-31812 -- bump quinn-proto to 0.11.14 (rhtpa-2.2)
4. **Create downstream propagation subtask**: Propagate CVE-2026-31812 fix -- update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
5. **Link tasks**: upstream task Depend -> TC-8001, downstream subtask Depend -> TC-8001, downstream Blocks <- upstream
6. **Post digest comments**: on both tasks before creating links
7. **Post cross-stream impact comment**: noting 2.1.x stream is also affected
8. **Post summary comment**: documenting version impact table, Affects Versions correction, triage outcome, and remediation task links
9. **Transition**: TC-8001 to In Progress

All actions above are **proposed** -- they are presented to the engineer for confirmation before execution. No Jira mutations are performed without explicit approval (per Guardrails).
