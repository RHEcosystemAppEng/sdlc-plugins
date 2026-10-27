# Step 8 -- Remediation: TC-8001

## Triage Decision Tree

1. **Any supported versions affected?** YES -- 2.2.0, 2.2.1, 2.2.2 in scope; 2.1.0, 2.1.1 out of scope.
2. **Issue scoped to a single stream?** YES -- scoped to 2.2.x via suffix `[rhtpa-2.2]`.
3. **Other streams also affected?** YES -- 2.1.x is affected (Case A applies).
4. **Ecosystem classification?** Cargo = source dependency.
5. **Upstream fix available (Step 2.5)?**
   - 2.2.x (`release/0.4.z`): YES -- use dependency bump variant (2 tasks).
   - 2.1.x (`release/0.3.z`): NO -- use upstream backport variant (2 tasks, preemptive).

## Case A: Cross-Stream Impact

Stream 2.1.x is affected but is outside the issue's scope (TC-8001 is scoped to 2.2.x). A sibling Vulnerability issue search would be performed for CVE-2026-31812 with stream suffix matching 2.1.x. If no sibling exists, preemptive remediation tasks are created for the 2.1.x stream.

### Cross-stream impact comment (posted to TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based
on lock file analysis. This stream is tracked by a companion issue (see
Related links) or may require separate PSIRT triage.
```

---

## Case B: Remediation Tasks for 2.2.x (In-Scope, Dependency Bump Variant)

Since Step 2.5 confirms the upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 (fixed version), the dependency bump variant is used.

### Task 1: Dependency Bump Task (2.2.x)

**Jira creation call:**

```
bump_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)",
  description: <see description below>,
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

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (v0.4.9, retag of v0.4.8)
Source commit(s): v0.4.5, v0.4.8, v0.4.9

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

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

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

#### Description Digest Protocol for Task 1 (Dependency Bump)

After creating the task, perform the following steps in order, BEFORE creating any issue links or other comments:

1. **Re-fetch the description from Jira** to get the Jira-normalized content:
   ```
   bump_desc = jira.get_issue(<bump-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file:**
   ```
   # Write the description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest** using the project script:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format (ADF JSON or markdown) and outputs a format-tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.

4. **Post the digest comment to Jira** on the newly created task:
   ```
   jira.add_comment(<bump-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a3f8...64 hex chars...`). The comment body is exactly one line: `[sdlc-workflow] Description digest: sha256-md:<64-char-hex>`.

5. **Only after the digest comment is posted**, proceed to create issue links:
   - Link bump task to TC-8001 (Depend): `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <bump-task-key>, type: "Depend")`

---

### Task 2: Downstream Propagation Task (2.2.x)

**Jira creation call:**

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <see description below>,
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

The dependency bump (<bump-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct -- carried forward from upstream task
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

- Depends on: <bump-task-key> (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Protocol for Task 2 (Downstream Propagation, 2.2.x)

After creating the task, perform the following steps in order, BEFORE creating any issue links or other comments:

1. **Re-fetch the description from Jira** to get the Jira-normalized content:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file:**
   ```
   # Write the description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest** using the project script:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format and outputs a format-tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).

4. **Post the digest comment to Jira** on the newly created task:
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py`. The comment is exactly one line: `[sdlc-workflow] Description digest: sha256-md:<64-char-hex>`.

5. **Only after the digest comment is posted**, proceed to create issue links:
   - Link downstream task to TC-8001 (Depend): `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")`
   - Link downstream task as blocked by bump task (Blocks): `jira.create_link(inwardIssue: <bump-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`

---

## Case A: Preemptive Remediation Tasks for 2.1.x (Out-of-Scope, Upstream Backport Variant)

Stream 2.1.x is affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9) but has no stream-scoped CVE Jira. The upstream branch `release/0.3.z` does NOT yet ship the fix (latest tag v0.3.12 has quinn-proto 0.11.9). Preemptive tasks use the upstream backport variant and carry the `security-preemptive` label.

### Task 3: Upstream Backport Task (2.1.x, Preemptive)

**Jira creation call:**

```
upstream_task_21 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
  description: <see description below>,
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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9), RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)
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

#### Description Digest Protocol for Task 3 (Upstream Backport, 2.1.x Preemptive)

After creating the task, perform the following steps in order, BEFORE creating any issue links or other comments:

1. **Re-fetch the description from Jira** to get the Jira-normalized content:
   ```
   upstream_desc_21 = jira.get_issue(<upstream-task-21-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file:**
   ```
   # Write the description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest** using the project script:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format and outputs a format-tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).

4. **Post the digest comment to Jira** on the newly created task:
   ```
   jira.add_comment(<upstream-task-21-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py`. The comment is exactly one line: `[sdlc-workflow] Description digest: sha256-md:<64-char-hex>`.

5. **Only after the digest comment is posted**, proceed to create issue links:
   - Link preemptive task to TC-8001 (Related, not Depend -- because the originating CVE belongs to a different stream): `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-21-key>, type: "Related")`

---

### Task 4: Downstream Propagation Task (2.1.x, Preemptive)

**Jira creation call:**

```
downstream_task_21 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see description below>,
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
CVE-2026-31812 fix from <upstream-task-21-key>.

The upstream backport (<upstream-task-21-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct -- carried forward from upstream task
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

- Depends on: <upstream-task-21-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Protocol for Task 4 (Downstream Propagation, 2.1.x Preemptive)

After creating the task, perform the following steps in order, BEFORE creating any issue links or other comments:

1. **Re-fetch the description from Jira** to get the Jira-normalized content:
   ```
   downstream_desc_21 = jira.get_issue(<downstream-task-21-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file:**
   ```
   # Write the description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest** using the project script:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format and outputs a format-tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).

4. **Post the digest comment to Jira** on the newly created task:
   ```
   jira.add_comment(<downstream-task-21-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py`. The comment is exactly one line: `[sdlc-workflow] Description digest: sha256-md:<64-char-hex>`.

5. **Only after the digest comment is posted**, proceed to create issue links:
   - Link preemptive downstream task to TC-8001 (Related): `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-21-key>, type: "Related")`
   - Link downstream as blocked by upstream (Blocks): `jira.create_link(inwardIssue: <upstream-task-21-key>, outwardIssue: <downstream-task-21-key>, type: "Blocks")`

---

## Sequencing Summary

The full ordered sequence of Jira operations after all tasks are created:

### For each task, the order is strictly:
1. `create_issue` -- create the task
2. `get_issue` -- re-fetch the description from Jira (not the input string)
3. `sha256-digest.py` -- compute digest from re-fetched description
4. `add_comment` -- post `[sdlc-workflow] Description digest: <tagged-digest>`
5. `create_link` -- create Depend/Related/Blocks links

### Full operation sequence:

**Task 1 (Dependency bump, 2.2.x):**
1. `jira.create_issue(...)` -- create bump task
2. `jira.get_issue(<bump-task-key>, fields=["description"])` -- re-fetch description
3. `python3 scripts/sha256-digest.py /tmp/task-desc.md` -- compute digest
4. `jira.add_comment(<bump-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")` -- post digest
5. `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <bump-task-key>, type: "Depend")` -- link to CVE

**Task 2 (Downstream propagation, 2.2.x):**
1. `jira.create_issue(...)` -- create downstream task
2. `jira.get_issue(<downstream-task-key>, fields=["description"])` -- re-fetch description
3. `python3 scripts/sha256-digest.py /tmp/task-desc.md` -- compute digest
4. `jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")` -- post digest
5. `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")` -- link to CVE
6. `jira.create_link(inwardIssue: <bump-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")` -- blocked by bump

**Task 3 (Upstream backport, 2.1.x preemptive):**
1. `jira.create_issue(...)` -- create upstream backport task
2. `jira.get_issue(<upstream-task-21-key>, fields=["description"])` -- re-fetch description
3. `python3 scripts/sha256-digest.py /tmp/task-desc.md` -- compute digest
4. `jira.add_comment(<upstream-task-21-key>, "[sdlc-workflow] Description digest: <tagged-digest>")` -- post digest
5. `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-21-key>, type: "Related")` -- Related (preemptive, not Depend)

**Task 4 (Downstream propagation, 2.1.x preemptive):**
1. `jira.create_issue(...)` -- create downstream task
2. `jira.get_issue(<downstream-task-21-key>, fields=["description"])` -- re-fetch description
3. `python3 scripts/sha256-digest.py /tmp/task-desc.md` -- compute digest
4. `jira.add_comment(<downstream-task-21-key>, "[sdlc-workflow] Description digest: <tagged-digest>")` -- post digest
5. `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-21-key>, type: "Related")` -- Related (preemptive)
6. `jira.create_link(inwardIssue: <upstream-task-21-key>, outwardIssue: <downstream-task-21-key>, type: "Blocks")` -- blocked by upstream backport

### After all task creation and linking:

- Post preemptive task comment to TC-8001 listing the 2.1.x preemptive tasks
- Add `ai-cve-triaged` label to TC-8001
- Post the post-triage summary comment to TC-8001 with version impact table, Affects Versions correction, and all created task links

## Key Protocol Rules

- The digest is computed from the **re-fetched** description (after Jira normalization), NOT from the input string passed to `create_issue`
- The `scripts/sha256-digest.py` script auto-detects format (ADF vs markdown) and outputs a tagged digest
- The digest comment marker is exactly: `[sdlc-workflow] Description digest:`
- The digest comment must be posted **before** any issue links (Depend, Blocks, Related) or other comments on the task
- The digest comment is a standalone comment, not embedded in other comments
- Preemptive tasks use "Related" link type (not "Depend") to the originating CVE
- Standard tasks use "Depend" link type to their own CVE
