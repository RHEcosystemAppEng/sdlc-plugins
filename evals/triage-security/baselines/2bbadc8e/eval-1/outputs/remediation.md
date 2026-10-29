# Step 7.5 -- Release Jira Orchestration

## 7.5.1 -- Resolve Stream-to-Version Mapping

The issue is scoped to the **2.2.x** stream. The affected versions within scope are 2.2.0, 2.2.1, and 2.2.2. The release family is **2.2.x**.

The latest released version in the 2.2.x stream supportability matrix is **2.2.4** (build 0.4.12, dated 2026-05-04). The default next patch version would be **2.2.5**.

**PROPOSAL** (no Jira operations performed):

1. Search for an existing release Epic matching `"RHTPA 2.2.* Release Tasks"` via JQL:
   ```
   project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.2' AND summary ~ 'Release Tasks' ORDER BY created DESC
   ```

2. If no release Epic found, propose creating one:
   - **Summary**: "RHTPA 2.2.5 Release Tasks"
   - **Description**: "Release tracking Epic for RHTPA 2.2.5. Contains CVE triage and remediation tasks for this release."
   - **Labels**: ["ai-generated-jira"]
   - Engineer confirmation required before creation (version decision is high-stakes).

## 7.5.2 -- Find or Create Release Task

**PROPOSAL** (no Jira operations performed):

1. Search for an existing release Task under the release Epic:
   ```
   project = TC AND issuetype = Task AND parent = <release-epic-key> AND summary ~ 'RHTPA 2.2.5 CVE triage' ORDER BY created DESC
   ```

2. If no release Task found, propose creating one:
   - **Summary**: "RHTPA 2.2.5 CVE triage"
   - **Description**: "CVE triage tracking task for RHTPA 2.2.5. Linked to CVE Vulnerability issues (Related) and blocked by remediation Tasks (Blocks)."
   - **Labels**: ["ai-generated-jira"]
   - **Parent**: <release-epic-key>
   - Engineer confirmation required before creation.

## 7.5.3 -- Cross-CVE Dedup Decision

The Upstream Affected Component custom field is **not configured** in the project's Security Configuration. Per the skill methodology, the cross-CVE dedup check requires this field to be configured. Since it is absent, **Step 7.5.3 dedup is skipped entirely**.

No existing remediation task coverage needs to be checked. Proceed to Step 8 remediation task creation for the 2.2.x stream.

---

# Step 8 -- Remediation

## Triage Decision Path

1. **Any supported versions affected?** YES -- versions 2.2.0, 2.2.1, 2.2.2 in the 2.2.x stream are affected.
2. **Issue scoped to a single stream?** YES -- scoped to 2.2.x via suffix `[rhtpa-2.2]`.
3. **Other streams also affected?** YES -- stream 2.1.x (versions 2.1.0, 2.1.1) is also affected.
4. **Case A applies**: Post cross-stream impact comment, then Case B remediation.

## Case A -- Cross-Stream Impact

The version impact analysis reveals that stream **2.1.x** (outside this issue's scope) is also affected:

- 2.1.0: quinn-proto 0.11.9 (affected)
- 2.1.1: quinn-proto 0.11.9 (affected)

**PROPOSAL** (no Jira operations performed):

1. Post cross-stream impact comment on TC-8001:
   > Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.
   > These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

2. Check for existing CVE Jiras for 2.1.x via JQL:
   ```
   project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001
   ```

3. If no sibling CVE Jira exists for 2.1.x, create **preemptive** remediation tasks for 2.1.x (see Preemptive Tasks below).

4. If a sibling CVE Jira exists for 2.1.x, skip preemptive task creation for that stream -- it will be triaged through its own CVE issue.

## Case B -- Remediation Tasks for 2.2.x Stream (in-scope)

The 2.2.x stream has the upstream fix already available (quinn-proto 0.11.14 is at HEAD of release/0.4.z branch, confirmed by versions 2.2.3 and 2.2.4 shipping the fix). Therefore, the **dependency bump** variant is used instead of upstream backport.

Ecosystem: **Cargo** (source dependency) -- produces **2 tasks** per stream.

### Task 1: Dependency Bump (2.2.x)

**PROPOSAL** -- Jira Task to be created:

- **Summary**: "Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)"
- **Labels**: ["ai-generated-jira", "Security", "CVE-2026-31812"]
- **Link**: Depend (TC-8001 inward, this task outward)

**Description**:

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream --
a package manager update is sufficient.

Affected versions: 2.2.0 (v0.4.5, quinn-proto 0.11.9), 2.2.1 (v0.4.8,
quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1, quinn-proto 0.11.12)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct or transitive (to be confirmed via Cargo.toml inspection)
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the
  latest compatible version (>= 0.11.14)
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

### Task 2: Downstream Propagation (2.2.x)

**PROPOSAL** -- Jira Task to be created:

- **Summary**: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)"
- **Labels**: ["ai-generated-jira", "Security", "CVE-2026-31812"]
- **Link**: Depend (TC-8001 inward, this task outward)
- **Blocks**: Blocked by Task 1 (dependency bump must merge first)

**Description**:

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the dependency bump task.

The dependency bump task bumps quinn-proto to 0.11.14 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <dependency-bump-task-key> (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

## Case A -- Preemptive Remediation Tasks for 2.1.x Stream (if no sibling CVE exists)

If no sibling CVE Jira exists for the 2.1.x stream, the following preemptive tasks would be created. The 2.1.x upstream branch (release/0.3.z) does NOT have the fix (v0.3.12 ships quinn-proto 0.11.9), so the **upstream backport** variant is used.

### Preemptive Task 1: Upstream Backport (2.1.x)

**PROPOSAL** -- Jira Task to be created (preemptive):

- **Summary**: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)"
- **Labels**: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
- **Link**: Related (TC-8001 -- not Depend, because this is preemptive from a different stream's CVE)

**Description**:

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8, quinn-proto 0.11.9), 2.1.1 (v0.3.12,
quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct or transitive (to be confirmed via Cargo.toml inspection)
- The fix is NOT yet on the release/0.3.z branch (v0.3.12 ships quinn-proto 0.11.9)
- An upstream backport or dependency bump is required on release/0.3.z

### Remediation approach

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock on the
  release/0.3.z branch
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)
- Reference upstream fix PR: https://github.com/quinn-rs/quinn/pull/2048

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

- Depends on: TC-8001 (originating CVE, cross-stream)
```

### Preemptive Task 2: Downstream Propagation (2.1.x)

**PROPOSAL** -- Jira Task to be created (preemptive):

- **Summary**: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)"
- **Labels**: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
- **Link**: Related (TC-8001)
- **Blocks**: Blocked by Preemptive Task 1 (upstream backport must merge first)

**Description**:

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-backport-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (originating CVE, cross-stream)
```

## Post-Creation Jira Linkage (PROPOSALS)

After creating remediation tasks, the following Jira links would be established:

### 2.2.x stream (standard remediation):

1. **Depend**: TC-8001 (inward) -> dependency bump task (outward) -- standard remediation linkage
2. **Depend**: TC-8001 (inward) -> downstream propagation task (outward) -- standard remediation linkage
3. **Blocks**: dependency bump task (inward) -> downstream propagation task (outward) -- upstream blocks downstream
4. **Blocks**: dependency bump task (inward) -> release Task (outward) -- remediation blocks release
5. **Blocks**: downstream propagation task (inward) -> release Task (outward) -- remediation blocks release
6. **Related**: release Task (inward) -> TC-8001 (outward) -- CVE traceability to release

### 2.1.x stream (preemptive, if no sibling CVE exists):

1. **Related**: TC-8001 (inward) -> preemptive upstream backport task (outward) -- preemptive uses Related, not Depend
2. **Related**: TC-8001 (inward) -> preemptive downstream propagation task (outward) -- preemptive uses Related
3. **Blocks**: preemptive upstream backport task (inward) -> preemptive downstream propagation task (outward) -- upstream blocks downstream

## Post-Triage Summary (PROPOSAL)

After all triage actions are complete, the following would be applied to TC-8001:

1. **Add label**: `ai-cve-triaged` to TC-8001
2. **Post summary comment** documenting:
   - Version impact table (all streams)
   - Affects Versions correction: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
   - Remediation tasks created for 2.2.x (dependency bump + downstream propagation)
   - Cross-stream impact on 2.1.x (preemptive tasks if created)
   - Release Jira references (Epic and Task keys, if created)
   - @mention of the issue reporter (using reporter's Jira account ID)

All actions above are PROPOSALS. No Jira operations were performed.
