# TC-8001 — Step 8: Remediation

## Decision

- The issue is **scoped** to 2.2.x (`[rhtpa-2.2]`). 2.2.0–2.2.2 are affected, so **Case B** applies.
- Another stream (2.1.x) is also affected and has no known sibling CVE Jira. **Case A** applies:
  post a cross-stream comment and create **preemptive** 2.1.x tasks (`security-preemptive`,
  "Related" link).
- Ecosystem Cargo is a source dependency, so **2 tasks per stream**:
  - 2.2.x: fix already on `release/0.4.z` (shipped in 2.2.3/2.2.4). Use the **dependency bump +
    downstream propagation** pair.
  - 2.1.x: no fix on `release/0.3.z`. Use the **upstream backport + downstream propagation** pair
    (preemptive).
- Triage note for the confirmation gate: the latest 2.2.x release (2.2.4) already ships
  quinn-proto 0.11.14. Tasks T1/T2 mainly verify that the release branch and the next z-stream
  build keep the fix and close out the tracking. The engineer may decline them at the gate and
  treat 2.2.x as "fixed in 2.2.3".
- No dedup (Step 7.5.3 skipped, because the Upstream Affected Component field is not configured).
- Coordination Guidance is omitted (no Deployment Context column).

Labels for every task: `ai-generated-jira`, `Security`, `CVE-2026-31812` (+ `security-preemptive` for 2.1.x).

---

## T1 — 2.2.x dependency bump (standard, Depend → TC-8001)

**Summary:** Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)
**Labels:** ai-generated-jira, Security, CVE-2026-31812

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (0.11.12),
RHTPA 2.2.2 (retag of 2.2.1). Not affected: 2.2.3, 2.2.4 (0.11.14).
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: not determined during triage (Cargo.toml not inspected) —
  confirm whether quinn-proto is direct or transitive (e.g., via quinn)
- **Remediation action**: run `cargo update -p quinn-proto` to pull in the latest
  compatible version
- Tags v0.4.11 / v0.4.12 already ship quinn-proto 0.11.14; verify release/0.4.z HEAD
  still resolves >= 0.11.14 and no regression was introduced
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify the lock file reflects >= 0.11.14 after the update
- If the vulnerable dependency is dev-only or build-only, the remediation priority
  is Normal regardless of CVE severity. Add `dev-dependency` label to the task.

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

## T2 — 2.2.x downstream propagation (standard, blocked by T1)

**Summary:** Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)
**Labels:** ai-generated-jira, Security, CVE-2026-31812

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from {{T1.key}}.

The dependency bump ({{T1.key}}) bumps quinn-proto to 0.11.14 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: carried forward from {{T1.key}} (to be confirmed)
- Update the rhtpa-backend reference to the merged commit or new release tag
  (current 2.2.4 pin v0.4.12 already ships 0.11.14 — confirm the next pin keeps it)
- If the upstream fix pinned a transitive dependency directly (fallback approach),
  verify the pinning is reflected in the downstream build's lock file
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: {{T1.key}} (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

## T3 — 2.1.x upstream backport (PREEMPTIVE, Related → TC-8001)

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
**Labels:** ai-generated-jira, Security, CVE-2026-31812, security-preemptive

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

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (remote DoS
via crafted STREAMS frame). The vulnerable dependency (quinn-proto < 0.11.14)
must be updated to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: not determined during triage — confirm direct vs transitive
- If the vulnerable dependency is dev-only or build-only, the remediation priority
  is Normal regardless of CVE severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto
- Bump it to a version whose transitive closure includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
- `cargo add quinn-proto@0.11.14` to override the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

## T4 — 2.1.x downstream propagation (PREEMPTIVE, blocked by T3)

**Summary:** Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)
**Labels:** ai-generated-jira, Security, CVE-2026-31812, security-preemptive

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
CVE-2026-31812 fix from {{T3.key}}.

The upstream backport ({{T3.key}}) bumps quinn-proto to 0.11.14 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: carried forward from {{T3.key}}
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback approach),
  verify the pinning is reflected in the downstream build's lock file
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: {{T3.key}} (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Execution sequence with description digest comments

Every step runs only after engineer confirmation at the gate. Per
`shared/description-digest-protocol.md`, the digest comment is posted **right after each
task is created and before any link or other comment on that task**. It is a standalone,
single-line comment with no footnote, using the exact marker
`[sdlc-workflow] Description digest:`. The digest is computed from the description
**re-fetched from Jira** (never from the string passed to `create_issue`) by
`scripts/sha256-digest.py`, and the full tagged 64-hex value is posted. No placeholder,
abbreviated, or example hash is used. The values are not computed here because no Jira
issue was created in this eval.

### 2.2.x (standard)

1. `jira.create_issue(projectKey: "TC", issueTypeName: "Task", summary: "Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)", description: <T1>, labels: ["ai-generated-jira","Security","CVE-2026-31812"])` returns T1.key
2. **T1 digest:**
   - `jira.get_issue(T1.key, fields=["description"])`. Write the returned description to `/tmp/task-desc.md`.
   - `python3 scripts/sha256-digest.py /tmp/task-desc.md`, check exit code 0, and get `sha256-md:<64-hex>` (MCP/markdown) or `sha256-adf:<64-hex>` (REST/ADF).
   - `jira.add_comment(T1.key, "[sdlc-workflow] Description digest: <full tagged digest output>")` (ADF single paragraph).
3. `jira.create_issue(... summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)", description: <T2 with T1.key substituted>, labels: ["ai-generated-jira","Security","CVE-2026-31812"])` returns T2.key
4. **T2 digest:** same procedure: re-fetch T2 description, run `sha256-digest.py`, then `jira.add_comment(T2.key, "[sdlc-workflow] Description digest: <tagged digest>")`.
5. Links (only after both digests are posted):
   - `create_link(inward: TC-8001, outward: T1.key, type: "Depend")`
   - `create_link(inward: TC-8001, outward: T2.key, type: "Depend")`
   - `create_link(inward: T1.key, outward: T2.key, type: "Blocks")`
   - If the Step 7.5 release Task is active: `create_link(inward: T1.key, outward: <release-task>, "Blocks")`, `create_link(inward: T2.key, outward: <release-task>, "Blocks")`, `create_link(inward: <release-task>, outward: TC-8001, "Related")`

### 2.1.x (preemptive, Case A)

6. `jira.create_issue(... summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)", description: <T3>, labels: ["ai-generated-jira","Security","CVE-2026-31812","security-preemptive"])` returns T3.key
7. **T3 digest:** re-fetch the T3 description, run `sha256-digest.py`, then `jira.add_comment(T3.key, "[sdlc-workflow] Description digest: <tagged digest>")`.
8. `jira.create_issue(... summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)", description: <T4 with T3.key substituted>, labels: [..., "security-preemptive"])` returns T4.key
9. **T4 digest:** re-fetch the T4 description, run `sha256-digest.py`, then `jira.add_comment(T4.key, "[sdlc-workflow] Description digest: <tagged digest>")`.
10. Links (after the digests):
    - `create_link(inward: TC-8001, outward: T3.key, type: "Related")`
    - `create_link(inward: TC-8001, outward: T4.key, type: "Related")`
    - `create_link(inward: T3.key, outward: T4.key, type: "Blocks")`
    - (Preemptive tasks are not linked to the 2.2.x release Task.)

### Comments on TC-8001 (after all task digests and links). Each ends with the Comment Footnote

Footnote (ADF `rule` + paragraph): "This comment was AI-generated by
[sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0."

11. Cross-stream impact: "Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s)
    2.1.x (2.1.0, 2.1.1 ship 0.11.9) based on lock file analysis. These streams are tracked by
    companion issues (see Related links) or may require separate PSIRT triage."
12. Preemptive task list: "Preemptive remediation tasks created for streams without CVE Jiras:
    - 2.1.x: T3.key, T4.key (security-preemptive). These tasks use the "Related" link type and
    carry the security-preemptive label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
    reconciliation will link them and remove the label."
13. Task list: "Remediation tasks created: T1.key (dependency bump), T2.key (downstream
    propagation, blocked by T1.key)".
14. Transition TC-8001 to In Progress (skip if the workflow treats Assigned as equivalent or later).
15. Post-triage: add the `ai-cve-triaged` label. Post a summary comment with the version impact
    table, the Affects Versions correction (RHTPA 2.0.0 → RHTPA 2.2.0, 2.2.1, 2.2.2), the
    outcome (remediation created, and 2.2.x fixed since 2.2.3), task keys T1–T4, release
    Epic/Task keys, no dedup, and an ADF @mention of the TC-8001 reporter.

## Pre-creation checklist

- [x] Task count per stream: 2 (Cargo is a source dependency)
- [x] Cross-stream coverage: 2.1.x gets preemptive T3/T4 (no sibling found)
- [x] Link types: Depend (T1/T2 → TC-8001), Related (T3/T4 preemptive), Blocks (T1→T2, T3→T4)
- [x] Preemptive labels on T3/T4
- [x] Coordination guidance: omitted (no Deployment Context column)
- [x] Release Jira linking: only the non-preemptive T1/T2
- [x] Dedup consistency: not applicable
- [x] A digest comment follows each create_issue, before any link or comment on that task
