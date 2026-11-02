# Step 8 — Remediation (Case B: Affected — create remediation tasks)

The version impact table shows affected versions in the 2.2.x stream (2.2.0, 2.2.1, 2.2.2). Ecosystem is Cargo (source dependency) → create **two** tasks: upstream backport + downstream propagation.

## Step 7.5 — Release Jira Orchestration

Before creating remediation tasks, the release Jira structure is resolved per Step 7.5. Confirmation from the engineer is required for version selection and Epic/Task creation. Since this eval prohibits actual Jira calls, these are described as planned procedures.

## Step 7.5.3 — Release Dedup

The Upstream Affected Component configuration is absent from the Security Configuration (no `customfield_10632` configured), so release dedup (Step 7.5.3) is **skipped entirely** per its prerequisite.

## Remediation Task 1: Upstream Backport

### Task Details

- **Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)
- **Issue Type**: Task
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Project**: TC

### Task Description

```
## Repository

rhtpa-backend (from Ecosystem Mappings Repository column, backend → rhtpa-backend)

## Target Branch

release/0.4.z (from Ecosystem Mappings Upstream Branch column for 2.2.x stream)

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- Run `cargo update -p quinn-proto` to update Cargo.lock

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Protocol for Upstream Backport Task

After creating the upstream backport task via `jira.create_issue(...)`, the following description digest protocol is executed **before** creating any issue links or posting any other comments:

1. **Re-fetch the task description from Jira** (not the description string passed to `create_issue`):
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
   The re-fetch is critical because Jira may transform the description during storage (e.g., ADF normalization, whitespace changes). The digest must be computed from what Jira actually stored, not what was submitted.

2. **Write the re-fetched description to a temporary file**:
   ```
   Write the description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest** using `scripts/sha256-digest.py`:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a tagged digest in the format `sha256-md:<hex>` (for Markdown descriptions) or `sha256-adf:<hex>` (for ADF descriptions).

4. **Post the digest comment** on the upstream backport task with the marker `[sdlc-workflow] Description digest:`:
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

5. **Only after the digest comment is posted**, proceed to create issue links:
   - `Depend` link: TC-8001 (Vulnerability) → <upstream-task-key>
   - `Blocks` link: <upstream-task-key> → <downstream-task-key>

This ordering (digest comment BEFORE links) ensures that `/implement-task` can verify description integrity in its Step 1.5 before processing the task.

---

## Remediation Task 2: Downstream Propagation Subtask

### Task Details

- **Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
- **Issue Type**: Task
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Project**: TC

### Task Description

```
## Repository

rhtpa-release.0.4.z (from Version Streams table for 2.2.x stream)

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
- **Dependency type**: direct — carried forward from upstream task
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

### Description Digest Protocol for Downstream Propagation Subtask

After creating the downstream propagation subtask via `jira.create_issue(...)`, the following description digest protocol is executed **before** creating any issue links or posting any other comments:

1. **Re-fetch the task description from Jira** (not the description string passed to `create_issue`):
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
   The re-fetch is critical because Jira may transform the description during storage. The digest must be computed from what Jira actually stored.

2. **Write the re-fetched description to a temporary file**:
   ```
   Write the description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest** using `scripts/sha256-digest.py`:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a tagged digest in the format `sha256-md:<hex>` or `sha256-adf:<hex>`.

4. **Post the digest comment** on the downstream propagation subtask with the marker `[sdlc-workflow] Description digest:`:
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

5. **Only after the digest comment is posted**, proceed to create issue links:
   - `Depend` link: TC-8001 (Vulnerability) → <downstream-task-key>
   - `Blocks` link: <upstream-task-key> → <downstream-task-key>

---

## Digest Protocol Summary (Both Tasks)

The description digest protocol per `shared/description-digest-protocol.md` requires:

1. **Hashing source**: The digest is computed from the **re-fetched** description (via Jira API after `create_issue`), NOT from the description string passed to `create_issue`. This accounts for any transformations Jira applies during storage.

2. **Digest tool**: `python3 scripts/sha256-digest.py <file>` computes the SHA-256 and outputs a tagged format (`sha256-md:<hex>` or `sha256-adf:<hex>`).

3. **Comment marker**: Every digest comment uses the exact marker `[sdlc-workflow] Description digest:` followed by the tagged digest.

4. **Ordering rule**: Digest comments are posted BEFORE any issue links (`Depend`, `Blocks`, `Related`) or other comments on the task. This is enforced for both the upstream backport task and the downstream propagation subtask.

5. **Per-task requirement**: Each remediation task gets its own independent digest — the upstream backport task and the downstream propagation subtask each go through the full protocol independently.

## Jira Linkage (after digest comments)

After both tasks have their digest comments posted:

1. `Depend` link: TC-8001 → <upstream-task-key>
2. `Depend` link: TC-8001 → <downstream-task-key>
3. `Blocks` link: <upstream-task-key> → <downstream-task-key>
4. Transition TC-8001 to In Progress
5. Add `ai-cve-triaged` label to TC-8001
6. Post summary comment on TC-8001 listing created tasks
