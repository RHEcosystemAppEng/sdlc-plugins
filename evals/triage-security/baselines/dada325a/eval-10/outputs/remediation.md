# Step 8 – Remediation: TC-8020 (CVE-2026-55123, tokio < 1.42.0)

Decision path: supported versions are affected. The issue is scoped to `[rhtpa-2.2]`, and another stream
(rhtpa-2.1) is also affected with no CVE Jira of its own. Two sets of tasks follow:

- **Case A (current stream, rhtpa-2.2)**: standard remediation tasks linked to TC-8020 with **Depend**.
- **Case B (other stream, rhtpa-2.1)**: preemptive remediation tasks, labelled `security-preemptive`,
  linked to TC-8020 with **Related**.

Ecosystem: Cargo is a source dependency, so each stream gets **2 tasks**: an upstream backport and a downstream
propagation. The fix is not confirmed on the upstream branches, so the backport variant is used.

Each task creation is immediately followed by its description digest comment
(`[sdlc-workflow] Description digest: <sha256-md:...>`). The digest is posted before any links or other comments.

---

## Case A – Current stream rhtpa-2.2 (standard)

### Task A1 – Upstream backport (2.2.x)

- **Summary**: `Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)`
- **Issue type**: Task, project TC
- **Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123"]`
- **Links**: TC-8020 -> A1 (**Depend**). A1 -> 2.2.x release Task (**Blocks**). A1 -> A2 (**Blocks**).

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: tokio use-after-free when a spawned task is aborted
while holding a borrowed reference (CVSS 8.1, High).
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed
version (1.42.0+).

Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1),
RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (verify against Cargo.toml; if transitive, record the chain)

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.lock (and Cargo.toml if pinned)
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency** that pulls in tokio to a version
whose transitive closure includes tokio >= 1.42.0.
**Fallback: pin the transitive dependency directly** via
`cargo add tokio@1.42.0`; document why the direct bump was not viable.

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (parent tracking issue)
```

### Task A2 – Downstream propagation (2.2.x)

- **Summary**: `Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
- **Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123"]`
- **Links**: TC-8020 -> A2 (**Depend**). A1 -> A2 (**Blocks**, so A2 is blocked by A1). A2 -> 2.2.x release Task (**Blocks**).

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from <A1-key>.

The upstream backport (<A1-key>) bumps tokio to 1.42.0 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release repo
so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <A1-key> (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

### Release Jira linkage (2.2.x, Step 7.5)
- A1 and A2 each **Block** the 2.2.x release Task ("RHTPA <next-2.2.z> CVE triage").
- The release Task is linked to TC-8020 with **Related**.

---

## Case B – Other stream rhtpa-2.1 (preemptive; no CVE Jira exists)

The JQL sibling search for label `CVE-2026-55123` returned no Vulnerability issue for rhtpa-2.1, so preemptive tasks are created.
No Vulnerability issue is created, because PSIRT owns those.

### Task B1 – Upstream backport (2.1.x, preemptive)

- **Summary**: `Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)`
- **Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`
- **Links**: TC-8020 -> B1 (**Related**, not Depend). B1 -> B2 (**Blocks**). Not linked to release Jira (preemptive).

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-55123: tokio use-after-free when a spawned task is aborted
while holding a borrowed reference (CVSS 8.1, High).
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed
version (1.42.0+).

Affected versions: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (verify against Cargo.toml; if transitive, record the chain)

### Remediation approach (direct dependency)

- Update tokio dependency to >= 1.42.0 in Cargo.lock (and Cargo.toml if pinned)
- tokio 1.40.0 -> 1.42.0 spans two minor versions; check the upstream
  changelog for MSRV or behavioral changes on the 0.3.z branch

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency** that pulls in tokio.
**Fallback: pin** via `cargo add tokio@1.42.0`; document why in the PR.

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)
```

### Task B2 – Downstream propagation (2.1.x, preemptive)

- **Summary**: `Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
- **Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`
- **Links**: TC-8020 -> B2 (**Related**). B1 -> B2 (**Blocks**).

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from <B1-key>.

The upstream backport (<B1-key>) bumps tokio to 1.42.0 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo
so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <B1-key> (upstream backport must merge first)
- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)
```

---

## Pre-creation checklist

- [x] Task count per stream: Cargo is a source dependency, so 2 tasks per stream (A1+A2, B1+B2)
- [x] Cross-stream coverage: the only out-of-scope affected stream (rhtpa-2.1) has preemptive tasks
- [x] Link types: Depend (A1, A2 -> TC-8020); Related (B1, B2 -> TC-8020); Blocks (A1->A2, B1->B2)
- [x] Preemptive labels: B1 and B2 carry `security-preemptive`
- [x] Coordination guidance: omitted because the Deployment Context column is absent (backward compatibility)
- [x] Release Jira linking: A1 and A2 Block the 2.2.x release Task. TC-8020 is Related to the release Task. Preemptive tasks are not linked.
- [x] Dedup consistency: no Step 7.5.3 dedup match, so tasks are created

## Post-triage

- Transition TC-8020 to In Progress, or skip if it is already in Assigned, an indeterminate-category status.
- Add the `ai-cve-triaged` label to TC-8020.
- Post a summary comment covering: the impact table, the Affects Versions correction, the outcome (remediation created), the A1/A2/B1/B2 keys, the release Epic/Task keys, an @mention of the reporter, and the Comment Footnote (`sdlc-workflow/triage-security v0.13.10`).
- Every Jira mutation above requires engineer confirmation before execution.
